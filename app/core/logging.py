import logging
from logging.handlers import RotatingFileHandler
import os

# Make sure that log dir exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Config logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Format log
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    f"{LOG_DIR}/app.log", maxBytes=5*1024*1024, backupCount=3
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
