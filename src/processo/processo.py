from typing import List


class Processo:
    def __init__(self, processo: List[str], id) -> None:
        """Contexto de software"""

        # Identificacao
        self.pid = id
        # self.uid = uid (?)

        # Quotas
        self.tempo_inicio = int(processo[0].strip())
        self.processo_time = int(processo[2].strip())
        self.waiting_time = 0
        self.cpu_time = 0
        self.printer = int(processo[4].strip())
        self.scanner = int(processo[5].strip())
        self.modem = int(processo[6].strip())
        self.sata = int(processo[7].strip())

        # Privilegios
        self.prioridade = int(processo[1].strip())

        '''Fim do contexto de software'''

        ''' Espaco de enderecamento '''
        self.memoria_inicio_bloco = -1
        self.memoria_tamanho_bloco = int(processo[3].strip())

        ''' Fim do espaco de enderecamento '''

        ''' Contexto de hardware
            não existe nesse contexto
            os registradores foram abstraidos
        '''

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
