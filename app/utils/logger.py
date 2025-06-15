import logging
import inspect
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)
log_file = "logs/app.log"
file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d -> %(funcName)s()] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        file_handler
    ]
)

logger = logging.getLogger("LLM-App")

def log_info(message):
    frame = inspect.currentframe().f_back
    logger.info(f"{message}")

def log_error(message):
    frame = inspect.currentframe().f_back
    logger.error(f"{message}")

def log_debug(message):
    frame = inspect.currentframe().f_back
    logger.debug(f"{message}")
