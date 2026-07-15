#!/usr/bin/env bash
set -uo pipefail
set -C
umask 077

PYTHON=/home/chakwong/miniconda3/envs/tfgpu/bin/python3
P01_ROOT=.local/mathdevmcp/evidence/p01-20260711

usage() {
  printf '%s\n' \
    'Usage: scripts/p01_bootstrap_gate.sh MODE --attempt b0N --entry-root PATH --attempt-root PATH --prior-round-close NONE|PATH' \
    'MODE is exactly run, close, or verify.'
}

fail() {
  printf 'p01 bootstrap error: %s\n' "$*" >&2
  exit 2
}

sha_file() {
  sha256sum -- "$1" | cut -d ' ' -f 1
}

byte_count() {
  wc -c < "$1" | tr -d '[:space:]'
}

fsync_file() {
  "$PYTHON" -c 'import os,sys; fd=os.open(sys.argv[1], os.O_RDONLY|os.O_NOFOLLOW); os.fsync(fd); os.close(fd)' "$1"
}

fsync_dir() {
  "$PYTHON" -c 'import os,sys; fd=os.open(sys.argv[1], os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW); os.fsync(fd); os.close(fd)' "$1"
}

atomic_publish() {
  local temporary=$1
  local destination=$2
  fsync_file "$temporary"
  if ! ln -- "$temporary" "$destination"; then
    rm -f -- "$temporary"
    return 1
  fi
  fsync_dir "$(dirname -- "$destination")"
  rm -f -- "$temporary"
  fsync_dir "$(dirname -- "$destination")"
}

