from mathdevmcp.math_normalization import normalize_math_text, normalize_math_tokens


def test_normalize_math_text_handles_plain_and_latex_function_notation():
    assert normalize_math_text(r"\log \pi(u) + \logdet") == "logpiu+logdet"
    assert normalize_math_text("log pi(u) + logdet") == "logpiu+logdet"


def test_normalize_math_text_handles_unicode_pi():
    assert normalize_math_text("log π(u)") == "logpiu"


def test_normalize_math_tokens_splits_compact_expression_boundaries():
    assert normalize_math_tokens("def transformed_density(log_pi): return log_pi") == "def transformed_density log_pi  return log_pi"
