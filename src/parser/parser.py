import json
import time
import requests
from loguru import logger

from src.db.db import Db
from src.db.config import engine
from src.parser.common import CryptoResponse, Parser, PercentChange

# Конфігурація
UPDATE_PERIOD = 120
COIN_LIMIT = 1000

session = requests.Session()
last_update: float = time.time() - UPDATE_PERIOD

logger.info(f"Період оновлення даних про монети {UPDATE_PERIOD} сек.")


def fetch_coin_data() -> dict:
    """
    Виконує запит до API CoinMarketCup для отримання даних про монети.
    Повертає відповідь у форматі словника.
    """
    global last_update

    url = (
        f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={COIN_LIMIT}'
        f'&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&audited=false'
    )

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/120.0.0.0 Safari/537.36'}

    if time.time() - last_update < UPDATE_PERIOD:
        logger.info(f"Наступне оновлення через {UPDATE_PERIOD - (time.time() - last_update):.2f} сек.")
        return {}

    try:
        start = time.time()
        response = session.get(url, headers=headers)
        last_update = time.time()

        if response.status_code == 200:
            logger.info(f"Дані про монети оновлено за {time.time() - start:.2f} сек.")
            return response.json()
        else:
            logger.error(f"Помилка підключення: статус код {response.status_code}")
            return {}

    except requests.exceptions.ConnectionError:
        logger.error("Помилка з'єднання з API CoinMarketCup.")
        return {}


def save_coin_data_to_file(data: dict, filename: str = 'coin info.json'):
    """
    Зберігає дані в JSON файл.
    """
    if not data:
        logger.warning("Немає нових даних для збереження.")
        return

    try:
        with open(filename, 'w', encoding='utf8') as file:
            json.dump(data, file)
        logger.info(f"Дані успішно збережено у файл '{filename}'.")

    except Exception as e:
        logger.error(f"Помилка збереження даних у файл: {e}")


def load_coin_data_from_file(filename: str = 'coin info.json') -> dict:
    """
    Читає дані з JSON файлу та повертає у вигляді словника.
    """
    try:
        with open(filename, 'r', encoding='utf8') as file:
            return json.load(file)

    except FileNotFoundError:
        logger.warning(f"Файл '{filename}' не знайдено. Створюється новий файл.")
        with open(filename, 'w', encoding='utf8') as file:
            pass
        return {}

    except json.decoder.JSONDecodeError:
        logger.error(f"Помилка декодування JSON у файлі '{filename}'.")
        return {}


def check_for_exist_coin(coin_name_or_symbol: str) -> bool:
    """
    Перевіряє, чи існує монета за ім'ям або символом у збережених даних.
    """
    data_file = load_coin_data_from_file()
    if not data_file:
        return False

    all_data = CryptoResponse(**data_file)

    for coin in all_data.data.cryptoCurrencyList:
        if coin.symbol == coin_name_or_symbol.upper() or coin.name == coin_name_or_symbol.capitalize():
            Db(engine=engine).add_coin(coin.name)
            return True

    return False


def parse_percent_change(quotes) -> PercentChange | None:
    """
    Витягає дані відсоткових змін для валюти USD.
    """
    for quota in quotes:
        if quota.name == "USD":
            return PercentChange(
                percentChange1h=quota.percentChange1h,
                percentChange24h=quota.percentChange24h,
                percentChange7d=quota.percentChange7d,
                percentChange30d=quota.percentChange30d,
                percentChange60d=quota.percentChange60d,
                percentChange90d=quota.percentChange90d,
            )
    return None


def get_coin_info(coin_name_list: list) -> list[Parser]:
    """
    Читає дані з файлу та повертає список монет із зазначеної назви або символу.
    """
    coin_data = []
    data_file = load_coin_data_from_file()

    if not data_file:
        return coin_data

    all_data = CryptoResponse(**data_file)

    for coin_info in all_data.data.cryptoCurrencyList:
        percent_change = parse_percent_change(coin_info.quotes)

        if coin_info.name.lower() in coin_name_list:
            coin_data.append(
                Parser(
                    name=coin_info.name,
                    symbol=coin_info.symbol,
                    tags=coin_info.tags,
                    price=coin_info.quotes[2].price,
                    percent_change=percent_change,
                )
            )
    return coin_data


def response_update():
    """
    Безкінечний цикл для періодичного оновлення даних.
    """
    while True:
        data = fetch_coin_data()
        save_coin_data_to_file(data)
        time.sleep(1)
