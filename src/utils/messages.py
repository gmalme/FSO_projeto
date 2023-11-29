from colorama import Fore

NOT_ENOUGH_MEMO = 1                      
NOT_ENOUGH_SPACE = 2                     
NO_PERMISSION_REMOVE_ARQUIVO = 3           
INEXISTENT_REMOVE_ARQUIVO = 4              
EXCEEDED_RECURSOS = 5                  
BLOCKED_DUE_RECURSOS = 6               
OPERACAO_NOT_PERFORMED = 17            
MAX_FILA_PROCESSOS_REACHED = 20        
BLOCKED_DUE_MEMORIA = 21                 

SUCCESSFUL_REMOVE_ARQUIVO  = 7              
SUCCESSFUL_CREATE_ARQUIVO = 8               

START_PROCESSO = 9                       
PROCESSO_INSTRUCTION = 10
PROCESSO_RETURN_SIGINT = 11

DEALLOCATED_RECURSOS = 12
WAITING_FOR_RT_PROCESSO = 13
WAITING_FOR_USUARIOS_PROCESSO = 14
BLOCKED_PROCESSO = 15
DEBUG_MODE_ON = 16
DOWN_PROCESSO = 18
UP_PROCESSO = 19

ERROR_MESSAGES = {
    NOT_ENOUGH_MEMO: "\n\ndispatcher => O processoo {pid} não pode ser alocado na memória por falta de espaço",
    NOT_ENOUGH_SPACE: "\tSistema de arquivo => O processoo {pid} não pode criar o arquivo {arquivonome} (falta de espaço).",
    NO_PERMISSION_REMOVE_ARQUIVO: "\tSistema de arquivo => O processoo {processo.pid} não pode deletar o arquivo {arquivonome} (sem permissão).",
    INEXISTENT_REMOVE_ARQUIVO: "\tSistema de arquivo => O processoo {pid} não pode deletar o arquivo {arquivonome} porque ele não existe.",
    EXCEEDED_RECURSOS: "\n\ndispatcher => O processoo {pid} não conseguiu ser criado (gerenciador_recursos insuficientes)",
    BLOCKED_DUE_RECURSOS: "\n\ndispatcher => O processoo {pid} foi bloqueado (não conseguiu obter {recurso} - requisitado: {proc_quantity} (disponível {max_quantity_remaning})).",    OPERACAO_NOT_PERFORMED: "A operação \"{op}\" não foi executada pois o processoo {pid} encerrou antes",
    MAX_FILA_PROCESSOS_REACHED: "O processoo {pid} não pode ser inserido na fila pois sua capacidade máxima foi atingida {max_size}",
    BLOCKED_DUE_MEMORIA: "\n\ndispatcher => O processoo {pid} foi bloqueado (não conseguiu ser alocado na memória).",
}

SUCCESS_MESSAGES = {
    SUCCESSFUL_REMOVE_ARQUIVO: "\tSistema de arquivo => O processoo {pid} deletou o arquivo {arquivonome}.",
    SUCCESSFUL_CREATE_ARQUIVO: "\tSistema de arquivo => O processoo {pid} criou o arquivo {arquivonome} (blocos {' '.join(block_range)}).",
}

LOG_MESSAGES = {
    START_PROCESSO: "\n\ndispatcher => {processo} \nprocesso {pid} => \nP{pid} STARTED",
    PROCESSO_INSTRUCTION: "P{pid} instruction {op}",
    PROCESSO_RETURN_SIGINT: "P{pid} return SIGINT",
}

DEBUG_MESSAGES = {
    DEALLOCATED_RECURSOS: 'desalocou gerenciador_recursos',
    WAITING_FOR_RT_PROCESSO: 'esperando por processoo rt...',
    WAITING_FOR_USUARIOS_PROCESSO: 'esperando por processoo usuario...',
    BLOCKED_PROCESSO: 'processoo bloqueou',
    DEBUG_MODE_ON: Fore.GREEN + 'DEGUB MODE ON' + Fore.RESET,
    DOWN_PROCESSO: Fore.BLUE + 'processo {pid} desceu para fila {fila}' + Fore.RESET,
    UP_PROCESSO: Fore.BLUE + 'processo {pid} subiu para fila {fila}' + Fore.RESET,
}

MAX_SIZE = 100

ERROR_COLOR = 'RED'
SUCCESS_COLOR = 'GREEN'
LOG_COLOR = 'MAGENTA'
DEBUG_COLOR = 'YELLOW'

RESET_TEXT = Fore.RESET
