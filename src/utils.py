import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas.core.interchange.dataframe_protocol import DataFrame

log_file = Path(__file__).parent.parent / "logs" / "utils.log"
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

logger.propagate = False
file_handler = logging.FileHandler(log_file, encoding="UTF-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s: modul - %(name)s, func:%(funcName)s --%(levelname)s--\n %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greeting() -> str:
    """В зависимости от времени суток выдает приветствие"""
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
    """Открывает xlsx файл по пути и возвращает dataframe"""
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
        df_transactions["Дата операции"] = pd.to_datetime(
            df_transactions["Дата операции"], dayfirst=True, format="%d.%m.%Y %H:%M:%S"
        )
        df_transactions = df_transactions.set_index("Дата операции")

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
    """Извлекает последние 4 цифры из номера карты"""
    try:
        logger.info("Извлечение последних 4 цифр карты")
        return str(card_num)[-4:]

    except Exception as ex:
        logger.error(f"Ошибка извлечения последних цифр карты: {ex}")
        return ""


def calculate_cashback(amount: float) -> float:
    """Высчитывает кэшбэк от суммы операции (1%)"""
    try:
        logger.info("Расчет кэшбека за операцию")
        result = round(amount * 0.01, 2)
        return result

    except Exception as ex:
        logger.error(f"Ошибка расчета кэшбека {ex}")
        return 0


def get_dict_info_card(list_transactions: list[dict]) -> dict:
    """Получает транзакцию и формирует статистику по каждой карте в виде словаря"""
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


def get_last_transactions(list_transactions: list[dict]) -> list[dict]:
    """Формирует последние 5 операций по картам из заданного словаря"""
    i = 0

    result = []
    logger.info("Сортировка словаря по дате платежа")
    try:
        sorted_transactions = sorted(list_transactions, key=lambda x: x["Дата платежа"], reverse=True)

        logger.info("Формирование словаря со статистиками карт")
        for transaction in sorted_transactions:
            if i < 5:
                i += 1
                logger.info("Получение данных для формирования словаря")
                answer_dict = {
                    "date": transaction.get("Дата платежа"),
                    "amount": transaction.get("Сумма операции с округлением"),
                    "category": transaction.get("Категория"),
                    "description": transaction.get("Описание"),
                }
                result.append(answer_dict)
                logger.info("В словарь добавлены статистики по карте")

        return result
    except Exception as ex:
        logger.error(f"Ошибка формирования последних 5ти операций: {ex}")
        return []


def get_now_currency(list_currency: List[str]) -> Union[List[Dict[str, Union[str, float]]], str]:
    """Использует API для получения актуальных котировок валют по отношению к рублю"""
    try:
        load_dotenv()
        API_KEY_FOR_APILAYER = os.getenv("API_KEY_FOR_APILAYER")

        logger.info("Формирует строку из полученного списка с именами котировок")
        str_symbols = ", ".join(list_currency)
        return_currency = []
        url = "https://api.apilayer.com/exchangerates_data/latest"

        params = {"base": "RUB", "symbols": str_symbols}  # Базовая валюта: рубль  # Валюты для сравнения

        headers = {"apikey": API_KEY_FOR_APILAYER}  # Передаём ключ в заголовках

        try:
            logger.info(f"Запрос на получения данных с API {url}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP

            logger.info("Запись полученной информации в формате json")
            data = response.json()

            # Выводим курсы
            logger.info("Вывод курсов валют")
            for currency, rate in data["rates"].items():
                result = {"currency": currency, "rate": round(1 / rate, 2)}  # Конвертируем в "1 USD = X RUB"
                return_currency.append(result)
                logger.info("Добавление в список словаря с полученными курсами валют")

            return return_currency

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении данных с API {url}")
            return f"Ошибка запроса: {e}"

    except Exception as ex:
        logger.info(f"Ошибка при работе с получением или преобразованием курса валют: {ex}")
        return []


def read_json(path: str) -> Any:
    """Читает файл json и возвращает список словарей"""
    try:
        logger.info(f"Чтение файла json по пути {path}")
        with open(path, "r") as file:
            reader = json.load(file)
            return reader
    except Exception as ex:
        logger.error(f"Ошибка чтения файла json {ex}")
        return []


def get_stock_prices(list_stock: List[str]) -> List[Dict[str, Union[str, float]]]:
    """Принимает список названий акций и возвращает словарь с ценами"""
    try:
        result = []

        load_dotenv()
        API_KEY_FOR_ALFAVANTAGE = os.getenv("API_KEY_FOR_ALFAVANTAGE")

        logger.info("Формирование словаря с ценами на акции")
        for symbol in list_stock:
            url = (
                f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}"
                f"&apikey={API_KEY_FOR_ALFAVANTAGE}"
            )
            url_for_log = (
                f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}"
                f"&apikey=API_KEY_FOR_ALFAVANTAGE"
            )

            logger.info(f"Получение данных по запросу к API {url_for_log}")
            response = requests.get(url)

            logger.info("Запись полученных данных в json формате")
            data = response.json()

            logger.info("Формирование словаря с полученными значениями цен акций")
            tmp_dict_stocks = {"stock": symbol, "price": data["Global Quote"]["05. price"]}

            logger.info("Добавление словаря к возвращаемому результату")
            result.append(tmp_dict_stocks)

        return result
    except Exception as ex:
        logger.error(f"Ошибка при получении данных или формировании цен по акциям: {ex}")
        return []
