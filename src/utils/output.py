from colorama import Fore
from utils.singleton import Singleton
from utils.messages import MENSAGENS_DE_ERRO, MENSAGENS_DE_SUCESSO, MENSAGENS_DE_LOG, MENSAGENS_DE_DEBUG, MAX_SIZE, COR_ERRO, COR_SUCESSO, COR_LOG, COR_DEBUG, RESET_TEXT

class Output(metaclass=Singleton):

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode

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

    def debug(self, code, *args, **kwargs):
        if not self.debug_mode:
            return

        self._print_message(code, MENSAGENS_DE_DEBUG, COR_DEBUG, **kwargs)
