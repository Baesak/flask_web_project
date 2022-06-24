"""Logger setup."""

import logging
from sys import stdout

my_logger = logging.getLogger("__name__")
my_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs.log", "a")
stdout_handler = logging.StreamHandler(stream=stdout)

file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
stdout_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
my_logger.addHandler(file_handler)
my_logger.addHandler(stdout_handler)

