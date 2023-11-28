import os
from sys import argv
import operator
import time
from utils.output import Output
from utils.dir import ROOT_DIR
from process.process_manager import ProcessManager
from file.file_manager import FileManager
from memory.memory_manager import MemoryManager
from resources.resource_manager import ResourceManager
from utils.messages import *


class Kernel:
    OUTPUT_MEMORY_PATH = os.path.join(ROOT_DIR, 'output', 'memory.out')
    OUTPUT_DISK_PATH = os.path.join(ROOT_DIR, 'output', 'disk.out')

    def __init__(self) -> None:
        if len(argv) > 1 and argv[1] == '-d':
            Output(True).debug(DEBUG_MODE_ON)

        self.file_manager = FileManager()
        self.resource_manager = ResourceManager()
        self.memory_manager = MemoryManager()
        self.process_manager = ProcessManager()

    def manual_throw(self):
        # PROCESS SCHEDULING TEST
        self.process_manager.insert_process_queue(self.process_manager.processes_table[2])
        self.process_manager.insert_process_queue(self.process_manager.processes_table[3])
        time.sleep(3)
        self.process_manager.insert_process_queue(self.process_manager.processes_table[0])
        self.process_manager.insert_process_queue(self.process_manager.processes_table[1])

    def throw_process(self):
        """Throw processes into the queue based on starting time."""
        sorted_proc = sorted(self.process_manager.processes_table, key=operator.attrgetter('starting_time'))
        acc = 0
        for p in sorted_proc:
            sleep_time = p.starting_time - acc
            if sleep_time > 0:
                time.sleep(sleep_time)
            with self.process_manager.queue_lock:
                self.process_manager.insert_process_queue(p)
            acc = p.starting_time

    def executar(self) -> None:
        try:
            self.start()
            self.throw_process()
            self.process_manager.real_time_thread.join()
            self.process_manager.user_thread.join()
        except KeyboardInterrupt:
            print('')
            with open(self.OUTPUT_MEMORY_PATH, 'w+') as f:
                f.write(str(self.memory_manager.memory))
            with open(self.OUTPUT_DISK_PATH, 'w+') as f:
                f.write(str(self.file_manager.disk))
            self.file_manager.check_operations_left(self.process_manager.terminated_process)
            exit()

    def start(self) -> None:
        self.process_manager.read_processes()
        self.file_manager.read_files()

