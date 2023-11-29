from typing import List


class Processo:
    def __init__(self, processo: List[str], id) -> None:
        self.pid = id
        self.tempo_inicio = int(processo[0].strip())
        self.processo_time = int(processo[2].strip())
        self.waiting_time = 0
        self.cpu_time = 0
        self.printer = int(processo[4].strip())
        self.scanner = int(processo[5].strip())
        self.modem = int(processo[6].strip())
        self.sata = int(processo[7].strip())
        self.prioridade = int(processo[1].strip())
        self.memoria_inicio_bloco = -1
        self.memoria_tamanho_bloco = int(processo[3].strip())

    def __repr__(self) -> str:
        return f'''
        PID: {self.pid}
        blocks: {self.memoria_tamanho_bloco}
        priority: {self.prioridade}
        printers: {self.printer}
        scanners: {self.scanner}
        modems: {self.modem}
        drives: {self.sata}
        '''
