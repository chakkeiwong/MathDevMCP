import pytest

from mathdevmcp.artifact_storage import write_bytes_no_replace
from mathdevmcp.backend_protocol import execute_backend


class FakeBackend:
    def execute(self, request):
        return {"status": "diagnostic", "request": dict(request)}


def test_backend_protocol_accepts_injected_mapping_without_backend_import() -> None:
    assert execute_backend(FakeBackend(), {"id": "x"}) == {"status": "diagnostic", "request": {"id": "x"}}


def test_backend_protocol_rejects_non_mapping_result() -> None:
    class BadBackend:
        def execute(self, request):
            return [request]

    with pytest.raises(TypeError, match="mapping"):
        execute_backend(BadBackend(), {})


def test_shared_artifact_writer_is_no_overwrite(tmp_path):
    destination = tmp_path / "nested" / "record.json"
    write_bytes_no_replace(destination, b"same")
    write_bytes_no_replace(destination, b"same")
    with pytest.raises(ValueError, match="collision"):
        write_bytes_no_replace(destination, b"different")


def test_shared_artifact_writer_rejects_symlink_parent(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    link = tmp_path / "link"
    link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="real directory"):
        write_bytes_no_replace(link / "record.json", b"secret")
    assert not (outside / "record.json").exists()


def test_shared_artifact_writer_cleans_short_write(monkeypatch, tmp_path):
    import mathdevmcp.artifact_storage as storage

    destination = tmp_path / "record.json"
    monkeypatch.setattr(storage.os, "write", lambda _fd, _payload: 0)
    with pytest.raises(OSError, match="short artifact write"):
        write_bytes_no_replace(destination, b"secret")
    assert not destination.exists()


def test_safe_generated_writer_replaces_symlink_without_following_target(tmp_path):
    from mathdevmcp.artifact_storage import write_bytes_safe

    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    link = tmp_path / "report.md"
    link.symlink_to(outside)
    write_bytes_safe(link, b"inside")
    assert link.read_bytes() == b"inside"
    assert outside.read_text(encoding="utf-8") == "outside"
