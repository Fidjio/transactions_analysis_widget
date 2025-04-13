import pytest
import json

from src.services import search_name


def test_search_name_basic(sample_transactions_for_services):
    """Тест базового случая работы функции"""
    result = search_name(sample_transactions_for_services)
    data = json.loads(result)

    assert isinstance(result, str)  # Проверяем что возвращается строка
    assert len(data) == 3  # Ожидаем 3 подходящих транзакции
    assert all(t["Категория"] == "переводы" for t in data)  # Все категории - переводы
    assert all("." in t["Описание"] or " " in t["Описание"] for t in data)  # Проверка формата описания


def test_search_name_empty_input(empty_transactions):
    """Тест с пустым входным списком"""
    result = search_name(empty_transactions)
    assert result == "[]"  # Ожидаем пустой JSON-массив


def test_search_name_invalid_data_types():
    """Тест с некорректными типами данных"""
    invalid_data = [
        {"Категория": 123, "Описание": "Иванов И.И."},  # Числовая категория
        {"Категория": "переводы", "Описание": None},  # None в описании
        "not a dictionary",  # Не словарь
    ]
    result = search_name(invalid_data)
    data = json.loads(result)
    assert len(data) == 0  # Ожидаем пустой результат


def test_search_name_missing_fields():
    """Тест с отсутствующими полями"""
    incomplete_data = [
        {"Описание": "Иванов И.И."},  # Нет категории
        {"Категория": "переводы"},  # Нет описания
        {},  # Пустой словарь
    ]
    result = search_name(incomplete_data)
    data = json.loads(result)
    assert len(data) == 0  # Ожидаем пустой результат
