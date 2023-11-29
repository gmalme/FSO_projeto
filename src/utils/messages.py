from colorama import Fore,Back,Style
RESET_TEXT = Fore.RESET + Back.RESET + Style.RESET_ALL
ERRO_PADRAO = Style.DIM + Back.WHITE + "\tErro | Processoo: {pid} "
SUCESSO_PADRAO = Back.WHITE + "\tSucesso | Processoo: {pid} "

ERRO_SEM_MEMORIA = 1                      
ERRO_SEM_DISCO = 2                     
ERRO_SEM_PERMISSAO = 3           
ERRO_ARQUIVO_INEXISTENTE = 4              
ERRO_SEM_RECURSOS = 5                  
ERRO_RECURSO_BLOQUEADO = 6               
ERRO_OPERACAO_BLOQUEADA = 17            
ERRO_FILA_CHEIA = 20        
ERRO_PROCESSO_BLOQUEADO = 21                 

SUCESSO_ARQUIVO_REMOVIDO  = 7              
SUCESSO_ARQUIVO_CRIADO = 8               

START_PROCESSO = 9                       
PROCESSO_INSTRUCTION = 10
PROCESSO_RETURN_SIGINT = 11

RECURSO_LIBERADO = 12
ESPERANDO_PROCESSO_TR = 13
ESPERANDO_PROCESSO_USUARIO = 14
PROCESSO_BLOQUEADO = 15
DEBUG_MODE_ON = 16
PROCESSO_DECREMENTADO = 18
PROCESSO_INCRIMENTADO = 19

ERROR_MESSAGES = {
    ERRO_SEM_MEMORIA: ERRO_PADRAO + "(falta de espaço) - não há espaço na memoria para alocar o processo.",
    ERRO_SEM_DISCO: ERRO_PADRAO + "(falta de espaço) - não há espaço no disco para alocar o arquivo {arquivonome}.",
    ERRO_SEM_PERMISSAO: ERRO_PADRAO + "(sem permissão) - não tem permissão para deletar o arquivo {arquivonome}.",
    ERRO_ARQUIVO_INEXISTENTE: ERRO_PADRAO + "(arquivo não localizado) - o arquivo {arquivonome} não foi localizado.",
    ERRO_SEM_RECURSOS: ERRO_PADRAO + "(recursos insuficientes) - não foi criado por falta de recursos.",
    ERRO_RECURSO_BLOQUEADO: ERRO_PADRAO + "(foi bloqueado) - não conseguiu obter {recurso} - requisitado: {proc_quantity} (disponível {max_quantity_remaning}).",   
    ERRO_OPERACAO_BLOQUEADA: "Erro | Operação: \"{op}\" não foi executada pois o processoo {pid} encerrou antes",
    ERRO_FILA_CHEIA: ERRO_PADRAO + "(fila cheia) - não pode ser inserido na fila pois sua capacidade máxima foi atingida {max_size}",
    ERRO_PROCESSO_BLOQUEADO: ERRO_PADRAO + "(não conseguiu ser alocado na memória) - foi bloqueado.",
}

SUCCESS_MESSAGES = {
    SUCESSO_ARQUIVO_REMOVIDO: SUCESSO_PADRAO + "deletou o arquivo {arquivonome}.",
    SUCESSO_ARQUIVO_CRIADO: SUCESSO_PADRAO + "criou o arquivo {arquivonome} ).",
}

LOG_MESSAGES = {
    START_PROCESSO: "\n\tIdentificador: \n" + Style.DIM + Back.BLUE + "{processo}" + RESET_TEXT + "\nprocesso {pid} => \nP{pid} INICIADO",
    PROCESSO_INSTRUCTION: "Processo: {pid} Operação {op}",
    PROCESSO_RETURN_SIGINT: "Processo: {pid} FINALIZADO",
}

DEBUG_MESSAGES = {
    RECURSO_LIBERADO: 'desalocou gerenciador recursos',
    ESPERANDO_PROCESSO_TR: 'esperando por processo de tempo real...',
    ESPERANDO_PROCESSO_USUARIO: 'esperando por processo de usuario...',
    PROCESSO_BLOQUEADO: 'processo foi bloqueado',
    DEBUG_MODE_ON: Fore.GREEN + 'DEGUB MODE ON' + RESET_TEXT,
    PROCESSO_DECREMENTADO: Fore.BLUE + 'processo {pid} desceu para fila {fila}' + RESET_TEXT,
    PROCESSO_INCRIMENTADO: Fore.BLUE + 'processo {pid} subiu para fila {fila}' + RESET_TEXT,
}

MAX_SIZE = 100

ERROR_COLOR = 'RED'
SUCCESS_COLOR = 'GREEN'
LOG_COLOR = 'MAGENTA'
DEBUG_COLOR = 'CYAN'
