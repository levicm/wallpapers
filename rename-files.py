import os
import re

# Função para processar um único diretório
def process_directory(path):
    print(f"Precessing directory: {path}")
    prefix_file = os.path.join(path, '.prefix')
    if not os.path.exists(prefix_file):
        print(f"[Ignoring] Directory '{path}'. File '.prefix' not found.")
        return

    # Ler o prefixo do arquivo
    with open(prefix_file, 'r') as f:
        prefix = f.read().strip()

    # Expressão para arquivos já renomeados corretamente
    pattern = re.compile(rf'^{re.escape(prefix)}-(\d{{3}})\.jpe?g$', re.IGNORECASE)

    # Descobrir o maior índice existente
    existing_indices = []
    for file in os.listdir(path):
        if pattern.match(file):
            match = pattern.match(file)
            existing_indices.append(int(match.group(1)))

    start_index = max(existing_indices) + 1 if existing_indices else 1
    print(f"Start index: {start_index}")

    # Renomear arquivos fora do padrão
    i = start_index
    for file in sorted(os.listdir(path)):
        full_path = os.path.join(path, file)
        if not os.path.isfile(full_path) or pattern.match(file):
            continue

        ext = file.split('.')[-1].lower()
        if ext not in ('jpg', 'jpeg'):
            continue

        new_name = f"{prefix}-{i:03d}.{ext}"
        new_path = os.path.join(path, new_name)
        os.rename(full_path, new_path)
        print(f"[{path}] {file} → {new_name}")
        i += 1

# Executa a função em todos os subdiretórios recursivamente
for root, dirs, files in os.walk('.'):
    if os.path.basename(root).startswith('.'):
        print(f"[Ignorado] Diretório oculto '{root}'")
        continue

    process_directory(root)