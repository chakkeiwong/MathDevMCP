from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import time
from typing import Callable

from .contracts import attach_contract


@dataclass(frozen=True)
class NumericRunnerResult:
    status: str
    reason: str
    diagnostic: str
    evidence: dict


def _finish(status: str, reason: str, diagnostic: str, evidence: dict) -> dict:
    return attach_contract(asdict(NumericRunnerResult(status, reason, diagnostic, evidence)), "numeric_diagnostic_result")


def _elapsed(started: float) -> float:
    return time.perf_counter() - started


def _is_square(matrix: list[list[float]]) -> bool:
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)


def _cholesky(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    chol = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = matrix[i][j] - sum(chol[i][k] * chol[j][k] for k in range(j))
            if i == j:
                if value <= 0:
                    raise ValueError("matrix is not positive definite")
                chol[i][j] = math.sqrt(value)
            else:
                chol[i][j] = value / chol[j][j]
    return chol


def check_logdet_domain(matrix: list[list[float]], *, timeout_seconds: float = 1.0) -> dict:
    started = time.perf_counter()
    if _elapsed(started) > timeout_seconds:
        return _finish("inconclusive", "Numeric diagnostic timed out before execution.", "logdet_domain_check", {"timeout_seconds": timeout_seconds})
    if not _is_square(matrix):
        return _finish("mismatch", "Log determinant input is not square.", "logdet_domain_check", {"shape": [len(matrix), len(matrix[0]) if matrix else 0]})
    try:
        chol = _cholesky(matrix)
    except ValueError as exc:
        return _finish("mismatch", str(exc), "logdet_domain_check", {"shape": [len(matrix), len(matrix)], "positive_definite": False})
    logdet = 2.0 * sum(math.log(chol[i][i]) for i in range(len(chol)))
    return _finish(
        "verified",
        "Matrix passed a Cholesky-based positive-definite logdet domain check.",
        "logdet_domain_check",
        {"shape": [len(matrix), len(matrix)], "positive_definite": True, "logdet": logdet, "elapsed_seconds": _elapsed(started)},
    )


def _gaussian_solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(matrix)
    augmented = [list(row) + [float(vector[i])] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            raise ValueError("linear system is singular or ill-conditioned")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            augmented[row] = [value - factor * augmented[col][idx] for idx, value in enumerate(augmented[row])]
    return [row[-1] for row in augmented]


def check_solve_residual(matrix: list[list[float]], vector: list[float], *, tolerance: float = 1e-8, timeout_seconds: float = 1.0) -> dict:
    started = time.perf_counter()
    if not _is_square(matrix) or len(vector) != len(matrix):
        return _finish("inconclusive", "Solve residual check requires an n by n matrix and n-vector.", "linear_solve_residual_check", {"shape": [len(matrix), len(matrix[0]) if matrix else 0], "vector_length": len(vector)})
    if len(matrix) > 8:
        return _finish("inconclusive", "Solve residual check refuses inputs larger than 8 by 8.", "linear_solve_residual_check", {"shape": [len(matrix), len(matrix)]})
    if _elapsed(started) > timeout_seconds:
        return _finish("inconclusive", "Numeric diagnostic timed out before execution.", "linear_solve_residual_check", {"timeout_seconds": timeout_seconds})
    try:
        solution = _gaussian_solve(matrix, vector)
    except ValueError as exc:
        return _finish("mismatch", str(exc), "linear_solve_residual_check", {"shape": [len(matrix), len(matrix)]})
    residual = [
        sum(matrix[i][j] * solution[j] for j in range(len(solution))) - vector[i]
        for i in range(len(matrix))
    ]
    residual_norm = math.sqrt(sum(value * value for value in residual))
    status = "verified" if residual_norm <= tolerance else "mismatch"
    reason = "Linear solve residual is within tolerance." if status == "verified" else "Linear solve residual exceeds tolerance."
    return _finish(
        status,
        reason,
        "linear_solve_residual_check",
        {"solution": solution, "residual_norm": residual_norm, "tolerance": tolerance, "elapsed_seconds": _elapsed(started)},
    )


def check_finite_difference_gradient(
    func: Callable[[float], float] | None,
    grad: Callable[[float], float] | None,
    point: float,
    *,
    step: float = 1e-5,
    tolerance: float = 1e-4,
) -> dict:
    if func is None or grad is None:
        return _finish("inconclusive", "Finite-difference gradient check requires explicit callable encodings.", "finite_difference_gradient_check", {})
    numerical = (func(point + step) - func(point - step)) / (2.0 * step)
    analytic = grad(point)
    error = abs(numerical - analytic)
    status = "verified" if error <= tolerance else "mismatch"
    reason = "Analytic gradient matches finite differences within tolerance." if status == "verified" else "Analytic gradient differs from finite differences."
    return _finish(
        status,
        reason,
        "finite_difference_gradient_check",
        {"point": point, "numerical": numerical, "analytic": analytic, "absolute_error": error, "tolerance": tolerance},
    )
