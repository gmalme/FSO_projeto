"""
Gerenciador de processos

O Gerenciador de processos tem como função agrupar os processos em quatro níveis de prioridades.

Fila - FIFO:
- O programa inclui duas filas de prioridades distintas: a fila de processos de tempo real e a fila de processos de usuários.
- Os processos de usuário utilizam múltiplas filas de prioridades com realimentação, mantendo três filas com prioridades distintas.
- Os processos de usuário podem ser preemptados, e o quantum é definido como 1 milissegundo.
- Cada fila deve ter suporte para, no máximo, 1000 processos.
"""
from typing import List

from app.processo.processo import Processo
from utils.dir import ROOT_DIR
from utils.output import Output
from app.filas.fila_processos import FilaProcessos
from app.recursos_sistema.memoria.gerenciador_memoria import GerenciadorMemoria
from app.gerenciador_recursos.gerenciador_recurso import GerenciadorRecurso
from app.recursos_sistema.arquivo.gerenciador_arquivo import GerenciadorArquivos
from threading import Thread, Lock
import time
from utils.messages import *


class ProcessoGerenciador:
    def __init__(self) -> None:
        self.tabela_processos: List[Processo] = []
        self.fila = FilaProcessos()
        self.gerenciador_memoria = GerenciadorMemoria()
        self.gerenciador_recurso = GerenciadorRecurso()
        self.gerenciador_arquivo = GerenciadorArquivos()
        self.current_proc = (None, None)
        self.thread_tempo_real = Thread(target=self.fila_atual_thread, daemon=True)
        self.thread_usuarios = Thread(target=self.fila_thread_usuarios, daemon=True)
        self.fila_lock = Lock()
        self.terminated_processos = []
        self.blocked_processos = []
        self.flag_rt_interrupt = False
        self.out = Output()
        self.__wait_for_processo()

    def ler_processos(self) -> None:
        processo_list = []
        with open(ROOT_DIR + '/input/processos.txt') as processos_arquivo: processo_list = processos_arquivo.readlines()

        self.tabela_processos = [Processo(p.split(','), id) for (id, p) in enumerate(processo_list)]

    def inserir_processo_fila(self, processo: Processo):
        if self.fila.get_size() > self.fila.TAMANHO_MAXIMO_TOTAL_DA_FILA:
            self.out.error(MAX_FILA_PROCESSOS_REACHED, pid=processo.pid, max_size=self.fila.TAMANHO_MAXIMO_TOTAL_DA_FILA)
            return

        if processo.prioridade:
            self.fila.fila_usuarios.inserir(processo)
        else:
            self.fila.fila_atual.put(processo)

    def __context_switching(self, processo):
        if processo[0]:
            result = self.gerenciador_memoria.alocar(processo[0])
            if result == -2: return -1
            if result == -1:
                self.out.debug(BLOCKED_PROCESSO)
                self.blocked_processos.append(processo[0])
                return 0
        self.current_proc = processo
        return 1

    def __wait_for_processo(self):
        self.thread_tempo_real.start()
        self.thread_usuarios.start()

    def unblock_processos(self):
        for blocked_processo in self.blocked_processos:
            result_memo = self.gerenciador_memoria.alocar(blocked_processo)
            result = self.gerenciador_recurso.request(blocked_processo)
            if result > 0 and result_memo >= 0:
                self.blocked_processos.remove(blocked_processo)
                self.fila.fila_usuarios.inserir(blocked_processo)
                break

    def real_time_running(self):
        self.fila.fila_usuarios.subir()
        processo, _ = self.current_proc
        o = 0
        operations = self.gerenciador_arquivo.obter_operacoes(processo.pid)
        self.out.log(START_PROCESSO, processo=processo, pid=processo.pid)
        while processo.processo_time > 0:

            self.out.log(PROCESSO_INSTRUCTION, pid=processo.pid, op=processo.cpu_time)
            if o < len(operations):
                self.gerenciador_arquivo.executar_operacao(operations[o], processo)
                o += 1
            processo.processo_time -= 1
            processo.cpu_time += 1
            self.fila.fila_usuarios.envelhecer()
            time.sleep(1)

        self.out.log(PROCESSO_RETURN_SIGINT, pid=processo.pid)
        self.terminated_processos.append(processo.pid)
        self.gerenciador_memoria.liberar(processo)

    def usuarios_running(self):
        self.fila.fila_usuarios.subir()
        processo, fila = self.current_proc
        remaining_quantum = self.fila.fila_usuarios.obter_fila_quantum(fila)
        self.flag_rt_interrupt = False
        o = 0
        operations = self.gerenciador_arquivo.obter_operacoes(processo.pid)
        self.out.log(START_PROCESSO, processo=processo, pid=processo.pid)
        while remaining_quantum > 0 and processo.processo_time > 0:

            if not self.fila.fila_atual.empty(): self.flag_rt_interrupt = True

            self.out.log(PROCESSO_INSTRUCTION, pid=processo.pid, op=processo.cpu_time)
            if o < len(operations):
                self.gerenciador_arquivo.executar_operacao(operations[o], processo)
                o += 1
            remaining_quantum -= 1
            processo.processo_time -= 1
            processo.cpu_time += 1
            self.fila.fila_usuarios.envelhecer()
            time.sleep(1)

        if processo.processo_time <= 0:
            self.out.debug(DEALLOCATED_RECURSOS)
            self.out.log(PROCESSO_RETURN_SIGINT, pid=processo.pid)
            self.gerenciador_recurso.deallocate(processo)
            self.terminated_processos.append(processo.pid)
            self.gerenciador_memoria.liberar(processo)
            self.unblock_processos()
        else:
            self.fila.fila_usuarios.descer(*self.current_proc, self.flag_rt_interrupt)

    def fila_atual_thread(self):
        controle = 0
        while controle < 10:
            self.out.debug(WAITING_FOR_RT_PROCESSO)
            if not self.fila.fila_atual.empty():
                controle=0
                self.fila_lock.acquire()
                first = (self.fila.fila_atual.get(), self.fila.fila_atual)
                result = self.__context_switching(first)
                if result > 0: self.real_time_running()
                self.fila_lock.release()
            time.sleep(1)
            controle+=1

    def fila_thread_usuarios(self):
        controle = 0
        while controle < 10:
            self.out.debug(WAITING_FOR_USUARIOS_PROCESSO)
            if not self.fila.fila_usuarios.vazia():
                controle=0
                self.fila_lock.acquire()
                if not self.fila.fila_atual.empty():
                    self.fila_lock.release()
                else:
                    first = self.fila.fila_usuarios.obter()
                    recursos = self.gerenciador_recurso.request(first[0])
                    if recursos:
                        result = self.__context_switching(first)
                        if result > 0: self.usuarios_running()
                    elif not recursos:
                        self.out.debug(BLOCKED_PROCESSO)
                        self.blocked_processos.append(first[0])

                    self.fila_lock.release()
            time.sleep(1)
            controle+=1

