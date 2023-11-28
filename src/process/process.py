from typing import List


class Process:
    def __init__(self, process: List[str], id) -> None:
        """Contexto de software"""

        # Identificacao
        self.pid = id
        # self.uid = uid (?)

        # Quotas
        self.starting_time = int(process[0].strip())
        self.process_time = int(process[2].strip())
        self.waiting_time = 0
        self.cpu_time = 0
        self.printer = int(process[4].strip())
        self.scanner = int(process[5].strip())
        self.modem = int(process[6].strip())
        self.sata = int(process[7].strip())

        # Privilegios
        self.priority = int(process[1].strip())

        '''Fim do contexto de software'''

        ''' Espaco de enderecamento '''
        self.memory_start_block = -1
        self.memory_block_size = int(process[3].strip())

        ''' Fim do espaco de enderecamento '''

        ''' Contexto de hardware
            não existe nesse contexto
            os registradores foram abstraidos
        '''

    def __repr__(self) -> str:
        return f'''
        PID: {self.pid}
        blocks: {self.memory_block_size}
        priority: {self.priority}
        printers: {self.printer}
        scanners: {self.scanner}
        modems: {self.modem}
        drives: {self.sata}
        '''
