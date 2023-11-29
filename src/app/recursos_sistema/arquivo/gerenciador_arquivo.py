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

from app.recursos_sistema.disco.disco import Disco
from app.recursos_sistema.arquivo.arquivos import Arquivo
from app.recursos_sistema.arquivo.operacoes_arquivo import Operacao
from utils.dir import ROOT_DIR
from app.processo.processo import Processo
from utils.singleton import Singleton
from utils.output import *
from utils.messages import *


class GerenciadorArquivos(metaclass=Singleton):
    def __init__(self) -> None:
        self.disco: Disco
        self.arquivos: List[Arquivo] = []
        self.operacoes: list = []
        self.out = Output()

    def ler_arquivos(self) -> None:
        with open(ROOT_DIR + '/input/arquivos.txt') as arquivos_arquivo:
            list_line = arquivos_arquivo.readlines()
            num_arquivos = int(list_line[1].strip())

            tamanho_disco = list_line[0].strip()
            arquivo_list = list_line[2:num_arquivos + 2]
            operacao_list = list_line[num_arquivos + 2:len(list_line)]

            self.disco = Disco(tamanho_disco)
            self.arquivos = [Arquivo(*f.split(',')) for f in arquivo_list]
            self.operacoes = [Operacao(*o.split(',')) for o in operacao_list]
            self.__inicializar_disco()

    def __inicializar_disco(self):
        for arquivo in self.arquivos:
            self.disco.preencher(arquivo.primeiro_bloco, arquivo.tamanho_bloco, arquivo.nome)

    def alocar(self, arquivonome: str, tamanho_arquivo: int, pid: int):
        start_addr = self.disco.alocar(tamanho_arquivo, arquivonome)

        if start_addr < 0:
            self.out.error(NOT_ENOUGH_SPACE, pid=pid, arquivonome=arquivonome)

        return start_addr

    def executar_operacao(self, operacao: Operacao, processo: Processo):
        self.operacoes.remove(operacao)
        if operacao.operacao_id:
            arquivo = list(filter(lambda f: f.nome == operacao.nome_arquivo, self.arquivos))

            if len(arquivo) <= 0:
                self.out.error(INEXISTENT_REMOVE_ARQUIVO, pid=processo.pid, arquivonome=operacao.nome_arquivo)
                return

            arquivo = arquivo[0]

            if processo.pid != arquivo.criado_por and processo.pid != 0:
                self.out.error(NO_PERMISSION_REMOVE_ARQUIVO, pid=processo.pid, arquivonome=operacao.nome_arquivo)
                return

            self.disco.liberar(arquivo.primeiro_bloco, arquivo.tamanho_bloco)
            self.out.success(SUCCESSFUL_REMOVE_ARQUIVO, pid=processo.pid, arquivonome=operacao.nome_arquivo)
        else:
            start_addr = self.alocar(operacao.nome_arquivo, operacao.tamanho_bloco_criado, processo.pid)

            if start_addr == -1:
                return

            novo_arquivo: Arquivo = Arquivo(operacao.nome_arquivo, str(start_addr), str(operacao.tamanho_bloco_criado), processo.pid)
            self.arquivos.append(novo_arquivo)
            blocos = list(range(start_addr, start_addr + operacao.tamanho_bloco_criado))
            blocos = list(map(lambda x: str(x), blocos))
            self.out.success(SUCCESSFUL_REMOVE_ARQUIVO, pid=processo.pid, arquivonome=operacao.nome_arquivo,
                             block_range=blocos)

    def obter_operacoes(self, pid: int):
        return list(filter(lambda o: o.processo_id == pid, self.operacoes))

    def verificar_operacoes_restantes(self, processos_finalizados):
        for proc_finalizado in processos_finalizados:
            restantes = self.obter_operacoes(proc_finalizado)
            if len(restantes) > 0:
                for op_restante in restantes:
                    self.out.error(OPERACAO_NOT_PERFORMED, pid=op_restante.processo_id, op=op_restante)