validate_relative_path() {
  local value=$1
  [[ -n "$value" && "$value" != /* && "$value" != *\\* ]] || return 1
  local part
  IFS='/' read -r -a parts <<< "$value"
  for part in "${parts[@]}"; do
    [[ -n "$part" && "$part" != . && "$part" != .. ]] || return 1
  done
}

validate_components_no_symlink() {
  local value=$1
  local current=.
  local part
  IFS='/' read -r -a parts <<< "$value"
  for part in "${parts[@]}"; do
    current=$current/$part
    if [[ -e "$current" || -L "$current" ]]; then
      [[ ! -L "$current" ]] || return 1
    fi
  done
}

require_regular() {
  local value=$1
  validate_relative_path "$value" || return 1
  validate_components_no_symlink "$value" || return 1
  [[ -f "$value" && ! -L "$value" ]]
}

current_manifest() {
  local output=$1
  find src tests scripts -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.pyo' -print0 \
    | LC_ALL=C sort -z \
    | xargs -0 sha256sum >| "$output"
}

set_command() {
  local number=$1
  case "$number" in
    1)
      COMMAND_ID=bootstrap_pytest
      COMMAND=(
        "$PYTHON" -m pytest -q
        tests/test_evidence_manifest.py::test_governance_records_require_strict_canonical_bytes
        tests/test_evidence_manifest.py::test_governance_store_is_no_overwrite_regular_file
        tests/test_evidence_manifest.py::test_round_close_schema_enforces_stage_nullability_and_both_entry_bindings
        tests/test_evidence_manifest.py::test_review_and_audit_grammars_are_closed_unique_and_final
        tests/test_evidence_manifest.py::test_governance_receipt_chain_and_action_bindings_are_closed
        tests/test_evidence_manifest.py::test_stable_publication_revalidates_bindings_without_injected_authority
        tests/test_evidence_manifest.py::test_stable_publication_is_no_overwrite_hard_link_with_terminal_receipt
        tests/test_evidence_manifest.py::test_bootstrap_close_parser_matches_independent_ascii_grammar
      )
      ;;
    2)
      COMMAND_ID=bootstrap_compile
      COMMAND=(
        "$PYTHON" -m py_compile
        src/mathdevmcp/evidence_manifest.py
        scripts/generate_p01_synthetic_evidence.py
        scripts/p01_governance.py
        tests/test_evidence_manifest.py
        tests/test_promotion_policy.py
      )
      ;;
    3)
      COMMAND_ID=bootstrap_shell_syntax
      COMMAND=(bash -n scripts/p01_bootstrap_gate.sh)
      ;;
    4)
      COMMAND_ID=bootstrap_diff
      COMMAND=(git diff --check)
      ;;
    *) return 1 ;;
  esac
}

argv_digest() {
  "$PYTHON" -c 'import hashlib,sys; print(hashlib.sha256(b"\0".join(value.encode("utf-8") for value in sys.argv[1:])).hexdigest())' "$@"
}

line_value() {
  local line=$1
  local prefix=$2
  [[ "$line" == "$prefix"* ]] || return 1
  printf '%s' "${line#"$prefix"}"
}

validate_attempt_artifacts() {
  local require_pass=$1
  local ledger=$ATTEMPT_ROOT/bootstrap-command-ledger.txt
  local run_log=$ATTEMPT_ROOT/bootstrap-run.log
  local implementation=$ATTEMPT_ROOT/implementation-exit-sha256.txt
  require_regular "$ledger" || return 1
  require_regular "$run_log" || return 1
  require_regular "$implementation" || return 1
  [[ $(wc -l < "$ledger" | tr -d '[:space:]') == 56 ]] || return 1
  [[ $(tail -c 1 "$ledger" | od -An -t u1 | tr -d '[:space:]') == 10 ]] || return 1
  mapfile -t LEDGER_LINES < "$ledger"
  [[ ${#LEDGER_LINES[@]} == 56 ]] || return 1
  [[ ${LEDGER_LINES[0]} == MATHDEVMCP_P01_BOOTSTRAP_LEDGER_V1 ]] || return 1
  [[ ${LEDGER_LINES[1]} == "attempt=$ATTEMPT" ]] || return 1
  [[ ${LEDGER_LINES[2]} == "entry_implementation_manifest_sha256=$ENTRY_IMPLEMENTATION_SHA" ]] || return 1
  [[ ${LEDGER_LINES[3]} == "entry_protected_manifest_sha256=$ENTRY_PROTECTED_SHA" ]] || return 1
  [[ ${LEDGER_LINES[4]} == "prior_round_close_ref=$PRIOR_ROUND_CLOSE" ]] || return 1
  [[ ${LEDGER_LINES[5]} == "prior_round_close_sha256=$PRIOR_ROUND_CLOSE_SHA" ]] || return 1
  [[ ${LEDGER_LINES[6]} == command_count=4 ]] || return 1
  [[ ${LEDGER_LINES[55]} == END ]] || return 1

  VALIDATED_EXITS=()
  local number index tag expected_ref stdout_path stderr_path value
  for number in 1 2 3 4; do
    set_command "$number" || return 1
    index=$((7 + (number - 1) * 12))
    printf -v tag '%02d' "$number"
    [[ ${LEDGER_LINES[$index]} == "command_${tag}_id=$COMMAND_ID" ]] || return 1
    [[ ${LEDGER_LINES[$((index + 1))]} == "command_${tag}_argv_sha256=$(argv_digest "${COMMAND[@]}")" ]] || return 1
    value=$(line_value "${LEDGER_LINES[$((index + 2))]}" "command_${tag}_started_at_utc=") || return 1
    [[ $value =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || return 1
    value=$(line_value "${LEDGER_LINES[$((index + 3))]}" "command_${tag}_ended_at_utc=") || return 1
    [[ $value =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || return 1
    value=$(line_value "${LEDGER_LINES[$((index + 4))]}" "command_${tag}_wall_time_ns=") || return 1
    [[ $value =~ ^(0|[1-9][0-9]*)$ ]] || return 1
    value=$(line_value "${LEDGER_LINES[$((index + 5))]}" "command_${tag}_exit_code=") || return 1
    [[ $value =~ ^(0|[1-9][0-9]{0,2})$ && $value -le 255 ]] || return 1
    VALIDATED_EXITS+=("$value")
    expected_ref=logs/command-${tag}.stdout
    [[ ${LEDGER_LINES[$((index + 6))]} == "command_${tag}_stdout_ref=$expected_ref" ]] || return 1
    stdout_path=$ATTEMPT_ROOT/$expected_ref
    require_regular "$stdout_path" || return 1
    [[ ${LEDGER_LINES[$((index + 7))]} == "command_${tag}_stdout_sha256=$(sha_file "$stdout_path")" ]] || return 1
    [[ ${LEDGER_LINES[$((index + 8))]} == "command_${tag}_stdout_byte_count=$(byte_count "$stdout_path")" ]] || return 1
    expected_ref=logs/command-${tag}.stderr
    [[ ${LEDGER_LINES[$((index + 9))]} == "command_${tag}_stderr_ref=$expected_ref" ]] || return 1
    stderr_path=$ATTEMPT_ROOT/$expected_ref
    require_regular "$stderr_path" || return 1
    [[ ${LEDGER_LINES[$((index + 10))]} == "command_${tag}_stderr_sha256=$(sha_file "$stderr_path")" ]] || return 1
    [[ ${LEDGER_LINES[$((index + 11))]} == "command_${tag}_stderr_byte_count=$(byte_count "$stderr_path")" ]] || return 1
  done

  [[ $(wc -l < "$run_log" | tr -d '[:space:]') == 7 ]] || return 1
  mapfile -t RUN_LINES < "$run_log"
  [[ ${#RUN_LINES[@]} == 7 ]] || return 1
  [[ ${RUN_LINES[0]} == MATHDEVMCP_P01_BOOTSTRAP_RUN_V1 ]] || return 1
  [[ ${RUN_LINES[1]} == "attempt=$ATTEMPT" ]] || return 1
  [[ ${RUN_LINES[2]} == "bootstrap_pytest_exit=${VALIDATED_EXITS[0]}" ]] || return 1
  [[ ${RUN_LINES[3]} == "bootstrap_compile_exit=${VALIDATED_EXITS[1]}" ]] || return 1
  [[ ${RUN_LINES[4]} == "bootstrap_shell_syntax_exit=${VALIDATED_EXITS[2]}" ]] || return 1
  [[ ${RUN_LINES[5]} == "bootstrap_diff_exit=${VALIDATED_EXITS[3]}" ]] || return 1
  local expected_status=PASS
  for value in "${VALIDATED_EXITS[@]}"; do
    [[ $value == 0 ]] || expected_status=FAIL
  done
  [[ ${RUN_LINES[6]} == "status=$expected_status" ]] || return 1
  if [[ $require_pass == yes ]]; then
    [[ $expected_status == PASS ]] || return 1
  fi

  local current_temp
  current_temp=$(mktemp "$ATTEMPT_ROOT/.implementation-current.XXXXXX") || return 1
  current_manifest "$current_temp"
  if ! cmp -s -- "$implementation" "$current_temp"; then
    rm -f -- "$current_temp"
    return 1
  fi
  rm -f -- "$current_temp"
  IMPLEMENTATION_EXIT_SHA=$(sha_file "$implementation")
  LEDGER_SHA=$(sha_file "$ledger")
  RUN_LOG_SHA=$(sha_file "$run_log")
  RUN_LOG_BYTES=$(byte_count "$run_log")
}

validate_close() {
  local close=$ATTEMPT_ROOT/bootstrap-close.txt
  validate_attempt_artifacts yes || return 1
  require_regular "$close" || return 1
  [[ $(wc -l < "$close" | tr -d '[:space:]') == 15 ]] || return 1
  [[ $(tail -c 1 "$close" | od -An -t u1 | tr -d '[:space:]') == 10 ]] || return 1
  mapfile -t CLOSE_LINES < "$close"
  [[ ${#CLOSE_LINES[@]} == 15 ]] || return 1
  local result_ref result_sha
  result_ref=docs/plans/mathdevmcp-real-document-remediation-phase-01-bootstrap-${ATTEMPT}-result-2026-07-11.md
  require_regular "$result_ref" || return 1
  result_sha=$(sha_file "$result_ref")
  [[ ${CLOSE_LINES[0]} == MATHDEVMCP_P01_BOOTSTRAP_CLOSE_V1 ]] || return 1
  [[ ${CLOSE_LINES[1]} == "bootstrap_attempt=$ATTEMPT" ]] || return 1
  [[ ${CLOSE_LINES[2]} == status=PASS ]] || return 1
  [[ ${CLOSE_LINES[3]} == "entry_implementation_manifest_sha256=$ENTRY_IMPLEMENTATION_SHA" ]] || return 1
  [[ ${CLOSE_LINES[4]} == "entry_protected_manifest_sha256=$ENTRY_PROTECTED_SHA" ]] || return 1
  [[ ${CLOSE_LINES[5]} == "prior_result_round_close_ref=$PRIOR_ROUND_CLOSE" ]] || return 1
  [[ ${CLOSE_LINES[6]} == "prior_result_round_close_sha256=$PRIOR_ROUND_CLOSE_SHA" ]] || return 1
  [[ ${CLOSE_LINES[7]} == "implementation_exit_manifest_sha256=$IMPLEMENTATION_EXIT_SHA" ]] || return 1
  [[ ${CLOSE_LINES[8]} == "bootstrap_command_ledger_sha256=$LEDGER_SHA" ]] || return 1
  [[ ${CLOSE_LINES[9]} == "bootstrap_log_sha256=$RUN_LOG_SHA" ]] || return 1
  [[ ${CLOSE_LINES[10]} == "bootstrap_log_byte_count=$RUN_LOG_BYTES" ]] || return 1
  [[ ${CLOSE_LINES[11]} == bootstrap_exit_code=0 ]] || return 1
  [[ ${CLOSE_LINES[12]} == "bootstrap_result_note_ref=$result_ref" ]] || return 1
  [[ ${CLOSE_LINES[13]} == "bootstrap_result_note_sha256=$result_sha" ]] || return 1
  [[ ${CLOSE_LINES[14]} == END ]] || return 1
  BOOTSTRAP_CLOSE_SHA=$(sha_file "$close")
  BOOTSTRAP_RESULT_REF=$result_ref
  BOOTSTRAP_RESULT_SHA=$result_sha
}

[[ $# -ge 1 ]] || { usage >&2; exit 2; }
MODE=$1
shift
case "$MODE" in run|close|verify) ;; *) usage >&2; exit 2 ;; esac

ATTEMPT=
ENTRY_ROOT=
ATTEMPT_ROOT=
PRIOR_ROUND_CLOSE=
SEEN_ATTEMPT=0
SEEN_ENTRY=0
SEEN_ATTEMPT_ROOT=0
SEEN_PRIOR=0
while [[ $# -gt 0 ]]; do
  [[ $# -ge 2 ]] || fail "option $1 requires a value"
  case "$1" in
    --attempt)
      [[ $SEEN_ATTEMPT == 0 ]] || fail 'duplicate --attempt'
      ATTEMPT=$2
      SEEN_ATTEMPT=1
      ;;
    --entry-root)
      [[ $SEEN_ENTRY == 0 ]] || fail 'duplicate --entry-root'
      ENTRY_ROOT=$2
      SEEN_ENTRY=1
      ;;
    --attempt-root)
      [[ $SEEN_ATTEMPT_ROOT == 0 ]] || fail 'duplicate --attempt-root'
      ATTEMPT_ROOT=$2
      SEEN_ATTEMPT_ROOT=1
      ;;
    --prior-round-close)
      [[ $SEEN_PRIOR == 0 ]] || fail 'duplicate --prior-round-close'
      PRIOR_ROUND_CLOSE=$2
      SEEN_PRIOR=1
      ;;
    *) fail "unknown option $1" ;;
  esac
  shift 2
done
[[ $SEEN_ATTEMPT == 1 && $SEEN_ENTRY == 1 && $SEEN_ATTEMPT_ROOT == 1 && $SEEN_PRIOR == 1 ]] || fail 'all four options are required exactly once'
[[ $ATTEMPT =~ ^b0[1-5]$ ]] || fail 'attempt must match b0[1-5]'
[[ $ENTRY_ROOT == "$P01_ROOT/entry" ]] || fail 'entry root is not the fixed P01 entry root'
[[ $ATTEMPT_ROOT == "$P01_ROOT/bootstrap-attempts/$ATTEMPT" ]] || fail 'attempt root does not match attempt id'
validate_relative_path "$ENTRY_ROOT" || fail 'entry root is not normalized'
validate_relative_path "$ATTEMPT_ROOT" || fail 'attempt root is not normalized'
validate_components_no_symlink "$ENTRY_ROOT" || fail 'entry root contains a symlink'
require_regular "$ENTRY_ROOT/implementation-entry-sha256.txt" || fail 'entry implementation manifest is unavailable'
require_regular "$ENTRY_ROOT/protected-dirty-sha256.txt" || fail 'entry protected manifest is unavailable'
ENTRY_IMPLEMENTATION_SHA=$(sha_file "$ENTRY_ROOT/implementation-entry-sha256.txt")
ENTRY_PROTECTED_SHA=$(head -n 11 "$ENTRY_ROOT/protected-dirty-sha256.txt" | sha256sum | cut -d ' ' -f 1)

if [[ $PRIOR_ROUND_CLOSE == NONE ]]; then
  PRIOR_ROUND_CLOSE_SHA=NONE
else
  [[ $PRIOR_ROUND_CLOSE =~ ^\.local/mathdevmcp/evidence/p01-20260711/result-rounds/rr0[1-4]/round-close\.json$ ]] || fail 'prior round close path is outside the fixed grammar'
  require_regular "$PRIOR_ROUND_CLOSE" || fail 'prior round close is unavailable or unsafe'
  PRIOR_ROUND_CLOSE_SHA=$(sha_file "$PRIOR_ROUND_CLOSE")
fi

case "$MODE" in
  run)
    [[ ! -e "$ATTEMPT_ROOT" && ! -L "$ATTEMPT_ROOT" ]] || fail 'attempt root already exists'
    mkdir -p -- "$P01_ROOT/bootstrap-attempts" || fail 'cannot create bootstrap-attempt parent'
    validate_components_no_symlink "$P01_ROOT/bootstrap-attempts" || fail 'bootstrap parent is unsafe'
    mkdir -- "$ATTEMPT_ROOT" || fail 'cannot allocate attempt root'
    mkdir -- "$ATTEMPT_ROOT/logs" || fail 'cannot allocate attempt logs'
    implementation_temp=$(mktemp "$ATTEMPT_ROOT/.implementation-exit.XXXXXX") || fail 'cannot allocate implementation temp'
    current_manifest "$implementation_temp"
    atomic_publish "$implementation_temp" "$ATTEMPT_ROOT/implementation-exit-sha256.txt" || fail 'cannot publish implementation manifest'

    IDS=()
    ARGV_SHAS=()
    STARTED=()
    ENDED=()
    WALLS=()
    EXITS=()
    STDOUT_REFS=()
    STDOUT_SHAS=()
    STDOUT_COUNTS=()
    STDERR_REFS=()
    STDERR_SHAS=()
    STDERR_COUNTS=()
    overall=0
    for number in 1 2 3 4; do
      set_command "$number" || fail 'internal command registry failure'
      printf -v tag '%02d' "$number"
      stdout_ref=logs/command-${tag}.stdout
      stderr_ref=logs/command-${tag}.stderr
      stdout_path=$ATTEMPT_ROOT/$stdout_ref
      stderr_path=$ATTEMPT_ROOT/$stderr_ref
      started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
      start_ns=$("$PYTHON" -c 'import time; print(time.monotonic_ns())')
      env PYTHONPATH=src "${COMMAND[@]}" > "$stdout_path" 2> "$stderr_path"
      exit_code=$?
      end_ns=$("$PYTHON" -c 'import time; print(time.monotonic_ns())')
      ended=$(date -u +%Y-%m-%dT%H:%M:%SZ)
      wall=$((end_ns - start_ns))
      fsync_file "$stdout_path"
      fsync_file "$stderr_path"
      IDS+=("$COMMAND_ID")
      ARGV_SHAS+=("$(argv_digest "${COMMAND[@]}")")
      STARTED+=("$started")
      ENDED+=("$ended")
      WALLS+=("$wall")
      EXITS+=("$exit_code")
      STDOUT_REFS+=("$stdout_ref")
      STDOUT_SHAS+=("$(sha_file "$stdout_path")")
      STDOUT_COUNTS+=("$(byte_count "$stdout_path")")
      STDERR_REFS+=("$stderr_ref")
      STDERR_SHAS+=("$(sha_file "$stderr_path")")
      STDERR_COUNTS+=("$(byte_count "$stderr_path")")
      [[ $exit_code == 0 ]] || overall=1
    done
    ledger_temp=$(mktemp "$ATTEMPT_ROOT/.bootstrap-command-ledger.XXXXXX") || fail 'cannot allocate ledger temp'
    {
      printf 'MATHDEVMCP_P01_BOOTSTRAP_LEDGER_V1\n'
      printf 'attempt=%s\n' "$ATTEMPT"
      printf 'entry_implementation_manifest_sha256=%s\n' "$ENTRY_IMPLEMENTATION_SHA"
      printf 'entry_protected_manifest_sha256=%s\n' "$ENTRY_PROTECTED_SHA"
      printf 'prior_round_close_ref=%s\n' "$PRIOR_ROUND_CLOSE"
      printf 'prior_round_close_sha256=%s\n' "$PRIOR_ROUND_CLOSE_SHA"
      printf 'command_count=4\n'
      for index in 0 1 2 3; do
        printf -v tag '%02d' "$((index + 1))"
        printf 'command_%s_id=%s\n' "$tag" "${IDS[$index]}"
        printf 'command_%s_argv_sha256=%s\n' "$tag" "${ARGV_SHAS[$index]}"
        printf 'command_%s_started_at_utc=%s\n' "$tag" "${STARTED[$index]}"
        printf 'command_%s_ended_at_utc=%s\n' "$tag" "${ENDED[$index]}"
        printf 'command_%s_wall_time_ns=%s\n' "$tag" "${WALLS[$index]}"
        printf 'command_%s_exit_code=%s\n' "$tag" "${EXITS[$index]}"
        printf 'command_%s_stdout_ref=%s\n' "$tag" "${STDOUT_REFS[$index]}"
        printf 'command_%s_stdout_sha256=%s\n' "$tag" "${STDOUT_SHAS[$index]}"
        printf 'command_%s_stdout_byte_count=%s\n' "$tag" "${STDOUT_COUNTS[$index]}"
        printf 'command_%s_stderr_ref=%s\n' "$tag" "${STDERR_REFS[$index]}"
        printf 'command_%s_stderr_sha256=%s\n' "$tag" "${STDERR_SHAS[$index]}"
        printf 'command_%s_stderr_byte_count=%s\n' "$tag" "${STDERR_COUNTS[$index]}"
      done
      printf 'END\n'
    } >| "$ledger_temp"
    atomic_publish "$ledger_temp" "$ATTEMPT_ROOT/bootstrap-command-ledger.txt" || fail 'cannot publish bootstrap ledger'
    run_temp=$(mktemp "$ATTEMPT_ROOT/.bootstrap-run.XXXXXX") || fail 'cannot allocate run-log temp'
    status=PASS
    [[ $overall == 0 ]] || status=FAIL
    {
      printf 'MATHDEVMCP_P01_BOOTSTRAP_RUN_V1\n'
      printf 'attempt=%s\n' "$ATTEMPT"
      printf 'bootstrap_pytest_exit=%s\n' "${EXITS[0]}"
      printf 'bootstrap_compile_exit=%s\n' "${EXITS[1]}"
      printf 'bootstrap_shell_syntax_exit=%s\n' "${EXITS[2]}"
      printf 'bootstrap_diff_exit=%s\n' "${EXITS[3]}"
      printf 'status=%s\n' "$status"
    } >| "$run_temp"
    atomic_publish "$run_temp" "$ATTEMPT_ROOT/bootstrap-run.log" || fail 'cannot publish bootstrap run log'
    validate_attempt_artifacts no || fail 'fresh bootstrap artifacts failed independent validation'
    printf 'bootstrap_attempt=%s status=%s ledger_sha256=%s\n' "$ATTEMPT" "$status" "$LEDGER_SHA"
    [[ $overall == 0 ]] || exit 1
    ;;
  close)
    [[ -d "$ATTEMPT_ROOT" && ! -L "$ATTEMPT_ROOT" ]] || fail 'attempt root is unavailable or unsafe'
    [[ ! -e "$ATTEMPT_ROOT/bootstrap-close.txt" && ! -L "$ATTEMPT_ROOT/bootstrap-close.txt" ]] || fail 'bootstrap close already exists'
    validate_attempt_artifacts yes || fail 'bootstrap attempt does not have a passing validated run'
    result_ref=docs/plans/mathdevmcp-real-document-remediation-phase-01-bootstrap-${ATTEMPT}-result-2026-07-11.md
    require_regular "$result_ref" || fail 'bootstrap result note is unavailable or unsafe'
    result_sha=$(sha_file "$result_ref")
    close_temp=$(mktemp "$ATTEMPT_ROOT/.bootstrap-close.XXXXXX") || fail 'cannot allocate close temp'
    {
      printf 'MATHDEVMCP_P01_BOOTSTRAP_CLOSE_V1\n'
      printf 'bootstrap_attempt=%s\n' "$ATTEMPT"
      printf 'status=PASS\n'
      printf 'entry_implementation_manifest_sha256=%s\n' "$ENTRY_IMPLEMENTATION_SHA"
      printf 'entry_protected_manifest_sha256=%s\n' "$ENTRY_PROTECTED_SHA"
      printf 'prior_result_round_close_ref=%s\n' "$PRIOR_ROUND_CLOSE"
      printf 'prior_result_round_close_sha256=%s\n' "$PRIOR_ROUND_CLOSE_SHA"
      printf 'implementation_exit_manifest_sha256=%s\n' "$IMPLEMENTATION_EXIT_SHA"
      printf 'bootstrap_command_ledger_sha256=%s\n' "$LEDGER_SHA"
      printf 'bootstrap_log_sha256=%s\n' "$RUN_LOG_SHA"
      printf 'bootstrap_log_byte_count=%s\n' "$RUN_LOG_BYTES"
      printf 'bootstrap_exit_code=0\n'
      printf 'bootstrap_result_note_ref=%s\n' "$result_ref"
      printf 'bootstrap_result_note_sha256=%s\n' "$result_sha"
      printf 'END\n'
    } >| "$close_temp"
    atomic_publish "$close_temp" "$ATTEMPT_ROOT/bootstrap-close.txt" || fail 'cannot publish bootstrap close'
    validate_close || fail 'published bootstrap close failed independent validation'
    printf 'bootstrap_attempt=%s status=PASS close_sha256=%s\n' "$ATTEMPT" "$BOOTSTRAP_CLOSE_SHA"
    ;;
  verify)
    [[ -d "$ATTEMPT_ROOT" && ! -L "$ATTEMPT_ROOT" ]] || fail 'attempt root is unavailable or unsafe'
    [[ ! -e "$ATTEMPT_ROOT/bootstrap-shell-verification.log" && ! -L "$ATTEMPT_ROOT/bootstrap-shell-verification.log" ]] || fail 'bootstrap shell verification already exists'
    validate_close || fail 'bootstrap close failed independent verification'
    verify_temp=$(mktemp "$ATTEMPT_ROOT/.bootstrap-shell-verification.XXXXXX") || fail 'cannot allocate verification temp'
    {
      printf 'MATHDEVMCP_P01_BOOTSTRAP_SHELL_VERIFICATION_V1\n'
      printf 'bootstrap_close_ref=%s/bootstrap-close.txt\n' "$ATTEMPT_ROOT"
      printf 'bootstrap_close_sha256=%s\n' "$BOOTSTRAP_CLOSE_SHA"
      printf 'bootstrap_command_ledger_ref=%s/bootstrap-command-ledger.txt\n' "$ATTEMPT_ROOT"
      printf 'bootstrap_command_ledger_sha256=%s\n' "$LEDGER_SHA"
      printf 'bootstrap_run_log_ref=%s/bootstrap-run.log\n' "$ATTEMPT_ROOT"
      printf 'bootstrap_run_log_sha256=%s\n' "$RUN_LOG_SHA"
      printf 'bootstrap_result_note_ref=%s\n' "$BOOTSTRAP_RESULT_REF"
      printf 'bootstrap_result_note_sha256=%s\n' "$BOOTSTRAP_RESULT_SHA"
      printf 'status=PASS\n'
    } >| "$verify_temp"
    atomic_publish "$verify_temp" "$ATTEMPT_ROOT/bootstrap-shell-verification.log" || fail 'cannot publish shell verification'
    printf 'bootstrap_attempt=%s status=PASS verification_sha256=%s\n' "$ATTEMPT" "$(sha_file "$ATTEMPT_ROOT/bootstrap-shell-verification.log")"
    ;;
esac
