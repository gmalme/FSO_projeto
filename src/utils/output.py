from colorama import Fore
from utils.singleton import Singleton
from utils.messages import MENSAGENS_DE_ERRO, MENSAGENS_DE_SUCESSO, MENSAGENS_DE_LOG, MAX_SIZE, COR_ERRO, COR_SUCESSO, COR_LOG, RESET_TEXT

class Output(metaclass=Singleton):
    def _print_colored(self,message, color):
        print(f"{getattr(Fore, color)}{message}{RESET_TEXT}")

    def _print_message(self, code, messages, color, **kwargs):
        msg = messages.get(code, '').format(**kwargs)
        self._print_colored(msg, color)

    def error(self, code, **kwargs):
        self._print_message(code, MENSAGENS_DE_ERRO, COR_ERRO, **kwargs)

    def success(self, code, **kwargs):
        self._print_message(code, MENSAGENS_DE_SUCESSO, COR_SUCESSO, **kwargs)

    def log(self, code, **kwargs):
        self._print_message(code, MENSAGENS_DE_LOG, COR_LOG, **kwargs)