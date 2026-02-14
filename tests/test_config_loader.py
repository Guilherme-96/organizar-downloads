from pathlib import Path

from organizador_downloads.config_loader import load_extension_map


def test_load_extension_map_normalizes_extensions(tmp_path: Path) -> None:
    config = tmp_path / "map.yaml"
    config.write_text("JPG: Imagens\n.pdf: Arquivos em PDF\n", encoding="utf-8")

    mapping = load_extension_map(config)

    assert mapping[".jpg"] == "Imagens"
    assert mapping[".pdf"] == "Arquivos em PDF"


def test_load_extension_map_invalid_yaml(tmp_path: Path) -> None:
    config = tmp_path / "bad.yaml"
    config.write_text("x: [1, 2", encoding="utf-8")

    try:
        load_extension_map(config)
        assert False, "Era esperado ValueError para YAML invalido"
    except ValueError as exc:
        assert "YAML invalido" in str(exc)
