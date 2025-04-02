import json
from datetime import datetime
import requests  # Для запросов к API курсов валют и акций


def get_greeting(time_str):
    """Возвращает приветствие в зависимости от времени."""
    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").time()
    hour = time.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
