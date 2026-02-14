from pathlib import Path

from organizador_downloads.organizer import run
from organizador_downloads.reporting import setup_logger


def test_run_two_phases_and_cleanup(tmp_path: Path) -> None:
    base = tmp_path / "Downloads"
    base.mkdir()

    mapping = {
        ".txt": "Arquivos em TXT",
        ".pdf": "Arquivos em PDF",
    }

    # fase 1 (Outros recursivo)
    outros = base / "Outros"
    nested = outros / "sub"
    nested.mkdir(parents=True)
    (nested / "a.txt").write_text("ok", encoding="utf-8")
    (nested / "x.abc").write_text("other", encoding="utf-8")

    # fase 2 (raiz)
    (base / "b.pdf").write_text("pdf", encoding="utf-8")

    log = tmp_path / "run.log"
    logger = setup_logger(log, quiet=True)

    report = run(
        base_path=base,
        dry_run=False,
        quiet=True,
        log_file=log,
        extension_map=mapping,
        logger=logger,
    )

    assert (base / "Arquivos em TXT" / "a.txt").exists()
    assert (base / "Outros" / "x.abc").exists()
    assert (base / "Arquivos em PDF" / "b.pdf").exists()

    # subpasta vazia de Outros deve ser removida
    assert not (base / "Outros" / "sub").exists()

    # todos arquivos validos foram processados
    assert report.total_scanned == 3
    assert report.total_moved == 3
    assert report.total_errors == 0


def test_run_dry_run_does_not_change_files(tmp_path: Path) -> None:
    base = tmp_path / "Downloads"
    base.mkdir()
    (base / "a.txt").write_text("txt", encoding="utf-8")

    mapping = {".txt": "Arquivos em TXT"}
    log = tmp_path / "run.log"
    logger = setup_logger(log, quiet=True)

    report = run(
        base_path=base,
        dry_run=True,
        quiet=True,
        log_file=log,
        extension_map=mapping,
        logger=logger,
    )

    assert (base / "a.txt").exists()
    assert not (base / "Arquivos em TXT").exists()
    assert report.total_scanned == 1
    assert report.total_moved == 1
