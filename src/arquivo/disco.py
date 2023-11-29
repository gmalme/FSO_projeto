from utils.ascii_table import create_table
from arquivo.bit_enum import Bit


class Disco:
    def __init__(self, tamanho) -> None:
        """Inicializa um disco com o tamanho fornecido."""
        self.tamanho = int(tamanho.strip())
        self.mapa_bits = [Bit.LIVRE.value] * self.tamanho

    def __repr__(self):
        return create_table(self.mapa_bits)

    def __str__(self):
        return self.__repr__()

    def __first_fit(self, tamanho_bloco):
        """Encontra o primeiro espaço disponível para um bloco do tamanho fornecido."""
        assert 0 < tamanho_bloco <= self.tamanho, "Tamanho de bloco inválido"

        for index in range(self.tamanho - tamanho_bloco + 1):
            espaco = self.mapa_bits[index:index + tamanho_bloco]
            if espaco.count(Bit.LIVRE.value) == tamanho_bloco:
                return index

        return -1

    def alocar(self, tamanho_bloco, nome_arquivo):
        """Aloca um bloco do tamanho fornecido para o arquivo especificado."""
        start_addr = self.__first_fit(tamanho_bloco)

        if start_addr < 0:
            return -1

        self.preencher(start_addr, tamanho_bloco, nome_arquivo)
        return start_addr

    def preencher(self, start_addr, tamanho_bloco, nome_arquivo):
        """Preenche o bloco especificado com o nome do arquivo fornecido."""
        for i in range(start_addr, start_addr + tamanho_bloco):
            self.mapa_bits[i] = nome_arquivo

    def liberar(self, start_addr, tamanho_bloco):
        """Libera o bloco especificado."""
        for i in range(start_addr, start_addr + tamanho_bloco):
            self.mapa_bits[i] = Bit.LIVRE.value
