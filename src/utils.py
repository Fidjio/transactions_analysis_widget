from typing import Any
import logging
import pandas as pd
from datetime import datetime

from pandas.core.interchange.dataframe_protocol import DataFrame
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


def open_xlsx_file(path: str) -> DataFrame | list[Any]:
    """ Открывает xlsx файл по пути и возвращает dataframe """
    try:
        logger.info(f"Открывается файл по пути {path}..")
        data = pd.read_excel(path)
        return data

    except Exception as ex:
        logger.error(f"Ошибка при открытии файла: {ex}")
        return []


def filter_by_date(df_transactions: DataFrame, user_date: str) -> list[Any] | Any:
    """Фильтрует транзакции по конечной дате (включая user_date)"""
    try:
        # Создаем копию DataFrame, чтобы не изменять исходные данные
        df_transactions = df_transactions.copy()
        logger.info("Преобразование столбца с датой полученного DataFrame..")
        # Преобразуем столбец с датой в datetime и устанавливаем его как индекс
        df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'],
                                                          dayfirst=True, format="%d.%m.%Y %H:%M:%S")
        df_transactions = df_transactions.set_index('Дата операции')

        logger.info("Сортировка индекса (индекс столбец с датами)")
        # Сортируем индекс для корректной работы срезов
        df_transactions = df_transactions.sort_index()

        logger.info("Преобразование полученной даты от пользователя в datetime")
        # Преобразуем user_date в datetime
        upper_date = pd.to_datetime(user_date, dayfirst=True, format="%d.%m.%Y %H:%M:%S")

        # Определение начальной даты для фильтрации
        start_date = upper_date.replace(day=1)  # 1-е число того же месяца

        logger.info("Фильтрация транзакций по диапазону от начала месяца до указанной даты")
        # Фильтруем транзакции от start_date до upper_date (включительно)
        filtered_df = df_transactions.loc[start_date:upper_date]
        return filtered_df

    except Exception as ex:
        logger.error(f"Ошибка при фильтрации по дате: {ex}")
        return []
