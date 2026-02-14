from pathlib import Path

from organizador_downloads.file_ops import move_file, resolve_unique_destination


def test_resolve_unique_destination_suffix(tmp_path: Path) -> None:
    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()

    first = dest_dir / "arquivo.txt"
    first.write_text("a", encoding="utf-8")

    second = dest_dir / "arquivo_1.txt"
    second.write_text("b", encoding="utf-8")

    resolved = resolve_unique_destination(dest_dir, "arquivo.txt")

    assert resolved.name == "arquivo_2.txt"


def test_move_file_dry_run_does_not_move(tmp_path: Path) -> None:
    src = tmp_path / "origem.txt"
    src.write_text("conteudo", encoding="utf-8")
    dst = tmp_path / "dest" / "origem.txt"

    ok, message = move_file(src, dst, dry_run=True)

    assert ok is True
    assert message == "dry-run"
    assert src.exists()
    assert not dst.exists()
