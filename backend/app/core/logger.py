import logging
import os
from logging.handlers import RotatingFileHandler

# LOG DIRECTORY

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "phema.log")

# FORMATTER

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# CONSOLE HANDLER

console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# FILE HANDLER (ROTATING)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,   # 5 MB
    backupCount=3
)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# MAIN LOGGER

logger = logging.getLogger("phema")

logger.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.propagate = False