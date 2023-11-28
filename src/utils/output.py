from colorama import Fore
from utils.singleton import Singleton
from utils.messages import ERROR_MESSAGES, SUCCESS_MESSAGES, LOG_MESSAGES, DEBUG_MESSAGES, MAX_SIZE, ERROR_COLOR, SUCCESS_COLOR, LOG_COLOR, DEBUG_COLOR, RESET_TEXT

class Output(metaclass=Singleton):

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode

    def _print_colored(self,message, color):
        print(f"{getattr(Fore, color)}{message}{RESET_TEXT}")

    def _print_message(self, code, messages, color, **kwargs):
        msg = messages.get(code, '').format(**kwargs)
        self._print_colored(msg, color)

    def error(self, code, **kwargs):
        self._print_message(code, ERROR_MESSAGES, ERROR_COLOR, **kwargs)

    def success(self, code, **kwargs):
        self._print_message(code, SUCCESS_MESSAGES, SUCCESS_COLOR, **kwargs)

    def log(self, code, **kwargs):
        self._print_message(code, LOG_MESSAGES, LOG_COLOR, **kwargs)

    def debug(self, code, *args, **kwargs):
        if not self.debug_mode:
            return

        self._print_message(code, DEBUG_MESSAGES, DEBUG_COLOR, **kwargs)
