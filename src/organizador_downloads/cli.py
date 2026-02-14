from argparse import ArgumentParser
from pathlib import Path

from .config_loader import load_extension_map
from .organizer import run
from .reporting import setup_logger

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "extension_map.yaml"


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Organiza arquivos por extensao")
    parser.add_argument("path", nargs="?", help="Caminho da pasta a organizar")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem mover arquivos")
    parser.add_argument(
        "--log-file",
        default="logs/organizar_downloads.log",
        help="Arquivo de log (padrao: logs/organizar_downloads.log)",
    )
    parser.add_argument("--quiet", action="store_true", help="Reduz saida no console")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    raw_path = args.path
    if not raw_path:
        raw_path = input("Digite o caminho da pasta que deseja organizar: ").strip().strip('"')

    base_path = Path(raw_path)
    log_file = Path(args.log_file)

    try:
        extension_map = load_extension_map(DEFAULT_CONFIG_PATH)
        logger = setup_logger(log_file=log_file, quiet=args.quiet)
        report = run(
            base_path=base_path,
            dry_run=args.dry_run,
            quiet=args.quiet,
            log_file=log_file,
            extension_map=extension_map,
            logger=logger,
        )
    except ValueError as exc:
        print(f"Erro de validacao: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Erro inesperado: {exc}")
        return 2

    if not args.quiet:
        print(
            f"Concluido. Varridos={report.total_scanned} "
            f"Movidos={report.total_moved} "
            f"Pulados={report.total_skipped} "
            f"Erros={report.total_errors}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
