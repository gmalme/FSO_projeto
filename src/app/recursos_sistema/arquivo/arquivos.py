class Arquivo:
    def __init__(self, nome: str, primeiro_bloco: str, tamanho_bloco: str, criado_por: int = 0) -> None:
        self.nome = nome.strip()
        self.primeiro_bloco = int(primeiro_bloco.strip())
        self.tamanho_bloco = int(tamanho_bloco.strip())
        self.criado_por = criado_por

    def __repr__(self) -> str:
        return f'Arquivo {self.nome} está no bloco {self.primeiro_bloco} tem tamanho {self.tamanho_bloco} blocos'
