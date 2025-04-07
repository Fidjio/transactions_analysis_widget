import logging

from datetime import datetime

from pathlib import Path


log_file = Path(__file__).parent.parent / 'logs' / 'utils.log'
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

logger.propagate = False
file_handler = logging.FileHandler(log_file, encoding="UTF-8", mode="w")
file_formatter = logging.Formatter('%(asctime)s: modul - %(name)s, func:%(funcName)s --%(levelname)s--\n %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greeting() -> str:
    """ В зависимости от времени суток выдает приветствие"""
    current_hour = datetime.now().hour
    logger.info("работает функция выбора приветственного сообщения")
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
