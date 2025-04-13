import json
import os
from datetime import datetime, timedelta

from src.views import get_info_for_page_main


def test_get_info_for_page_main_success(setup_test_environment, monkeypatch):
    # Мокируем API запросы, чтобы тесты не зависели от внешних сервисов
    def mock_get_now_currency(currencies):
        return [{"currency": "USD", "rate": 75.5}, {"currency": "EUR", "rate": 85.2}]

    def mock_get_stock_prices(stocks):
        return [{"stock": "IBM", "price": "120.50"}, {"stock": "AAPL", "price": "150.75"}]

    # Применяем моки
    monkeypatch.setattr("src.utils.get_now_currency", mock_get_now_currency)
    monkeypatch.setattr("src.utils.get_stock_prices", mock_get_stock_prices)

    # Устанавливаем текущую рабочую директорию на временную
    os.chdir(setup_test_environment)

    # Вызываем тестируемую функцию
    test_date = "31.01.2023 23:59:59"
    result = get_info_for_page_main(test_date)
    result_dict = json.loads(result)

    # Проверяем структуру ответа
    assert "greeting" in result_dict
    assert "cards" in result_dict
    assert "top_transactions" in result_dict
    assert "currency_rates" in result_dict
    assert "stock_prices" in result_dict

    # Проверяем данные по картам
    assert len(result_dict["cards"]) == 2  # Две карты в тестовых данных

    # Проверяем суммы и кэшбэк
    for card in result_dict["cards"]:
        if card["last_digits"] == "3456":
            assert card["total_spent"] == 2000.0
            assert card["cashback"] == 20.0  # 1% от 3000
        elif card["last_digits"] == "7654":
            assert card["total_spent"] == 3000.0
            assert card["cashback"] == 30.0

    # Проверяем топ транзакций
    assert len(result_dict["top_transactions"]) == 2  # Всего 2 транзакции в тестовых данных
    assert result_dict["top_transactions"][0]["amount"] == 3000.0  # Последняя транзакция

    # Проверяем курсы валют (из мока)
    assert len(result_dict["currency_rates"]) == 2
    assert result_dict["currency_rates"][0]["currency"] == "USD"

    # Проверяем цены акций (из мока)
    assert len(result_dict["stock_prices"]) == 0


def test_get_info_for_page_main_with_invalid_date(setup_test_environment):
    # Устанавливаем текущую рабочую директорию на временную
    os.chdir(setup_test_environment)

    # Вызываем тестируемую функцию с неверной датой
    invalid_date = "invalid_date"
    result = get_info_for_page_main(invalid_date)
    result_dict = json.loads(result)

    # Проверяем, что вернулась ошибка
    assert "error" in result_dict


def test_get_info_for_page_main_with_future_date(setup_test_environment):
    # Устанавливаем текущую рабочую директорию на временную
    os.chdir(setup_test_environment)

    # Дата в будущем
    future_date = (datetime.now() + timedelta(days=365)).strftime("%d.%m.%Y %H:%M:%S")
    result = get_info_for_page_main(future_date)
    result_dict = json.loads(result)

    # Проверяем, что вернулись данные (хотя бы greeting)
    assert "greeting" in result_dict
    # Карты должны быть пустыми или с нулевыми суммами
    assert len(result_dict["cards"]) == 0 or all(card["total_spent"] == 0 for card in result_dict["cards"])


def test_get_info_for_page_main_with_missing_files(setup_test_environment):
    # Удаляем файлы, чтобы проверить обработку ошибок
    os.remove(setup_test_environment / "data" / "operations.xlsx")

    # Устанавливаем текущую рабочую директорию на временную
    os.chdir(setup_test_environment)

    test_date = "31.01.2023 23:59:59"
    result = get_info_for_page_main(test_date)
    result_dict = json.loads(result)

    # Проверяем, что вернулась ошибка
    assert "error" in result_dict
