import json
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest
from pandas import DataFrame

from src.utils import (
    calculate_cashback,
    filter_by_date,
    get_dict_info_card,
    get_greeting,
    get_last_digits,
    get_last_transactions,
    get_now_currency,
    get_stock_prices,
    open_xlsx_file,
    read_json,
)


# Тесты для get_greeting()
def test_get_greeting_morning():
    # Создаем mock-объект для datetime
    with patch("datetime.datetime") as mock_datetime:
        # Настраиваем mock чтобы now() возвращал нужное время
        mock_datetime.now.return_value = datetime(2023, 1, 1, 8, 0, 0)  # 8:00 утра
        assert get_greeting() == "Доброе утро"


# Тесты для open_xlsx_file()
def test_open_xlsx_file_success(tmp_path):
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    df.to_excel(test_file)
    result = open_xlsx_file(str(test_file))
    assert isinstance(result, DataFrame)
    assert not result.empty


def test_open_xlsx_file_failure():
    result = open_xlsx_file("nonexistent.xlsx")
    assert result == []


# Тесты для filter_by_date()
def test_filter_by_date_success(sample_transactions_for_utils):
    result = filter_by_date(sample_transactions_for_utils, "20.01.2023 00:00:00")
    assert len(result) == 2  # Должно вернуть 2 транзакции (1 и 15 января)


def test_filter_by_date_invalid_format(sample_transactions_for_utils):
    result = filter_by_date(sample_transactions_for_utils, "invalid-date")
    assert result == []


# Тесты для get_last_digits()
def test_get_last_digits_success():
    assert get_last_digits(1234567890) == "7890"


def test_get_last_digits_empty():
    assert get_last_digits("") == ""


# Тесты для calculate_cashback()
def test_calculate_cashback_normal():
    assert calculate_cashback(1000) == 10.0


def test_calculate_cashback_zero():
    assert calculate_cashback(0) == 0.0


# Тесты для get_dict_info_card()
def test_get_dict_info_card_success():
    transactions = [
        {"Номер карты": 1234567890, "Сумма операции с округлением": 100},
        {"Номер карты": 1234567890, "Сумма операции с округлением": 200},
        {"Номер карты": 9876543210, "Сумма операции с округлением": 300},
    ]
    result = get_dict_info_card(transactions)
    assert result == {"7890": 300.0, "3210": 300.0}


# Тесты для get_last_transactions()
def test_get_last_transactions():
    transactions = [
        {"Дата платежа": "01.01.2023", "Сумма операции с округлением": 100, "Категория": "A", "Описание": "Test1"},
        {"Дата платежа": "02.01.2023", "Сумма операции с округлением": 200, "Категория": "B", "Описание": "Test2"},
    ]
    result = get_last_transactions(transactions)
    assert len(result) == 2
    assert result[0]["date"] == "02.01.2023"


# Тесты для get_now_currency()
@patch("requests.get")
def test_get_now_currency_success(mock_get):
    mock_response = type(
        "MockResponse", (), {"json": lambda: {"rates": {"USD": 0.014, "EUR": 0.012}}, "raise_for_status": lambda: None}
    )
    mock_get.return_value = mock_response

    result = get_now_currency(["USD", "EUR"])
    assert len(result) == 2
    assert result[0]["currency"] == "USD"


# Тесты для read_json()
def test_read_json_success(tmp_path):
    test_file = tmp_path / "test.json"
    with open(test_file, "w") as f:
        json.dump([{"test": "data"}], f)
    result = read_json(str(test_file))
    assert result == [{"test": "data"}]


# Тесты для get_stock_prices()
@patch("requests.get")
def test_get_stock_prices_success(mock_get):
    mock_response = type(
        "MockResponse",
        (),
        {"json": lambda: {"Global Quote": {"05. price": "150.50"}}, "raise_for_status": lambda: None},
    )
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == "150.50"
