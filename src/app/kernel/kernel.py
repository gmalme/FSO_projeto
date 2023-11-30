import os
from sys import argv
import operator
import time
from utils.output import Output
from utils.dir import ROOT_DIR
from app.processo.gerenciador_processo import ProcessoGerenciador
from app.recursos_sistema.arquivo.gerenciador_arquivo import GerenciadorArquivos
from app.recursos_sistema.memoria.gerenciador_memoria import GerenciadorMemoria
from app.gerenciador_recursos.gerenciador_recurso import GerenciadorRecurso
from utils.messages import *


class Kernel:
    CAMINHO_SAIDA_MEMORIA = os.path.join(ROOT_DIR, 'output', 'memoria.out')
    CAMINHO_SAIDA_DISCO = os.path.join(ROOT_DIR, 'output', 'disco.out')

    def __init__(self) -> None:
        self.gerenciador_arquivo = GerenciadorArquivos()
        self.gerenciador_recurso = GerenciadorRecurso()
        self.gerenciador_memoria = GerenciadorMemoria()
        self.gerenciador_processo = ProcessoGerenciador()

    def disparar_manualmente(self):
        for processo in self.gerenciador_processo.tabela_processos:
            self.gerenciador_processo.inserir_processo_fila(processo)
            time.sleep(2)

    def disparar_processo(self):
        """Disparar processos na fila com base no tempo de início."""
        processos_ordenados = sorted(self.gerenciador_processo.tabela_processos, key=operator.attrgetter('tempo_inicio'))
        acumulador = 0
        for processo in processos_ordenados:
            tempo_espera = processo.tempo_inicio - acumulador
            if tempo_espera > 0:
                time.sleep(tempo_espera)
            with self.gerenciador_processo.fila_lock:
                self.gerenciador_processo.inserir_processo_fila(processo)
            acumulador = processo.tempo_inicio

    def executar(self) -> None:
        try:
            self.iniciar()
            self.disparar_processo()
            self.gerenciador_processo.thread_tempo_real.join()
            self.gerenciador_processo.thread_usuarios.join()
        except KeyboardInterrupt:
            print('')
            with open(self.CAMINHO_SAIDA_MEMORIA, 'w+') as f:
                f.write(str(self.gerenciador_memoria.memoria))
            with open(self.CAMINHO_SAIDA_DISCO, 'w+') as f:
                f.write(str(self.gerenciador_arquivo.disco))
            self.gerenciador_arquivo.verificar_operacoes_restantes(self.gerenciador_processo.processos_terminados)
            exit()

    def iniciar(self) -> None:
        self.gerenciador_processo.ler_processos()
        self.gerenciador_arquivo.ler_arquivos()
