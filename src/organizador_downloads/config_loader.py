from pathlib import Path


def _normalize_extension(ext: str) -> str:
    cleaned = ext.strip().lower()
    if not cleaned:
        raise ValueError("Extensao vazia no mapeamento")
    if not cleaned.startswith("."):
        cleaned = f".{cleaned}"
    return cleaned


def _parse_simple_yaml(raw: str) -> dict[str, str]:
    """Parser minimo para YAML simples no formato `chave: valor`."""
    parsed: dict[str, str] = {}
    for line_no, raw_line in enumerate(raw.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            raise ValueError(f"YAML invalido na linha {line_no}: esperado 'chave: valor'")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Suporte intencionalmente restrito para evitar aceitar estruturas quebradas.
        if not key or not value:
            raise ValueError(f"YAML invalido na linha {line_no}: chave/valor vazio")
        if value.count("[") != value.count("]") or value.count("{") != value.count("}"):
            raise ValueError(f"YAML invalido na linha {line_no}: delimitadores desbalanceados")

        parsed[key] = value

    return parsed


def _load_raw_yaml(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")

    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        return _parse_simple_yaml(text)

    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML invalido em {path}: {exc}") from exc

    if not isinstance(loaded, dict):
        raise ValueError("Mapeamento de extensoes deve ser um objeto chave/valor")

    if not all(isinstance(k, str) for k in loaded.keys()):
        raise ValueError("YAML invalido: todas as chaves devem ser texto")
    if not all(isinstance(v, str) for v in loaded.values()):
        raise ValueError("YAML invalido: todos os valores devem ser texto")

    return loaded


def load_extension_map(path: Path) -> dict[str, str]:
    """Carrega e valida o arquivo YAML de mapeamento de extensoes."""
    try:
        content = _load_raw_yaml(path)
    except FileNotFoundError as exc:
        raise ValueError(f"Arquivo de configuracao nao encontrado: {path}") from exc

    normalized: dict[str, str] = {}
    for raw_ext, category in content.items():
        if not isinstance(raw_ext, str):
            raise ValueError(f"Extensao invalida no YAML: {raw_ext!r}")
        if not isinstance(category, str) or not category.strip():
            raise ValueError(f"Categoria invalida para {raw_ext!r}")
        normalized[_normalize_extension(raw_ext)] = category.strip()

    return normalized
