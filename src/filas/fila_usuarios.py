from queue import Queue
from processo.processo import Processo
from utils.output import Output
from utils.messages import *


class FilaUsuarios:
    def __init__(self) -> None:
        self.saida = Output()
        self.fila1 = Queue()  # RR 1-20
        self.fila2 = Queue()  # RR 21-49
        self.fila3 = Queue()  # RR >= 50
        self.MAX_PRIORIDADE_FILA1 = 20
        self.MAX_PRIORIDADE_FILA2 = 21
        self.MAX_PRIORIDADE_FILA3 = 50
        self.QUANTUM_FILA1 = 5
        self.QUANTUM_FILA2 = 10
        self.QUANTUM_FILA3 = 15
        self.TEMPO_ESPERA_ENVELHECIMENTO = 5

    def obter_fila_quantum(self, fila):
        if fila == self.fila1:
            return self.QUANTUM_FILA1
        if fila == self.fila2:
            return self.QUANTUM_FILA2
        return self.QUANTUM_FILA3

    def inserir(self, processo: Processo):
        if processo.prioridade <= self.MAX_PRIORIDADE_FILA1:
            self.fila1.put(processo)
        elif self.MAX_PRIORIDADE_FILA1 < processo.prioridade < self.MAX_PRIORIDADE_FILA3:
            self.fila2.put(processo)
        else:
            self.fila3.put(processo)

    def vazia(self):
        return all(fila.empty() for fila in [self.fila1, self.fila2, self.fila3])

    def obter(self):
        for fila in [self.fila1, self.fila2, self.fila3]:
            if not fila.empty():
                return fila.get(), fila

    def tamanho_fila(self):
        return sum(fila.qsize() for fila in [self.fila1, self.fila2, self.fila3])

    def descer(self, processo, ultima_fila, interrupcao):
        if not processo:
            return

        if interrupcao:
            ultima_fila.put(processo)
            return

        aumento_prioridade = 6 if ultima_fila == self.fila2 else 8
        processo.prioridade = min(self.MAX_PRIORIDADE_FILA3 - 1, processo.prioridade + aumento_prioridade)
        self.fila3.put(processo)
        self.saida.debug(DOWN_PROCESSO, pid=processo.pid, fila=3)

    def envelhecer(self):
        for fila in [self.fila1, self.fila2, self.fila3]:
            for proc in fila.queue:
                proc.waiting_time += 1
                if proc.waiting_time % self.TEMPO_ESPERA_ENVELHECIMENTO == 0:
                    proc.prioridade = max(1, proc.prioridade - 1)

    def subir(self):
        fila2_copy = self.fila2.queue.copy()
        fila3_copy = self.fila3.queue.copy()

        for processo in self.fila2.queue:
            if processo.prioridade <= self.MAX_PRIORIDADE_FILA1:
                self.fila1.put(processo)
                fila2_copy.remove(processo)
                self.saida.debug(UP_PROCESSO, pid=processo.pid, fila=1)

        for processo in self.fila3.queue:
            if self.MAX_PRIORIDADE_FILA1 < processo.prioridade < self.MAX_PRIORIDADE_FILA3:
                self.fila2.put(processo)
                fila3_copy.remove(processo)
                self.saida.debug(SUBIR_PROCESSO, pid=processo.pid, fila=2)

        self.fila2.queue = fila2_copy.copy()
        self.fila3.queue = fila3_copy.copy()
