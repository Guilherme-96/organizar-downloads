from pathlib import Path
import logging

from .file_ops import move_file, remove_empty_dirs, resolve_unique_destination
from .models import MoveAction, RunReport

DEFAULT_CATEGORY = "Outros"


def _move_single_file(
    file_path: Path,
    base_path: Path,
    extension_map: dict[str, str],
    report: RunReport,
    logger: logging.Logger,
    dry_run: bool,
) -> None:
    if file_path.is_dir():
        return

    category = extension_map.get(file_path.suffix.lower(), DEFAULT_CATEGORY)
    dest_dir = base_path / category
    destination = resolve_unique_destination(dest_dir, file_path.name)

    ok, message = move_file(file_path, destination, dry_run=dry_run)
    status = "moved" if ok else "error"

    report.add_action(
        MoveAction(
            source=file_path,
            destination=destination,
            category=category,
            status=status,
            message=message,
        )
    )

    if ok:
        logger.info(f"Movido: {file_path} -> {destination}")
    else:
        logger.error(f"Erro ao mover {file_path}: {message}")


def run(
    base_path: Path,
    dry_run: bool,
    quiet: bool,
    log_file: Path,
    extension_map: dict[str, str],
    logger: logging.Logger | None = None,
) -> RunReport:
    """Executa a organizacao preservando o fluxo de 2 fases."""
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(f"O caminho '{base_path}' nao existe ou nao e uma pasta valida.")

    report = RunReport()
    active_logger = logger or logging.getLogger("organizador_downloads")

    # Fase 1: processar Outros recursivamente
    others_dir = base_path / DEFAULT_CATEGORY
    if others_dir.exists() and others_dir.is_dir():
        for item in list(others_dir.rglob("*")):
            _move_single_file(
                item,
                base_path,
                extension_map,
                report,
                active_logger,
                dry_run,
            )
        if not dry_run:
            remove_empty_dirs(others_dir)

    categories = set(extension_map.values()) | {DEFAULT_CATEGORY}

    # Fase 2: processar somente a raiz
    for item in list(base_path.iterdir()):
        if item.is_dir() and item.name in categories:
            continue
        _move_single_file(
            item,
            base_path,
            extension_map,
            report,
            active_logger,
            dry_run,
        )

    active_logger.info(
        "Resumo | varridos=%s movidos=%s pulados=%s erros=%s",
        report.total_scanned,
        report.total_moved,
        report.total_skipped,
        report.total_errors,
    )

    return report
