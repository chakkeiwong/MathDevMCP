from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from pathlib import Path

from .contracts import attach_contract


@dataclass(frozen=True)
class AstOperationNode:
    id: str
    kind: str
    operation: str
    target: str | None
    expression: str
    line: int
    column: int
    evidence: dict


@dataclass(frozen=True)
class AstOperationGraph:
    status: str
    reason: str
    source_path: str | None
    operations: list[str]
    nodes: list[dict]
    diagnostics: list[dict]


_LOGDET_NAMES = {"slogdet", "logdet"}
_SOLVE_NAMES = {"solve", "inv", "inverse"}
_CHOLESKY_NAMES = {"cholesky", "chol"}
_GRADIENT_NAMES = {"grad", "value_and_grad", "jacobian", "jacfwd", "jacrev"}
_LOGSUMEXP_NAMES = {"logsumexp"}
_VECTORIZE_NAMES = {"vmap", "scan"}


def _unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return node.__class__.__name__


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Call):
        return _call_name(node.func)
    return ""


def _short_call_name(node: ast.AST) -> str:
    name = _call_name(node)
    return name.rsplit(".", 1)[-1]


def _target_names(target: ast.AST) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, ast.Attribute):
        return [_unparse(target)]
    if isinstance(target, ast.Tuple | ast.List):
        names: list[str] = []
        for elt in target.elts:
            names.extend(_target_names(elt))
        return names
    if isinstance(target, ast.Subscript):
        return [_unparse(target)]
    return []


def _name_contains(name: str, fragments: tuple[str, ...]) -> bool:
    lowered = name.lower()
    return any(fragment in lowered for fragment in fragments)


def _classify_call(node: ast.Call) -> set[str]:
    operations: set[str] = {"call"}
    short = _short_call_name(node.func).lower()
    full = _call_name(node.func).lower()
    if short in _LOGDET_NAMES or "slogdet" in full or "logdet" in full:
        operations.add("logdet")
    if short in _SOLVE_NAMES or full.endswith("linalg.solve") or full.endswith("linalg.inv"):
        operations.add("inverse_or_solve")
    if short in _CHOLESKY_NAMES or "cholesky" in full:
        operations.add("cholesky")
    if short in _GRADIENT_NAMES or full.endswith(".grad") or "value_and_grad" in full:
        operations.add("gradient")
    if short in _LOGSUMEXP_NAMES or "logsumexp" in full:
        operations.add("logsumexp")
        operations.add("particle_normalization")
    if short in _VECTORIZE_NAMES or full.endswith(".scan") or full.endswith(".vmap"):
        operations.add("vectorized_loop")
        if short == "scan" or full.endswith(".scan"):
            operations.add("scan_loop")
    if "log_prob" in full or "log_likelihood" in full or "logposterior" in full or "log_posterior" in full:
        operations.add("posterior_or_likelihood")
    if short in {"dot", "einsum", "matmul"}:
        operations.add("quadratic_form")
    return operations


def _has_matmul(node: ast.AST) -> bool:
    return any(isinstance(child, ast.BinOp) and isinstance(child.op, ast.MatMult) for child in ast.walk(node))


def _classify_assignment(targets: list[str], value: ast.AST) -> set[str]:
    operations: set[str] = {"assignment"}
    expression = _unparse(value).lower()
    target_text = " ".join(targets).lower()
    all_text = f"{target_text} {expression}"
    if _has_matmul(value):
        operations.add("matmul")
        operations.add("quadratic_form")
    if _name_contains(all_text, ("pred", "prior", "forecast")) and _name_contains(all_text, ("x", "state", "mean", "p_", "cov", "sigma")):
        operations.add("prediction_update")
    if _name_contains(all_text, ("innov", "resid", "innovation", " y ", "v_")):
        operations.add("innovation_update")
    if _name_contains(target_text, ("s", "innov_cov", "innovation_cov", "resid_cov")) and _name_contains(expression, ("h", "z", "obs", "p_pred", "r")):
        operations.add("innovation_covariance")
    if _name_contains(target_text, ("k", "gain")) or _name_contains(all_text, ("kalman_gain", "gain")):
        operations.add("kalman_gain")
    if _name_contains(target_text, ("x", "state", "mean")) and _name_contains(expression, ("innov", "resid", "gain", " k ")):
        operations.add("state_update")
    if _name_contains(target_text, ("p", "cov", "sigma")) and _name_contains(expression, ("gain", " k", "p_pred", "cov_pred", "sigma_pred")):
        operations.add("covariance_update")
    if _name_contains(all_text, ("grad", "nabla", "score", "jacobian")):
        operations.add("gradient")
    if _name_contains(all_text, ("log_prob", "logp", "log_post", "logpost", "log_likelihood", "likelihood")):
        operations.add("posterior_or_likelihood")
    if _name_contains(target_text, ("p_half", "momentum", "theta_next", "p_next")) and _name_contains(all_text, ("step_size", "grad", "mass_inv", "momentum")):
        operations.add("leapfrog_update")
    if _name_contains(all_text, ("hamiltonian", "potential_energy", "kinetic_energy")):
        operations.add("hamiltonian_energy")
    if _name_contains(all_text, ("logsumexp", "normalizer", "normalized_log_weights", "log_weight")):
        operations.add("particle_normalization")
    if _name_contains(all_text, ("expectation", "expected_", "e_t", "mean(")):
        operations.add("expectation")
    if _name_contains(all_text, ("euler_residual", "sdf", "stochastic_discount", "discount_factor")):
        operations.add("euler_residual")
    if _name_contains(all_text, ("dt", "step_size", "time_step", "euler_maruyama", "next_state", "x_next", "u_next")):
        operations.add("time_step_update")
    if _name_contains(all_text, ("stability", "cfl", "dt_max", "stable_step")):
        operations.add("stability_condition")
    if _name_contains(all_text, ("acceptance_ratio", "log_accept", "metropolis", "accept_prob")):
        operations.add("acceptance_ratio")
    if _name_contains(all_text, ("elbo", "entropy", "kl", "variational")):
        operations.add("elbo_objective")
    if _name_contains(all_text, ("reparameter", "epsilon", "eps", "z_sample")):
        operations.add("reparameterization_gradient")
    if _name_contains(all_text, ("vmap", "scan", "lax.scan")):
        operations.add("vectorized_loop")
    if ".shape" in expression or ".shape" in target_text:
        operations.add("shape_reference")
    return operations


