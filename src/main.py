import logging
from kernel.kernel import Kernel


def main():
    try:
        kernel = Kernel()
        kernel.executar()
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
