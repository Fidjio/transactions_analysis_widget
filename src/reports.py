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


def get_reports_dec(name_file="reports.json"):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                logger.info(f"Декоратор начал работу с заданным именем файла {name_file}")
                data = func(*args, **kwargs)
                path_to_file = os.path.join(os.path.abspath("reports/"), name_file)
                with open(path_to_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                logger.info("Запись файла закончена!")
                return data
            except Exception as ex:
                logger.error(f"Произошла ошибка в декораторе при работе с функцией {func.__name__}: {ex}")
                return None

        return inner
    return wrapper


@get_reports_dec()
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
