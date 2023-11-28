import os

src_dir = ''
ROOT_DIR = os.path.abspath(os.path.join(os.curdir, src_dir))

if not os.path.exists(ROOT_DIR): print(f"O diretório '{src_dir}' não existe. Certifique-se de que ele foi criado.")