import json
import logging
import os
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from dateutil.relativedelta import relativedelta


logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'reports.log', encoding="UTF-8", mode="w")
file_formatter = logging.Formatter('%(asctime)s: modul - %(name)s, func:%(funcName)s --%(levelname)s--\n %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> str | Any:
    """ Функция возвращает траты по заданной категории за последние три месяца (от переданной даты). """
    try:
        logger.info("Функция начала работу")
        df_transaction = transactions.copy()

        logger.info("Конвертирование столбца dataframe['Дата платежа'] из строки в datatime")
        df_transaction["Дата платежа"] = pd.to_datetime(df_transaction["Дата платежа"], format='%d.%m.%Y', dayfirst=True)

        if not date:
            date_now = datetime.now()
            date_obj = date_now.strftime("%d.%m.%Y")
            use_date = datetime.strptime(date_obj, "%d.%m.%Y").replace()
            logger.info("Установлена дата 'Сегодня'")

        else:
            use_date = datetime.strptime(date, "%d.%m.%Y").replace()
            logger.info(f"Установлена дата полученная от пользователя '{use_date}'")

        start_date = use_date - relativedelta(months=3)
        end_date = use_date.replace()
        # Фильтруем dataframe на диапазон дат в 3 месяца

        filtered = df_transaction[(df_transaction["Дата платежа"] >= start_date) &
                                (df_transaction["Дата платежа"] <= end_date)]
        logger.info("DataFrame отфильтрован по диапазону дат")

        # Удаляем все значения NaN из df если такие имеются
        filtered.loc[:, "Сумма операции"] = filtered["Сумма операции"].fillna(0)
        logger.info("Удалены все значения NaN из DataFrame")

        result = filtered[(filtered["Категория"].str.lower() == category.lower())]
        logger.info(f"DataFrame отфильтрован по категории '{category}'")

        # Конвертируем df в json
        json_str = result.to_json(
            orient='records',  # Формат вывода
            force_ascii=False,  # Сохраняем кириллицу
            indent=4  # Красивое форматирование (опционально)
        )
        logger.info("DataFrame конвертирован в json для возврата результата функции")

        return json_str

    except Exception as ex:
        logger.error(f"Ошибка в работе функции: {ex}")
        return ""
