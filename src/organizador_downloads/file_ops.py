from pathlib import Path
import shutil


def resolve_unique_destination(dest_dir: Path, filename: str) -> Path:
    """Retorna um caminho unico, adicionando sufixo incremental quando necessario."""
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate

    original = Path(filename)
    counter = 1
    while True:
        candidate = dest_dir / f"{original.stem}_{counter}{original.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def move_file(src: Path, dst: Path, dry_run: bool) -> tuple[bool, str | None]:
    """Move o arquivo ou simula o movimento."""
    if dry_run:
        return True, "dry-run"

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return True, None
    except Exception as exc:  # pragma: no cover
        return False, str(exc)


def remove_empty_dirs(root: Path) -> int:
    """Remove diretorios vazios dentro de root de baixo para cima."""
    if not root.exists() or not root.is_dir():
        return 0

    removed = 0
    for item in sorted(root.rglob("*"), reverse=True):
        if item.is_dir():
            try:
                next(item.iterdir())
            except StopIteration:
                item.rmdir()
                removed += 1
            except OSError:
                continue

    try:
        next(root.iterdir())
    except StopIteration:
        root.rmdir()
        removed += 1
    except OSError:
        pass

    return removed
