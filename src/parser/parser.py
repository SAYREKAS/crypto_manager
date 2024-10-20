import json
import time
from pprint import pprint

import requests
from loguru import logger

from src.db.config import engine
from src.db.db import Db
from src.parser.common import CryptoResponse, Parser, PercentChange

update_period = 120
coin_limit = 1000

session = requests.session()

last_update: float = time.time() - update_period

print(f"\nПеріод оновлення даних про монети {update_period}сек.\n")


def response():
    """Робимо запит до API CoinMarketCup щоб отримати словник з інформацією про монети та зберігаємо його в json файл.
    , У відповідь віддаємо json файл."""

    global last_update

    url = (
        f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={coin_limit}&sortBy=market_cap'
        f'&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&audited=false')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/120.0.0.0 Safari/537.36'}
    try:
        if time.time() - last_update >= update_period:
            start = time.time()
            req = session.get(url, headers=headers)
            last_update = time.time()

            if req.status_code == 200:
                print(f"Дані про монети оновлено {time.time() - start:.2f}сек.\n")
                with open('coin info.json', 'w', encoding='utf8') as file:
                    json.dump(req.json(), file)
                    file.close()
            else:
                print(f"Помилка при підключенні, статус код - {req.status_code}")
                with open('coin info.json', 'w', encoding='utf8') as file:
                    file.close()
        else:
            print(f'Наступне оновлення через {update_period - (time.time() - last_update)}сек.')
    except requests.exceptions.ConnectionError:
        print('connection lost')


def response_update():
    while True:
        response()
        time.sleep(1)


def check_for_exist_coin(coin_name_or_symbol):
    """Читаємо json файл та перевіряємо чи існує монета по імені або символу"""
    try:
        with open('coin info.json', 'r', encoding='utf8') as file:
            data_file = json.load(file)
            all_data = CryptoResponse(**data_file)

            for coin in all_data.data.cryptoCurrencyList:
                if coin.symbol == coin_name_or_symbol.upper() or coin.name == coin_name_or_symbol.capitalize():
                    Db(engine=engine).add_coin(coin.name)
                    file.close()
                    return True
            return False

    except FileNotFoundError:
        with open('coin info.json', 'w', encoding='utf8') as file:
            file.close()
            return ()

    except json.decoder.JSONDecodeError:
        print('check_for_exist_coin() - json.decoder.JSONDecodeError:')
        return ()


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
    Читаємо json файл і дістаємо з нього необхідну інформацію, результат зберігаємо у вигляді списку з словниками:
    [{'name': 'bitcoin', 'symbol': 'btc', 'tags': [tag1, tag2],
    'price': '20000','percent_change': (1h, 24h, 7d, 30d, 60d, 90d)}]
    """

    coin_data = []

    try:
        with open("coin info.json", "r", encoding="utf8") as file:
            data_file = json.load(file)
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

    except FileNotFoundError:
        logger.error("Файл 'coin info.json' не знайдено, створюємо новий.")
        with open("coin info.json", "w", encoding="utf8") as file:
            pass
        return []

    except json.decoder.JSONDecodeError:
        logger.error("Помилка декодування JSON у файлі 'coin info.json'.")
        return []


if __name__ == '__main__':
    pprint(get_coin_info(['bitcoin', 'cardano', 'ethereum', 'arbitrum', 'gfjdhj']))
