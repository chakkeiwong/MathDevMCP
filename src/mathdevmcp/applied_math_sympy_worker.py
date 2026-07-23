"""Fixed subprocess worker for bounded applied-math equality checks."""

from __future__ import annotations

import json
import re
import sys


_IDENTIFIER = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*\b")


def main() -> int:
    raw = sys.stdin.buffer.read(16_385)
    if len(raw) > 16_384:
        return 2
    try:
        request = json.loads(raw)
        if set(request) != {"lhs", "rhs"}:
            return 2
        lhs = request["lhs"]
        rhs = request["rhs"]
        if not isinstance(lhs, str) or not isinstance(rhs, str):
            return 2
        import sympy as sp
        from sympy.parsing.sympy_parser import parse_expr

        # Preserve denominator obligations before SymPy cancellation. A
        # symbolic denominator requires an explicit nonzero/domain condition.
        symbolic_division = any(
            re.search(r"/\s*[A-Za-z_(]", expression) for expression in (lhs, rhs)
        )

        identifiers = sorted(set(_IDENTIFIER.findall(lhs)) | set(_IDENTIFIER.findall(rhs)))
        local_dict = {name: sp.Symbol(name) for name in identifiers}
        left = parse_expr(lhs, local_dict=local_dict, evaluate=False)
        right = parse_expr(rhs, local_dict=local_dict, evaluate=False)
        left_denominator = sp.denom(sp.together(left))
        right_denominator = sp.denom(sp.together(right))
        denominators = sorted(
            {
                str(value)
                for value in (left_denominator, right_denominator)
                if value != 1
            }
        )
        if denominators or symbolic_division:
            result = {
                "status": "domain_conditions_required",
                "denominators": denominators,
                "sympy_version": sp.__version__,
            }
            payload = json.dumps(result, sort_keys=True, ensure_ascii=True).encode("utf-8")
            sys.stdout.buffer.write(payload[:16_384])
            return 0
        difference = sp.simplify(left - right)
        if difference == 0:
            result = {"status": "equivalent", "difference": "0", "sympy_version": sp.__version__}
        elif difference.is_number and difference != 0:
            result = {"status": "mismatch", "difference": str(difference), "sympy_version": sp.__version__}
        else:
            result = {"status": "unverified", "difference": str(difference), "sympy_version": sp.__version__}
        payload = json.dumps(result, sort_keys=True, ensure_ascii=True).encode("utf-8")
        if len(payload) > 16_384:
            return 3
        sys.stdout.buffer.write(payload)
        return 0
    except BaseException as exc:
        payload = json.dumps({"status": "error", "error_type": type(exc).__name__}).encode("utf-8")
        sys.stdout.buffer.write(payload[:16_384])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
