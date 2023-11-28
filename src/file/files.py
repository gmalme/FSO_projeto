class File:
    def __init__(self, name: str, first_block: str, block_size: str, created_by: int = 0) -> None:
        self.name = name.strip()
        self.first_block = int(first_block.strip())
        self.block_size = int(block_size.strip())
        self.created_by = created_by

    def __repr__(self) -> str:
        return f'Arquivo {self.name} está no bloco {self.first_block} tem tamanho {self.block_size} blocos'