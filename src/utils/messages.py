# messages.py
from colorama import Fore

# ERROR CODES
NOT_ENOUGH_MEMO = 1                      # memoria does not have space
NOT_ENOUGH_SPACE = 2                     # disco does not have space
NO_PERMISSION_REMOVE_ARQUIVO = 3           # does not have permission
INEXISTENT_REMOVE_ARQUIVO = 4              # arquivo does not exist
EXCEEDED_RECURSOS = 5                  # system does not have the requested number of recursos
BLOCKED_DUE_RECURSOS = 6               # processo was blocked due to can't get requested recursos
OPERACAO_NOT_PERFORMED = 17            # processo cycle number is less than the number of operations
MAX_FILA_PROCESSOS_REACHED = 20        # max processo fila size reached
BLOCKED_DUE_MEMORIA = 21                 # processo was blocked due to can't allocate memoria

# SUCESSFUL MESSAGES
SUCCESSFUL_REMOVE_ARQUIVO  = 7              # arquivo deleted successfully
SUCCESSFUL_CREATE_ARQUIVO = 8               # arquivo created successfully

# LOG MESSAGES
START_PROCESSO = 9                       #
PROCESSO_INSTRUCTION = 10
PROCESSO_RETURN_SIGINT = 11

# DEBUG MESSAGES
DEALLOCATED_RECURSOS = 12
WAITING_FOR_RT_PROCESSO = 13
WAITING_FOR_USUARIOS_PROCESSO = 14
BLOCKED_PROCESSO = 15
DEBUG_MODE_ON = 16
DOWN_PROCESSO = 18
UP_PROCESSO = 19

# Mapeamento de códigos para mensagens de erro
ERROR_MESSAGES = {
    NOT_ENOUGH_MEMO: "\n\ndispatcher => O processoo {pid} não pode ser alocado na memória por falta de espaço",
    NOT_ENOUGH_SPACE: "\tSistema de arquivo => O processoo {pid} não pode criar o arquivo {arquivonome} (falta de espaço).",
    NO_PERMISSION_REMOVE_ARQUIVO: "\tSistema de arquivo => O processoo {processo.pid} não pode deletar o arquivo {arquivonome} (sem permissão).",
    INEXISTENT_REMOVE_ARQUIVO: "\tSistema de arquivo => O processoo {pid} não pode deletar o arquivo {arquivonome} porque ele não existe.",
    EXCEEDED_RECURSOS: "\n\ndispatcher => O processoo {pid} não conseguiu ser criado (recursos insuficientes)",
    BLOCKED_DUE_RECURSOS: "\n\ndispatcher => O processoo {pid} foi bloqueado (não conseguiu obter {recurso} - requisitado: {proc_quantity} (disponível {max_quantity_remaning})).",    OPERACAO_NOT_PERFORMED: "A operação \"{op}\" não foi executada pois o processoo {pid} encerrou antes",
    MAX_FILA_PROCESSOS_REACHED: "O processoo {pid} não pode ser inserido na fila pois sua capacidade máxima foi atingida {max_size}",
    BLOCKED_DUE_MEMORIA: "\n\ndispatcher => O processoo {pid} foi bloqueado (não conseguiu ser alocado na memória).",
}

# Mapeamento de códigos para mensagens de sucesso
SUCCESS_MESSAGES = {
    SUCCESSFUL_REMOVE_ARQUIVO: "\tSistema de arquivo => O processoo {pid} deletou o arquivo {arquivonome}.",
    SUCCESSFUL_CREATE_ARQUIVO: "\tSistema de arquivo => O processoo {pid} criou o arquivo {arquivonome} (blocos {' '.join(block_range)}).",
}

# Mapeamento de códigos para mensagens de log
LOG_MESSAGES = {
    START_PROCESSO: "\n\ndispatcher => {processo} \nprocesso {pid} => \nP{pid} STARTED",
    PROCESSO_INSTRUCTION: "P{pid} instruction {op}",
    PROCESSO_RETURN_SIGINT: "P{pid} return SIGINT",
}

# Mapeamento de códigos para mensagens de debug
DEBUG_MESSAGES = {
    DEALLOCATED_RECURSOS: 'desalocou recursos',
    WAITING_FOR_RT_PROCESSO: 'esperando por processoo rt...',
    WAITING_FOR_USUARIOS_PROCESSO: 'esperando por processoo usuario...',
    BLOCKED_PROCESSO: 'processoo bloqueou',
    DEBUG_MODE_ON: Fore.GREEN + 'DEGUB MODE ON' + Fore.RESET,
    DOWN_PROCESSO: Fore.BLUE + 'processo {pid} desceu para fila {fila}' + Fore.RESET,
    UP_PROCESSO: Fore.BLUE + 'processo {pid} subiu para fila {fila}' + Fore.RESET,
}

# Constantes
MAX_SIZE = 100  # Exemplo de constante, ajuste conforme necessário

# Cores para mensagens
ERROR_COLOR = 'RED'
SUCCESS_COLOR = 'GREEN'
LOG_COLOR = 'MAGENTA'
DEBUG_COLOR = 'YELLOW'

# Texto de reset
RESET_TEXT = Fore.RESET