def _classify_compare(node: ast.Compare) -> set[str]:
    expression = _unparse(node).lower()
    if ".shape" in expression or "len(" in expression:
        return {"shape_guard"}
    return set()


def _classify_assert(node: ast.Assert) -> set[str]:
    operations = {"assertion"}
    operations.update(_classify_compare(node.test) if isinstance(node.test, ast.Compare) else set())
    expression = _unparse(node.test).lower()
    if ".shape" in expression or "symmetric" in expression or "positive" in expression or "cholesky" in expression:
        operations.add("shape_guard")
    if "symmetric" in expression or "positive" in expression or "cholesky" in expression:
        operations.add("covariance_guard")
    return operations


class _OperationVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.nodes: list[AstOperationNode] = []

    def _add_node(self, node: ast.AST, kind: str, operations: set[str], target: str | None, expression: str, evidence: dict) -> None:
        for operation in sorted(operations):
            node_id = f"{getattr(node, 'lineno', 0)}:{getattr(node, 'col_offset', 0)}:{kind}:{operation}:{len(self.nodes)}"
            self.nodes.append(
                AstOperationNode(
                    id=node_id,
                    kind=kind,
                    operation=operation,
                    target=target,
                    expression=expression,
                    line=getattr(node, "lineno", 0),
                    column=getattr(node, "col_offset", 0),
                    evidence=evidence,
                )
            )

    def visit_Assign(self, node: ast.Assign) -> None:
        targets = [name for target in node.targets for name in _target_names(target)]
        operations = _classify_assignment(targets, node.value)
        self._add_node(node, "assign", operations, ", ".join(targets) or None, _unparse(node.value), {"targets": targets})
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        targets = _target_names(node.target)
        operations = _classify_assignment(targets, node.value) if node.value is not None else {"assignment"}
        self._add_node(node, "assign", operations, ", ".join(targets) or None, _unparse(node.value), {"targets": targets, "annotation": _unparse(node.annotation)})
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        targets = _target_names(node.target)
        operations = _classify_assignment(targets, node.value)
        operations.add("augmented_assignment")
        self._add_node(node, "aug_assign", operations, ", ".join(targets) or None, _unparse(node.value), {"targets": targets, "operator": node.op.__class__.__name__})
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        operations = {"return"}
        if node.value is not None and _has_matmul(node.value):
            operations.update({"matmul", "quadratic_form"})
        self._add_node(node, "return", operations, None, _unparse(node.value), {})
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self._add_node(node, "call", _classify_call(node), None, _unparse(node), {"function": _call_name(node.func)})
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if isinstance(node.op, ast.MatMult):
            self._add_node(node, "binop", {"matmul", "quadratic_form"}, None, _unparse(node), {"operator": "MatMult"})
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self._add_node(node, "loop", {"loop"}, _unparse(node.target), _unparse(node.iter), {})
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self._add_node(node, "assert", _classify_assert(node), None, _unparse(node.test), {"message": _unparse(node.msg)})
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        operations = _classify_compare(node)
        if operations:
            self._add_node(node, "compare", operations, None, _unparse(node), {})
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        self._add_node(node, "subscript", {"subscript"}, None, _unparse(node), {})
        self.generic_visit(node)


def build_ast_operation_graph(source_text: str, *, source_path: str | None = None) -> dict:
    try:
        tree = ast.parse(source_text, filename=source_path or "<memory>")
    except SyntaxError as exc:
        return attach_contract(
            asdict(
                AstOperationGraph(
                    status="inconclusive",
                    reason="Python source could not be parsed into an AST.",
                    source_path=source_path,
                    operations=[],
                    nodes=[],
                    diagnostics=[
                        {
                            "kind": "python_syntax_error",
                            "message": exc.msg,
                            "line": exc.lineno,
                            "column": exc.offset,
                        }
                    ],
                )
            ),
            "ast_operation_graph",
        )
    visitor = _OperationVisitor()
    visitor.visit(tree)
    nodes = [asdict(node) for node in visitor.nodes]
    operations = sorted({node["operation"] for node in nodes})
    result = AstOperationGraph(
        status="consistent" if nodes else "inconclusive",
        reason="AST operation graph extracted from Python source." if nodes else "No auditable Python operations were found.",
        source_path=source_path,
        operations=operations,
        nodes=nodes,
        diagnostics=[],
    )
    return attach_contract(asdict(result), "ast_operation_graph")


def build_ast_operation_graph_for_file(path: str | Path) -> dict:
    source_path = str(Path(path))
    source_text = Path(path).read_text(encoding="utf-8")
    return build_ast_operation_graph(source_text, source_path=source_path)
