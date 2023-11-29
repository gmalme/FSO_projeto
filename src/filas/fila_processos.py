from queue import Queue
from filas.fila_usuarios import FilaUsuarios
import time
from threading import Thread


class FilaProcessos:
    """Uma classe que representa uma fila combinada para processos em tempo real e de usuário."""

    def __init__(self) -> None:
        """Inicializa o FilaProcessos."""
        self.fila_atual = Queue()
        self.fila_usuarios = FilaUsuarios()
        self.TAMANHO_MAXIMO_TOTAL_DA_FILA = 1000

    def get_size(self) -> int:
        """Obtém o tamanho total das filas combinadas."""
        return self.fila_atual.qsize() + self.fila_usuarios.tamanho_fila()
