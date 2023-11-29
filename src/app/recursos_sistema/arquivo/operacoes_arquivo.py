class Operacao:
    def __init__(self, processo_id: str, operacao_id: str, nome_arquivo: str, tamanho_bloco_criado:str='-1') -> None:
        self.processo_id = int(processo_id.strip())
        self.operacao_id = int(operacao_id.strip())
        self.nome_arquivo = nome_arquivo.strip()
        self.tamanho_bloco_criado = int(tamanho_bloco_criado.strip())
        
    def __repr__(self) -> str:
        return f'Operação do processoo {self.processo_id} de "criação" do arquivo {self.nome_arquivo} ({self.tamanho_bloco_criado} blocos)'