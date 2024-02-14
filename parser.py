import json
import time
import requests
from db import add_coin_to_db

update_period = 120
coin_limit = 2500

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
            print(f'Наступне оновлення через {round(update_period - (time.time() - last_update))}сек.')
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
            for coin in data_file.get('data', {}).get('cryptoCurrencyList', []):
                if coin['symbol'] == coin_name_or_symbol.upper() or coin['name'] == coin_name_or_symbol.capitalize():
                    add_coin_to_db(coin['name'])
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


def get_coin_info(coin_name_list):
    """Читаємо json файл і дістаємо з нього необхідну інформацію, результат зберігаємо у вигляді списку з словниками:
    [{'name': 'bitcoin', 'symbol': 'btc', 'tags': [tag1, tag2],
    'price': '20000','percent_change': (1h, 24h, 7d, 30d, 60d, 90d)}]"""

    percent_change = ()
    coin_data = []

    try:
        with open('coin info.json', 'r', encoding='utf8') as file:
            data_file = json.load(file)
            for coin_info in data_file.get('data').get('cryptoCurrencyList'):

                for quota in coin_info["quotes"]:
                    if quota['name'] != 'USD':
                        continue
                    percent_change = (
                        round(float(quota['percentChange1h']), 2),
                        round(float(quota['percentChange24h']), 2),
                        round(float(quota['percentChange7d']), 2),
                        round(float(quota['percentChange30d']), 2),
                        round(float(quota['percentChange60d']), 2),
                        round(float(quota['percentChange90d']), 2),
                    )

                if coin_info['name'].lower() in coin_name_list:
                    coin_data.append(
                        {'name': coin_info['name'], 'symbol': coin_info['symbol'], 'tags': coin_info['tags'],
                         'price': round(float(coin_info['quotes'][2]["price"]), 2), 'percent_change': percent_change})

            file.close()
            return sorted(coin_data, key=lambda x: x['name'])

    except FileNotFoundError:
        with open('coin info.json', 'w', encoding='utf8') as file:
            file.close()
        return ()
    except json.decoder.JSONDecodeError:
        print('get_coin_info() - json.decoder.JSONDecodeError:')
        return ()
