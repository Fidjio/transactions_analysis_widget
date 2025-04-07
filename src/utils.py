
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


def get_last_digits(card_num: int) -> str:
    """ Извлекает последние 4 цифры из номера карты"""
    try:
        logger.info("Извлечение последних 4 цифр карты")
        return str(card_num)[-4:]

    except Exception as ex:
        logger.error(f"Ошибка извлечения последних цифр карты: {ex}")
        return ""


def calculate_cashback(amount: float) -> float:
    """ Высчитывает кэшбэк от суммы операции (1%)"""
    try:
        logger.info("Расчет кэшбека за операцию")
        result = round(amount * 0.01, 2)
        return result

    except Exception as ex:
        logger.error(f"Ошибка расчета кэшбека {ex}")
        return 0


def get_dict_info_card(list_transactions: list[dict]) -> dict:
    """ Получает транзакцию и формирует статистику по каждой карте в виде словаря"""
    card_totals = {}
    try:
        logger.info("Формирование статистики по каждой карте")
        for t in list_transactions:
            last_digits = get_last_digits(t["Номер карты"])
            logger.info("Получен номер карты")

            amount = t["Сумма операции с округлением"]
            logger.info("Получена сумма операции")

            if last_digits not in card_totals:
                card_totals[last_digits] = 0.0
            card_totals[last_digits] += amount
            logger.info("Карта добавлена в словарь")

        return card_totals

    except Exception as ex:
        logger.error(f"Ошибка получения статистики {ex}")
        return {}

