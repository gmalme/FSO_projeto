"""
Gerenciador de Processos

O Gerenciador de Processos tem como função agrupar os processos em quatro níveis de prioridades.

Fila - FIFO:
- O programa inclui duas filas de prioridades distintas: a fila de processos de tempo real e a fila de processos de usuários.
- Os processos de usuário utilizam múltiplas filas de prioridades com realimentação, mantendo três filas com prioridades distintas.
- Os processos de usuário podem ser preemptados, e o quantum é definido como 1 milissegundo.
- Cada fila deve ter suporte para, no máximo, 1000 processos.
"""
from typing import List

from process.process import Process
from utils.dir import ROOT_DIR
from utils.output import Output
from queues.processes_queue import ProcessesQueue
from memory.memory_manager import MemoryManager
from resources.resource_manager import ResourceManager
from file.file_manager import FileManager
from threading import Thread, Lock
import time
from utils.messages import *


class ProcessManager:
    def __init__(self) -> None:
        self.processes_table: List[Process] = []
        self.queue = ProcessesQueue()
        self.memory_manager = MemoryManager()
        self.resource_manager = ResourceManager()
        self.file_manager = FileManager()
        self.current_proc = (None, None)
        self.real_time_thread = Thread(target=self.real_time_queue_thread, daemon=True)
        self.user_thread = Thread(target=self.user_queue_thread, daemon=True)
        self.queue_lock = Lock()
        self.terminated_processes = []
        self.blocked_processes = []
        self.flag_rt_interrupt = False
        self.out = Output()
        self.__wait_for_process()

    def read_processes(self) -> None:
        process_list = []
        with open(ROOT_DIR + '/input/processes.txt') as processes_file: process_list = processes_file.readlines()

        self.processes_table = [Process(p.split(','), id) for (id, p) in enumerate(process_list)]

    def insert_process_queue(self, process: Process):
        if self.queue.get_size() > self.queue.TAMANHO_MAXIMO_TOTAL_DA_FILA:
            self.out.error(MAX_PROCESSES_QUEUE_REACHED, pid=process.pid, max_size=self.queue.TAMANHO_MAXIMO_TOTAL_DA_FILA)
            return

        if process.priority:
            self.queue.user_queue.put(process)
        else:
            self.queue.real_time_queue.put(process)

    def __context_switching(self, process):
        """ Realizes the context switching between two processes

        Args:
            process (Process): process that will be executed (allocated in memory)

        Returns:
            Process: the last current process
        """
        if process[0]:
            result = self.memory_manager.alloc(process[0])
            if result == -2: return -1
            if result == -1:
                self.out.debug(BLOCKED_PROCESS)
                self.blocked_processes.append(process[0])
                return 0
        self.current_proc = process
        return 1

    def __wait_for_process(self):
        self.real_time_thread.start()
        self.user_thread.start()

    def unblock_processes(self):
        for blocked_process in self.blocked_processes:
            result_memo = self.memory_manager.alloc(blocked_process)
            result = self.resource_manager.request(blocked_process)
            if result > 0 and result_memo >= 0:
                self.blocked_processes.remove(blocked_process)
                self.queue.user_queue.put(blocked_process)
                break

    def real_time_running(self):
        self.queue.user_queue.up()
        process, _ = self.current_proc
        o = 0
        operations = self.file_manager.get_operations(process.pid)
        self.out.log(START_PROCESS, process=process, pid=process.pid)
        while process.process_time > 0:

            self.out.log(PROCESS_INSTRUCTION, pid=process.pid, op=process.cpu_time)
            if o < len(operations):
                self.file_manager.execute_operation(operations[o], process)
                o += 1
            process.process_time -= 1
            process.cpu_time += 1
            self.queue.user_queue.aging()
            time.sleep(1)

        self.out.log(PROCESS_RETURN_SIGINT, pid=process.pid)
        self.terminated_processes.append(process.pid)
        self.memory_manager.free(process)

    def user_running(self):
        self.queue.user_queue.up()
        process, queue = self.current_proc
        remaining_quantum = self.queue.user_queue.get_queue_quantum(queue)
        self.flag_rt_interrupt = False
        o = 0
        operations = self.file_manager.get_operations(process.pid)
        self.out.log(START_PROCESS, process=process, pid=process.pid)
        while remaining_quantum > 0 and process.process_time > 0:

            if not self.queue.real_time_queue.empty(): self.flag_rt_interrupt = True

            self.out.log(PROCESS_INSTRUCTION, pid=process.pid, op=process.cpu_time)
            if o < len(operations):
                self.file_manager.execute_operation(operations[o], process)
                o += 1
            remaining_quantum -= 1
            process.process_time -= 1
            process.cpu_time += 1
            self.queue.user_queue.aging()
            time.sleep(1)

        if process.process_time <= 0:
            self.out.debug(DEALLOCATED_RESOURCES)
            self.out.log(PROCESS_RETURN_SIGINT, pid=process.pid)
            self.resource_manager.deallocate(process)
            self.terminated_processes.append(process.pid)
            self.memory_manager.free(process)
            self.unblock_processes()
        else:
            self.queue.user_queue.down(*self.current_proc, self.flag_rt_interrupt)

    def real_time_queue_thread(self):
        """Thread function that will be waiting for the arriving real-time processes"""
        while True:
            self.out.debug(WAITING_FOR_RT_PROCESS)
            if not self.queue.real_time_queue.empty():
                self.queue_lock.acquire()
                first = (self.queue.real_time_queue.get(), self.queue.real_time_queue)
                result = self.__context_switching(first)
                if result > 0: self.real_time_running()
                self.queue_lock.release()
            time.sleep(1)

    def user_queue_thread(self):
        """Thread function that will be waiting for the arriving user processes"""
        while True:
            self.out.debug(WAITING_FOR_USER_PROCESS)
            if not self.queue.user_queue.empty():
                self.queue_lock.acquire()
                if not self.queue.real_time_queue.empty():
                    self.queue_lock.release()
                else:
                    first = self.queue.user_queue.get()
                    resources = self.resource_manager.request(first[0])
                    if resources:
                        result = self.__context_switching(first)
                        if result > 0: self.user_running()
                    elif not resources:
                        self.out.debug(BLOCKED_PROCESS)
                        self.blocked_processes.append(first[0])

                    self.queue_lock.release()
            time.sleep(1)
