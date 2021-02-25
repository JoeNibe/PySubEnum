import logging
import sys


# Importing color module
try:
    from colorama import Fore, Style, init
    init()
except ImportError:
    print("[-]Import Error. Please install colorama Module. \n>pip install colorama")
    sys.exit(0)

"""
Default Logging Levels
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
"""

TEST_LEVEL_NUM = 60
RUN_LEVEL_NUM = 22
GOOD_LEVEL_NUM = 25
levels = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]

console_format = '%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
file_format = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'

logging.addLevelName(TEST_LEVEL_NUM, 'TEST')
logging.addLevelName(RUN_LEVEL_NUM, 'RUN')
logging.addLevelName(GOOD_LEVEL_NUM, 'GOOD')


def _test(self, msg, *args, **kwargs):
    if self.isEnabledFor(TEST_LEVEL_NUM):
        self._log(TEST_LEVEL_NUM, msg, args, **kwargs)


def _run(self, msg, *args, **kwargs):
    if self.isEnabledFor(RUN_LEVEL_NUM):
        self._log(RUN_LEVEL_NUM, msg, args, **kwargs)


def _good(self, msg, *args, **kwargs):
    if self.isEnabledFor(GOOD_LEVEL_NUM):
        self._log(GOOD_LEVEL_NUM, msg, args, **kwargs)


logging.Logger.test = _test
logging.Logger.run = _run
logging.Logger.good = _good

FORMATS = {
    "DEBUG": f"[*] {Fore.LIGHTBLACK_EX}{console_format}{Fore.RESET}",
    "INFO": f"[+] {Fore.GREEN}{console_format}{Fore.RESET}",
    "WARNING": f"[!] {Fore.LIGHTYELLOW_EX}{console_format}{Fore.RESET}",
    "ERROR": f"[-] {Fore.LIGHTRED_EX}{console_format}{Fore.RESET}",
    "CRITICAL": f"[--] {Fore.RED}{console_format}{Fore.RESET}",
    "TEST": f"[**] {Fore.LIGHTYELLOW_EX}{console_format}{Fore.RESET}",
    "RUN": f"[ ] {Fore.WHITE}%(message)s{Fore.RESET}",
    "GOOD": f"[++] {Fore.LIGHTGREEN_EX}%(message)s{Fore.RESET}"
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelname)
        formatter = logging.Formatter(log_fmt, datefmt='%d-%m-%Y %H:%M:%S')
        return formatter.format(record)


def setup_logger(filename="log", con_level=2, file_level=4):
    LOGGER = logging.getLogger(filename)
    LOGGER.setLevel(logging.DEBUG)

    fh = logging.StreamHandler()  # Console Logger
    fh_file = logging.FileHandler(filename+".txt")  # File Logger

    fh.setLevel(levels[con_level])  # Controls the console debug level
    fh_file.setLevel(levels[file_level])  # Controls the file debug level
    fh_file_formatter = logging.Formatter(file_format, datefmt='%d-%m-%Y %H:%M:%S')
    fh.setFormatter(CustomFormatter())
    fh_file.setFormatter(fh_file_formatter)
    LOGGER.addHandler(fh)
    LOGGER.addHandler(fh_file)
    LOGGER.debug("-"*100)
    return LOGGER


def print_status(complete, total, text="", n_bar=50):
    percent = (complete/total) * n_bar
    display_text = f"{Fore.LIGHTGREEN_EX}{complete} Completed {Fore.RED}{total-complete} Remaining" + text
    sys.stdout.write(f"\r{Fore.CYAN}[{Fore.LIGHTGREEN_EX}"
                     f"{'=' * int(percent) + Fore.LIGHTYELLOW_EX + '>' * int(1-(percent//100)):{n_bar + 5}s}"
                     f"{Fore.CYAN}]{Fore.WHITE}{int(percent/n_bar*100)}%  {display_text}{Fore.RESET}          ")


if __name__ == "__main__":
    setup_logger()
