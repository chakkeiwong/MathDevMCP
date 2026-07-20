#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 PDF OUTPUT_DIR [FIRST_PAGE] [LAST_PAGE]" >&2
}

if [[ $# -lt 2 || $# -gt 4 ]]; then
  usage
  exit 2
fi

pdf=$1
output_dir=$2
first=${3:-1}

if [[ ! -f "$pdf" ]]; then
  echo "PDF not found: $pdf" >&2
  exit 1
fi

for command in pdfinfo pdftoppm pdftotext; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command" >&2
    exit 1
  fi
done

pages=$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2}')
if [[ -z "$pages" ]]; then
  echo "Could not determine PDF page count" >&2
  exit 1
fi

last=${4:-$((first + 11))}
if (( first < 1 || last < first || first > pages )); then
  echo "Invalid page range: $first-$last for $pages-page PDF" >&2
  exit 1
fi
if (( last > pages )); then
  last=$pages
fi

mkdir -p "$output_dir"
pdftoppm -f "$first" -l "$last" -jpeg -r 120 "$pdf" "$output_dir/page"
pdftotext -f "$first" -l "$last" -layout "$pdf" "$output_dir/extracted-pages.txt"
pdfinfo "$pdf" > "$output_dir/pdfinfo.txt"

if command -v montage >/dev/null 2>&1; then
  shopt -s nullglob
  images=("$output_dir"/page-*.jpg)
  if (( ${#images[@]} > 0 )); then
    montage "${images[@]}" -thumbnail 500x650 -tile 2x -geometry +12+12 \
      "$output_dir/contact-sheet.jpg"
  fi
fi

echo "Rendered pages $first-$last of $pages into $output_dir"
