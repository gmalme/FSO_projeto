"""
Gerenciador de Arquivos

O Gerenciador de Arquivos é responsável por permitir que os processos criem e deletem arquivos, seguindo um modelo de alocação específico.

Funcionalidades:
- Permitir que cada processo crie e delete arquivos.
- Na criação de um arquivo, os dados devem permanecer no disco mesmo após o encerramento do processo.
- O sistema de arquivos realizará alocação através do método contíguo, utilizando o algoritmo first-fit.
- Garantir que os processos de tempo real possam criar (se houver espaço) e deletar qualquer arquivo, independentemente de terem sido criados pelo processo.
- Os processos comuns só podem deletar arquivos criados por eles e podem criar quantos arquivos desejarem, no tamanho solicitado (se houver espaço suficiente).

Entrada:
- O sistema de arquivos recebe um arquivo .txt contendo a quantidade total de blocos no disco, a especificação dos segmentos ocupados por cada arquivo e as operações a serem realizadas por cada processo.

Saída:
- Após a execução de todos os processos, o pseudo-SO exibirá um mapa na tela do computador, mostrando a ocupação atual do disco. O mapa descreverá quais arquivos estão em cada bloco e quais blocos estão vazios (identificados por 0).
"""
from typing import List

from file.disk import Disk
from file.files import File
from file.operations import Operation
from utils.dir import ROOT_DIR
from process.process import Process
from utils.singleton import Singleton
from utils.output import *
from utils.messages import *


class FileManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.disk: Disk
        self.files: List[File] = []
        self.operations: list = []
        self.out = Output()

    def read_files(self) -> None:
        with open(ROOT_DIR + '/input/files.txt') as files_file:
            list_line = files_file.readlines()
            num_files = int(list_line[1].strip())

            disk_size = list_line[0].strip()
            file_list = list_line[2:num_files + 2]
            operation_list = list_line[num_files + 2:len(list_line)]

            self.disk = Disk(disk_size)
            self.files = [File(*f.split(',')) for f in file_list]
            self.operations = [Operation(*o.split(',')) for o in operation_list]
            self.__init_disk()

    def __init_disk(self):
        for file in self.files:
            self.disk.fill(file.first_block, file.block_size, file.name)

    def allocate(self, filename: str, file_size: int, pid: int):
        start_addr = self.disk.alloc(file_size, filename)

        if start_addr < 0: self.out.error(NOT_ENOUGH_SPACE, pid=pid, filename=filename)

        return start_addr

    def execute_operation(self, operation: Operation, process: Process):
        self.operations.remove(operation)
        if operation.operation_id:
            file = list(filter(lambda f: f.name == operation.file_name, self.files))

            if len(file) <= 0:
                self.out.error(INEXISTENT_REMOVE_FILE, pid=process.pid, filename=operation.file_name)
                return

            file = file[0]

            if process.pid != file.created_by and process.pid != 0:
                self.out.error(NO_PERMISSION_REMOVE_FILE, pid=process.pid, filename=operation.file_name)
                return

            self.disk.free(file.first_block, file.block_size)
            self.out.success(SUCCESSFUL_REMOVE_FILE, pid=process.pid, filename=operation.file_name)
        else:
            start_addr = self.allocate(operation.file_name, operation.created_block_size, process.pid)

            if start_addr == -1: return

            new_file: File = File(operation.file_name, str(start_addr), str(operation.created_block_size), process.pid)
            self.files.append(new_file)
            block_range = list(range(start_addr, start_addr + operation.created_block_size))
            block_range = list(map(lambda x: str(x), block_range))
            self.out.success(SUCCESSFUL_REMOVE_FILE, pid=process.pid, filename=operation.file_name,
                             block_range=block_range)

    def get_operations(self, pid: int):
        return list(filter(lambda o: o.process_id == pid, self.operations))

    def check_operations_left(self, finished_proc):
        for f in finished_proc:
            remaning = self.get_operations(f)
            if (len(remaning) > 0):
                for o in remaning: self.out.error(OPERATION_NOT_PERFORMED, pid=o.process_id, op=o)
