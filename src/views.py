import json
import logging
from pathlib import Path

from src.utils import (calculate_cashback, filter_by_date, get_dict_info_card, get_greeting, get_last_transactions,
                       get_now_currency, get_stock_prices, open_xlsx_file, read_json)

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler(Path(__file__).parent.parent / "logs" / "views.log", encoding="UTF-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s: modul - %(name)s, func:%(funcName)s --%(levelname)s--\n %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_info_for_page_main(date_user: str) -> str:
    """Функция для работы страницы Главная.
    Принимает дату и возвращает json-ответ"""
    try:
        logger.info("Чтение файла с транзакциями")
        data_transactions = open_xlsx_file(".//data//operations.xlsx")

        logger.info(f"Фильтрация данных по дате с помощью функции {filter_by_date.__name__}")
        filter_data = filter_by_date(data_transactions, date_user)

        logger.info("Преобразование данных в словарь")
        transactions = filter_data.to_dict("records")

        logger.info(f"Получение статистики по каждой карте с помощью функции {get_dict_info_card.__name__}")
        info_to_result = get_dict_info_card(transactions)

        logger.info("Получение настроек пользователя из файла user_settings.json")
        user_setting = read_json("data//user_settings.json")

        logger.info(f"Получение котировок валют с помощью функции {get_now_currency.__name__}")
        currency_rates = get_now_currency(user_setting.get("user_currencies"))

        logger.info(f"Получение словаря с акциями и их ценами с помощью функции {get_now_currency.__name__}")
        stock_prices = get_stock_prices(user_setting.get("user_stocks"))

        # Формируем итоговый JSON
        logger.info(
            f"Формирование списка словарей по картам (используются данные last_digits,"
            f"total и функция {calculate_cashback.__name__}"
        )
        cards = [
            {"last_digits": last_digits, "total_spent": round(total, 2), "cashback": calculate_cashback(total)}
            for last_digits, total in info_to_result.items()
        ]
        logger.info(f"Получение топа транзакций с помощью функции {get_last_transactions.__name__}")
        top_transactions = get_last_transactions(transactions)

        logger.info("Формирование конечного результата с помощью полученных данных")
        result = {
            "greeting": get_greeting(),
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }

        json_result = json.dumps(result, indent=4, ensure_ascii=False)
        return json_result

    except Exception as ex:
        logger.error(f"Ошибка при работе программы {ex}")
        return json.dumps({"error": str(ex)})
