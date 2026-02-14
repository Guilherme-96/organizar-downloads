from pathlib import Path
import shutil

caminho_input = input("Digite o caminho da pasta que deseja organizar: ").strip().strip('"')
caminho = Path(caminho_input)

if not caminho.exists() or not caminho.is_dir():
    print(f"Erro: O caminho '{caminho}' não existe ou não é uma pasta válida.")
    exit()

# Dicionário de mapeamento: extensão -> pasta de destino
mapeamento_extensoes = {
    # Imagens
    '.jpg': 'Imagens',
    '.jpeg': 'Imagens',
    '.png': 'Imagens',
    '.gif': 'Imagens',
    '.bmp': 'Imagens',
    '.svg': 'Imagens',
    '.ico': 'Imagens',
    '.webp': 'Imagens',

    # Excel
    '.xlsx': 'Arquivos em Excel',
    '.xlsm': 'Arquivos em Excel',
    '.xls': 'Arquivos em Excel',
    '.xlsb': 'Arquivos em Excel',

    # PDF
    '.pdf': 'Arquivos em PDF',

    # CSV
    '.csv': 'Arquivos em CSV',

    # HTML
    '.html': 'Arquivos em HTML',
    '.htm': 'Arquivos em HTML',

    # TXT
    '.txt': 'Arquivos em TXT',

    # Word
    '.doc': 'Arquivos em Word',
    '.docx': 'Arquivos em Word',

    # PowerPoint
    '.ppt': 'Arquivos em PowerPoint',
    '.pptx': 'Arquivos em PowerPoint',

    # Compactados
    '.zip': 'Arquivos Compactados',
    '.rar': 'Arquivos Compactados',
    '.7z': 'Arquivos Compactados',
    '.tar': 'Arquivos Compactados',
    '.gz': 'Arquivos Compactados',

    # Vídeos
    '.mp4': 'Vídeos',
    '.avi': 'Vídeos',
    '.mkv': 'Vídeos',
    '.mov': 'Vídeos',
    '.wmv': 'Vídeos',
    '.flv': 'Vídeos',
    '.webm': 'Vídeos',

    # Áudios
    '.mp3': 'Áudios',
    '.wav': 'Áudios',
    '.flac': 'Áudios',
    '.aac': 'Áudios',
    '.ogg': 'Áudios',
    '.m4a': 'Áudios',

    # Executáveis
    '.exe': 'Executáveis',
    '.msi': 'Executáveis',

    # Scripts
    '.py': 'Scripts',
    '.js': 'Scripts',
    '.java': 'Scripts',
    '.cpp': 'Scripts',
    '.c': 'Scripts',
    '.sh': 'Scripts',
    '.bat': 'Scripts',
}

def organizar_arquivo(arquivo, caminho_base):
    """Organiza um arquivo movendo-o para a pasta apropriada"""
    if arquivo.is_dir():
        return False

    extensao = arquivo.suffix.lower()

    # Determina a pasta de destino
    pasta_destino = mapeamento_extensoes.get(extensao, 'Outros')

    # Cria a pasta de destino se não existir
    caminho_destino = caminho_base / pasta_destino
    caminho_destino.mkdir(exist_ok=True)

    # Move o arquivo
    destino_final = caminho_destino / arquivo.name

    # Se já existir um arquivo com o mesmo nome, adiciona um número
    contador = 1
    while destino_final.exists():
        nome_base = arquivo.stem
        extensao_arquivo = arquivo.suffix
        destino_final = caminho_destino / f"{nome_base}_{contador}{extensao_arquivo}"
        contador += 1

    shutil.move(str(arquivo), str(destino_final))
    return True

print("Iniciando organização dos arquivos...")

# ETAPA 1: Processar arquivos da pasta "Outros" (recursivamente)
pasta_outros = caminho / 'Outros'
if pasta_outros.exists() and pasta_outros.is_dir():
    print("\nProcessando arquivos da pasta 'Outros' (incluindo subpastas)...")

    # Usar rglob para pegar todos os arquivos recursivamente
    todos_arquivos = list(pasta_outros.rglob('*'))
    contador_outros = 0

    for arquivo in todos_arquivos:
        try:
            if organizar_arquivo(arquivo, caminho):
                contador_outros += 1
                # Mostra o caminho relativo para facilitar identificação
                caminho_relativo = arquivo.relative_to(pasta_outros)
                print(f"  Movido: {caminho_relativo}")
        except Exception as e:
            print(f"  Erro ao processar {arquivo.name}: {e}")
            continue

    print(f"Total de arquivos movidos da pasta 'Outros': {contador_outros}")

    # Remove a pasta Outros e todas as subpastas vazias
    try:
        # Remove subpastas vazias primeiro
        for subpasta in sorted(pasta_outros.rglob('*'), reverse=True):
            if subpasta.is_dir():
                try:
                    if not any(subpasta.iterdir()):
                        subpasta.rmdir()
                        print(f"  Subpasta removida: {subpasta.relative_to(caminho)}")
                except:
                    pass

        # Tenta remover a pasta Outros principal
        if not any(pasta_outros.iterdir()):
            pasta_outros.rmdir()
            print("Pasta 'Outros' removida (estava vazia)")
    except Exception as e:
        print(f"Aviso: Não foi possível remover completamente a pasta 'Outros': {e}")
else:
    print("Pasta 'Outros' não encontrada ou já foi processada")

# ETAPA 2: Processar arquivos no diretório principal de Downloads
print("\nProcessando arquivos do diretório Downloads...")
arquivos = list(caminho.iterdir())
contador_principal = 0

for arquivo in arquivos:
    try:
        if organizar_arquivo(arquivo, caminho):
            contador_principal += 1
            print(f"  Organizado: {arquivo.name}")
    except Exception as e:
        print(f"  Erro ao processar {arquivo.name}: {e}")
        continue

print(f"Total de arquivos organizados no Downloads: {contador_principal}")
print("\n✓ Processamento Concluído!")
