# messages.py
from colorama import Fore

# ERROR CODES
NOT_ENOUGH_MEMO = 1                      # memory does not have space
NOT_ENOUGH_SPACE = 2                     # disk does not have space
NO_PERMISSION_REMOVE_FILE = 3           # does not have permission
INEXISTENT_REMOVE_FILE = 4              # file does not exist
EXCEEDED_RESOURCES = 5                  # system does not have the requested number of resources
BLOCKED_DUE_RESOURCES = 6               # process was blocked due to can't get requested resources
OPERATION_NOT_PERFORMED = 17            # process cycle number is less than the number of operations
MAX_PROCESSES_QUEUE_REACHED = 20        # max process queue size reached
BLOCKED_DUE_MEMORY = 21                 # process was blocked due to can't allocate memory

# SUCESSFUL MESSAGES
SUCCESSFUL_REMOVE_FILE  = 7              # file deleted successfully
SUCCESSFUL_CREATE_FILE = 8               # file created successfully

# LOG MESSAGES
START_PROCESS = 9                       # 
PROCESS_INSTRUCTION = 10
PROCESS_RETURN_SIGINT = 11

# DEBUG MESSAGES
DEALLOCATED_RESOURCES = 12
WAITING_FOR_RT_PROCESS = 13
WAITING_FOR_USER_PROCESS = 14
BLOCKED_PROCESS = 15
DEBUG_MODE_ON = 16
DOWN_PROCESS = 18
UP_PROCESS = 19

# Mapeamento de códigos para mensagens de erro
ERROR_MESSAGES = {
    NOT_ENOUGH_MEMO: "\n\ndispatcher => O processo {pid} não pode ser alocado na memória por falta de espaço",
    NOT_ENOUGH_SPACE: "\tSistema de arquivo => O processo {pid} não pode criar o arquivo {filename} (falta de espaço).",
    NO_PERMISSION_REMOVE_FILE: "\tSistema de arquivo => O processo {process.pid} não pode deletar o arquivo {filename} (sem permissão).",
    INEXISTENT_REMOVE_FILE: "\tSistema de arquivo => O processo {pid} não pode deletar o arquivo {filename} porque ele não existe.",
    EXCEEDED_RESOURCES: "\n\ndispatcher => O processo {pid} não conseguiu ser criado (recursos insuficientes)",
    BLOCKED_DUE_RESOURCES: "\n\ndispatcher => O processo {pid} foi bloqueado (não conseguiu obter {resource} - requisitado: {proc_quantity} (disponível {max_quantity_remaning})).",    OPERATION_NOT_PERFORMED: "A operação \"{op}\" não foi executada pois o processo {pid} encerrou antes",
    MAX_PROCESSES_QUEUE_REACHED: "O processo {pid} não pode ser inserido na fila pois sua capacidade máxima foi atingida {max_size}",
    BLOCKED_DUE_MEMORY: "\n\ndispatcher => O processo {pid} foi bloqueado (não conseguiu ser alocado na memória).",
}

# Mapeamento de códigos para mensagens de sucesso
SUCCESS_MESSAGES = {
    SUCCESSFUL_REMOVE_FILE: "\tSistema de arquivo => O processo {pid} deletou o arquivo {filename}.",
    SUCCESSFUL_CREATE_FILE: "\tSistema de arquivo => O processo {pid} criou o arquivo {filename} (blocos {' '.join(block_range)}).",
}

# Mapeamento de códigos para mensagens de log
LOG_MESSAGES = {
    START_PROCESS: "\n\ndispatcher => {process} \nprocess {pid} => \nP{pid} STARTED",
    PROCESS_INSTRUCTION: "P{pid} instruction {op}",
    PROCESS_RETURN_SIGINT: "P{pid} return SIGINT",
}

# Mapeamento de códigos para mensagens de debug
DEBUG_MESSAGES = {
    DEALLOCATED_RESOURCES: 'desalocou recursos',
    WAITING_FOR_RT_PROCESS: 'esperando por processo rt...',
    WAITING_FOR_USER_PROCESS: 'esperando por processo usuario...',
    BLOCKED_PROCESS: 'processo bloqueou',
    DEBUG_MODE_ON: Fore.GREEN + 'DEGUB MODE ON' + Fore.RESET,
    DOWN_PROCESS: Fore.BLUE + 'process {pid} desceu para fila {queue}' + Fore.RESET,
    UP_PROCESS: Fore.BLUE + 'process {pid} subiu para fila {queue}' + Fore.RESET,
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
