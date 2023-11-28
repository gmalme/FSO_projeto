from queue import Queue
from queues.user_queue import UserQueue
import time
from threading import Thread


class ProcessesQueue:
    """Uma classe que representa uma fila combinada para processos em tempo real e de usuário."""

    def __init__(self) -> None:
        """Inicializa o ProcessesQueue."""
        self.real_time_queue = Queue()
        self.user_queue = UserQueue()
        self.TAMANHO_MAXIMO_TOTAL_DA_FILA = 1000

    def get_size(self) -> int:
        """Obtém o tamanho total das filas combinadas."""
        return self.real_time_queue.qsize() + self.user_queue.qsize()
