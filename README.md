# Organizador de Downloads

Projeto modular para organizar arquivos por extensão.

## Execução

```bash
python -m organizador_downloads.cli [path] [--dry-run] [--log-file logs/organizar_downloads.log] [--quiet]
```

Se `path` não for informado, o CLI solicita o caminho via prompt.

## Exemplos

```bash
python -m organizador_downloads.cli "C:\\Users\\seu_usuario\\Downloads"
python -m organizador_downloads.cli "C:\\Users\\seu_usuario\\Downloads" --dry-run
```

## Testes

```bash
pytest
```
