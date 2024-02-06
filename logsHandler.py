import logging
from logging.handlers import TimedRotatingFileHandler
import os
import random
from datetime import date, datetime
from dotenv import load_dotenv

load_dotenv()

log_file_path = os.getenv("LOG_FILE_PATH")
log_file_name = os.getenv("LOG_FILE_NAME")
logger_enable = bool(os.getenv("LOGGER_ENABLE"))
global logger

def stamp():
    event_number = random.randint(1000000000, 9999999999)
    event_date = date.today()
    now = datetime.now()
    event_time = now.strftime("%H:%M:%S")
    log_str = f"{event_date} {event_time}  Unique Id: {event_number}"
    return log_str

def file_creator(log_file_to_watch):
    global logger
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    if logger_enable:
        logger.disabled = True
    else:
        logger.disabled = False
    handler = TimedRotatingFileHandler(log_file_to_watch, when="midnight", interval=1, backupCount=5)
    logger.addHandler(handler)

def logw(logtype, message):
    list_ = os.listdir(log_file_path)
    if log_file_name not in list_:
        log_file_to_watch = os.path.join(log_file_path, log_file_name)  # Joining path components
        file_creator(log_file_to_watch)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    unique_string = stamp()  # You need to implement this function
    formatted_message = f"{timestamp} [{unique_string}] - {message}"

    if logtype == 'info':
        logger.info(formatted_message)
    elif logtype == 'error':
        logger.error(formatted_message, exc_info=True)
    elif logtype == 'warning':
        logger.warning(formatted_message)
    elif logtype == 'debug':
        logger.debug(formatted_message)

log_file_to_watch = os.path.join(log_file_path, log_file_name)  # Joining path components
file_creator(log_file_to_watch)
