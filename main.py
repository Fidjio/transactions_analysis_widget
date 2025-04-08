import logging

from src.reports import spending_by_category
from src.services import search_name
from src.utils import open_xlsx_file
from src.views import get_info_for_page_main

logging.basicConfig(handlers=[])

if __name__ == "__main__":
    # # Запуск кода основной страницы
    # print(get_info_for_page_main("20.12.2021 01:23:41"))

    # Открытие файла с транзакциями для передачи в функции reports и services
    df_transactions = open_xlsx_file(".\\data\\operations.xlsx")

    # Запуск функции, которая фильтрует транзакции оставляя переводы только от физ лиц
    search_name(df_transactions.to_dict("records"))

    # Запуск функции, которая возвращает транзакции по определенной категории за определенный период времени
    spending_by_category(df_transactions, "Переводы", "31.12.2021")
