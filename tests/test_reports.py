from src.reports import spending_by_category


def test_spending_by_category_basic(sample_transactions):
    """Тест базового случая работы функции"""
    result = spending_by_category(sample_transactions, "Еда", "01.05.2023")
    assert isinstance(result, str)  # Проверяем, что возвращается строка (json)
    assert len(result) > 0  # Проверяем, что результат не пустой

def test_spending_by_category_date_none(sample_transactions):
    """Тест работы функции без указания даты"""
    result = spending_by_category(sample_transactions, "Еда")
    assert isinstance(result, str)
    assert len(result) > 0

def test_spending_by_category_with_nan(sample_transactions_with_nan):
    """Тест работы функции с NaN значениями"""
    result = spending_by_category(sample_transactions_with_nan, "Еда", "01.05.2023")
    assert isinstance(result, str)
    assert len(result) > 0

def test_spending_by_category_empty_result(sample_transactions):
    """Тест случая, когда нет подходящих транзакций"""
    result = spending_by_category(sample_transactions, "Несуществующая категория", "01.05.2023")
    assert result == []  # Проверяем пустой JSON-массив

def test_spending_by_category_invalid_date_format(sample_transactions):
    """Тест обработки неверного формата даты"""
    result = spending_by_category(sample_transactions, "Еда", "2023-05-01")
    assert result == '', "Ожидалась пустая строка при неверном формате даты"