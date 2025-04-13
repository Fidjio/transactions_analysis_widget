import logging
import re
import json
from pathlib import Path

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler(Path(__file__).parent.parent / "logs" / "services.log", encoding="UTF-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s: modul - %(name)s, func:%(funcName)s --%(levelname)s--\n %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_name(list_dict_t):
    """Фильтрует список транзакций, оставляя только переводы от физ. лиц (с именем и инициалом в описании),
    и возвращает результат в формате JSON."""
    logger.info("Проверка на наличие переданных данных")
    if not list_dict_t:
        return json.dumps([], ensure_ascii=False, indent=4)  # Пустой JSON-массив

    pattern = re.compile(r"(?<!\S)[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.\s?[А-ЯЁ]\.?(?!\S)", re.IGNORECASE)
    filtered_transactions = []
    logger.info("Начало работы функции по поиску имени в транзакции")
    for transaction in list_dict_t:
        try:
            if not isinstance(transaction.get("Категория"), (float, type(None))):
                logger.info("Получение категории из списка транзакций")
                category = transaction.get("Категория", "").lower()

                logger.info("Получение описания из списка транзакций")
                description = str(transaction.get("Описание", ""))

                if category == "переводы" and pattern.search(description):
                    logger.info("Добавление подходящих данных под запрос в список")
                    filtered_transactions.append(transaction)

        except (AttributeError, KeyError) as ex:
            logger.error(f"Ошибка в обработке транзакций {ex}")
            print(f"Ошибка в обработке транзакции: {transaction}. Ошибка: {ex}")
            continue

    return json.dumps(filtered_transactions, ensure_ascii=False, indent=4)
