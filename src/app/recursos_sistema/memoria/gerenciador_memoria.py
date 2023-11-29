from app.recursos_sistema.memoria.memoria import Memory
from app.processo.processo import Processo
from utils.singleton import Singleton

class GerenciadorMemoria(metaclass=Singleton):
    def __init__(self) -> None:
        self.MEMORY_REAl_TIME_SIZE = 64
        self.MEMORY_USER_SIZE = 960
        self.memory = Memory(self.MEMORY_REAl_TIME_SIZE, self.MEMORY_USER_SIZE)
        self.allocated_process = []

    def alocar(self, Processo: Processo):
        if(Processo.pid in self.allocated_process):
            return Processo.memoria_inicio_bloco

        Processo.memoria_inicio_bloco = self.memory.malloc(Processo.prioridade, Processo.memoria_tamanho_bloco, Processo.pid)
        if(Processo.memoria_inicio_bloco >= 0):
            self.allocated_process.append(Processo.pid)
        return Processo.memoria_inicio_bloco
    
    def liberar(self, Processo: Processo):
        self.memory.free(Processo.memoria_inicio_bloco, Processo.memoria_tamanho_bloco)
        self.allocated_process.remove(Processo.pid)