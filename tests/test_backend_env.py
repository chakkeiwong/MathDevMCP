from concurrent.futures import ThreadPoolExecutor
import os

from mathdevmcp.backend_env import BackendConfig, backend_subprocess_env
from mathdevmcp.document_derivation_tree import _backend_env_scope
from mathdevmcp.math_document_rigor import _backend_env_scope as rigor_backend_env_scope


def test_request_backend_config_does_not_mutate_process_environment(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_BACKEND_CONDA_ENV", "process-env")
    monkeypatch.delenv("MATHDEVMCP_LEAN_TOOLCHAIN", raising=False)
    before = dict(os.environ)

    with _backend_env_scope("request-env") as config:
        assert config.conda_env == "request-env"
        assert config.lean_toolchain == "leanprover/lean4:v4.20.0"

    assert dict(os.environ) == before


def test_rigor_backend_config_does_not_invent_toolchain_default(monkeypatch):
    monkeypatch.delenv("MATHDEVMCP_LEAN_TOOLCHAIN", raising=False)

    with rigor_backend_env_scope("request-env") as config:
        assert config.conda_env == "request-env"
        assert config.lean_toolchain is None


def test_concurrent_backend_subprocess_environments_remain_distinct(monkeypatch):
    monkeypatch.setenv("PATH", "/usr/bin")
    configs = [
        BackendConfig(prefix=None, lean_toolchain="toolchain-a"),
        BackendConfig(prefix=None, lean_toolchain="toolchain-b"),
    ]

    with ThreadPoolExecutor(max_workers=2) as executor:
        environments = list(executor.map(backend_subprocess_env, configs))

    assert [env["ELAN_TOOLCHAIN"] for env in environments] == ["toolchain-a", "toolchain-b"]
    assert os.environ.get("ELAN_TOOLCHAIN") is None
