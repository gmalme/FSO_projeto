class Arquivo:
    def __init__(self, nome: str, primeiro_bloco: str, tamanho_bloco: str, criador: int = 0) -> None:
        self.nome = nome.strip()
        self.primeiro_bloco = int(primeiro_bloco.strip())
        self.tamanho_bloco = int(tamanho_bloco.strip())
        self.criador = criador

    def __repr__(self) -> str:
        return f'Arquivo {self.nome} está no bloco {self.primeiro_bloco} tem tamanho {self.tamanho_bloco} blocos'
