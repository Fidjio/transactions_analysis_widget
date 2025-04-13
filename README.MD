# Приложение для анализа транзакций клиента
Приложение для анализа транзакций, которые находятся в Excel-файле. 
Приложение генерирует JSON-данные для веб-страниц,
формирует Excel-отчеты, а также предоставляет другие сервисы, такие как: 
- получение стоимости акций на текущий момент
- получение стоимости валют на текущий момент 

В каждую функцию добавлен logger для создания логов программы. Все логи хранятся 
в директории logs. \
Так же в директории reports хранятся json-ответы, которая выдает программа с помощью декоратора.

Виды обработки информации представлены ниже в разделе **"Реализованные функции"**. 
Запуск программы происходит через запуск main.py

## Статус проекта:
+ Статус разработки: готов.

## Технологии: 
+ Python
+ GitHub
+ PyCharm
+ logging

## Реализованные функции

### Модуль reports.py
1. ***get_reports_dec*** - декоратор, который записывает результат работы функции (json)
в файл, имя которого указывает пользователь в декораторе (по умолчанию reports.json.

2. ***spending_by_category*** - функция возвращает траты по заданной категории за последние 
три месяца (от переданной даты). Вызов функции:\
`spending_by_category(df_transactions, "Переводы", "31.12.2021")` -> Результат будет в json строке



### Модуль services.py
1. ***search_name*** - фильтрует список транзакций, оставляя только переводы от физ. лиц 
(с именем и инициалом в описании), и возвращает результат в формате JSON. Вызов функции:\
`search_name(df_transactions.to_dict("records"))` \
-> Возвращает список словарей json-формата, в котором содержаться только переводы физ. лиц.



### Модуль utils.py
1. ***get_greeting*** - в зависимости от времени суток выдает приветствие. Вызов функции:\
`print(get_greeting())`

2. ***open_xlsx_file*** - открывает xlsx файл по пути и возвращает dataframe. Вызов функции:\
`df_transactions = open_xlsx_file(".\\data\\operations.xlsx")` -> DataFrame

3. ***filter_by_date*** - фильтрует транзакции по конечной дате (включая user_date). 
Вызов функции:\
`filter_data = filter_by_date(data_transactions, date_user)` -> DataFrame_filtered

4. ***get_last_digits*** - извлекает последние 4 цифры из номера карты. Вызов функции:\
`get_last_digits(5555888877774444)` -> `4444`

5. ***calculate_cashback*** - высчитывает кэшбэк от суммы операции (1%). Вызов функции:\
`calculate_cashback(1000.00)` -> `10.0`

6. ***get_dict_info_card*** - получает транзакцию и формирует статистику по каждой карте 
в виде словаря. Вызов функции:\
`info_to_result = get_dict_info_card(transactions)` -> словарь с результатом статистики

7. ***get_last_transactions*** - формирует последние 5 операций по картам из заданного словаря. 
Вызов функции:\
`top_transactions = get_last_transactions(transactions)` -> последние 5 операций из полученного 
словаря.

8. ***get_now_currency*** - использует API для получения актуальных котировок валют 
по отношению к рублю. 
Вызов функции:\
`currency_rates = get_now_currency(user_setting.get("user_currencies"))`, где *user_currencies* - 
это отдельный файл json, в котором лежат котировки пользователя "user_currencies": ["USD", "EUR"].
\ результатом будет список словарей с валидными котировками для валют

9. ***read_json*** - читает файл json и возвращает список словарей. 
Вызов функции:\
`user_setting = read_json("data//user_settings.json")` -> list[dict]

10. ***get_stock_prices*** - принимает список названий акций и возвращает словарь с ценами. 
Вызов функции:\
`stock_prices = get_stock_prices(user_setting.get("user_stocks"))`, где *user_stocks* - 
это отдельный файл json, в котором лежат котировки пользователя "user_stocks": ["AAPL", "AMZN"].
\ результатом будет список словарей с валидными котировками для акций

### Модуль views.py
1. ***get_info_for_page_main*** - функция для работы страницы Главная.Данный модуль использует все функции из 
модуля utils.py для своей работы. Функция принимает дату и возвращает конечный результат 
работы в json-формате. Вызов функции:\
`print(get_info_for_page_main("20.12.2021 01:23:41"))`


## Добавлены тесты для pytest. Список тестов:
- Модуль test_reports.py
    - test_spending_by_category_basic
    - test_spending_by_category_date_none
    - test_spending_by_category_with_nan
    - test_spending_by_category_empty_result
    - test_spending_by_category_invalid_date_format
  
- Модуль test_services.py
    - test_search_name_basic
    - test_search_name_empty_input
    - test_search_name_invalid_data_types
    - test_search_name_missing_fields
  
- Модуль test_utils.py
    - test_get_greeting_morning
    - test_open_xlsx_file_success
    - test_open_xlsx_file_failure
    - test_filter_by_date_success
    - test_filter_by_date_invalid_format
    - test_get_last_digits_success
    - test_get_last_digits_empty
    - test_calculate_cashback_normal
    - test_calculate_cashback_zero
    - test_get_dict_info_card_success
    - test_get_last_transactions
    - test_get_now_currency_success
    - test_read_json_success
    - test_get_stock_prices_success

- Модуль test_views.py
    - test_get_info_for_page_main_with_invalid_date
    - test_get_info_for_page_main_with_future_date
    - test_get_info_for_page_main_with_missing_files


***Для хранения фикстур создан файл conftest.py***

***Для хранения секретных данных используейте .env.example, предварительно сменив расширение 
на .env.***


## Установка:
*Не требует обязательных условий.*
* Установить Poetry `pip install poetry`
* Установить завиcимости проекта.
+ Слить проект из GitHub https://github.com/Fidjio/transactions_analysis_widget
+ Запуск программы выполняестя из файла main.py в корне каталога *python main.py*


## Команда проекта
Сергей Карсканов - Junior Python developer
