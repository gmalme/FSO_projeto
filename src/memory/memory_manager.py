"""
Gerenciador de Memória

O Gerenciador de Memória tem como objetivo garantir que um processo não acesse as regiões de memória de outro processo.

Estrutura de Memória:
- A alocação de memória é implementada como um conjunto de blocos contíguos, onde cada bloco representa uma palavra da memória real.
- Cada processo deve alocar um segmento contíguo de memória, o qual permanecerá alocado durante toda a execução do processo.
- Não é necessário implementar memória virtual, swap, nem sistema de paginação.
- A gestão da memória envolve apenas a verificação da disponibilidade de recursos antes de iniciar um processo.
- O tamanho fixo da memória é de 1024 blocos.
- 64 blocos são reservados para processos de tempo-real, e os 960 blocos restantes são compartilhados entre os processos de usuário.
"""

from memory.memory import Memory
from process.process import Process
from utils.singleton import Singleton

class MemoryManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.MEMORY_REAL_TIME_SIZE = 64
        self.MEMORY_USER_SIZE = 960
        self.main_memory = Memory(self.MEMORY_REAL_TIME_SIZE, self.MEMORY_USER_SIZE)
        self.allocated_processes = set()

    def alloc(self, process: Process) -> int:
        """
        Allocate memory for a process.

        Returns the starting memory block index if successful, otherwise -1.
        """
        if process.pid in self.allocated_processes: return process.memory_start_block

        start_block = self.main_memory.malloc(process.priority, process.memory_block_size, process.pid)
        if start_block >= 0: self.allocated_processes.add(process.pid)
        return start_block

    def free(self, process: Process) -> None:
        """
        Free memory allocated to a process.
        """
        self.main_memory.free(process.memory_start_block, process.memory_block_size)
        self.allocated_processes.remove(process.pid)
