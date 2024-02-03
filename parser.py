import json
import time
import requests
from db import add_coin_to_db

coin_limit: int = 400
update_period: int = 60

url = (f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={coin_limit}&sortBy=market_cap'
       f'&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&audited=false')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/120.0.0.0 Safari/537.36'}

last_update: float = time.time() - update_period


def response():
    global last_update

    if time.time() - last_update >= update_period:
        req = requests.get(url, headers=headers)
        last_update = time.time()

        if req.status_code == 200:
            print(f"дані про монети отримано, статус код - {req.status_code}")
            with open('coin info.json', 'w', encoding='utf8') as f:
                json.dump(req.json(), f)
                print('файл перезаписано')
            return req.json()

        else:
            print(f"помилка при підключенні, статус код - {req.status_code}")
            with open('coin info.json', 'r', encoding='utf8') as f:
                data_file = json.load(f)
            return data_file

    else:
        print('час не прийшов')
        try:
            with open('coin info.json', 'r', encoding='utf8') as f:
                data_file = json.load(f)
            return data_file
        except FileNotFoundError:
            return {}


def check_for_exist_coin(coin_name_or_symbol):
    data = response()
    for coin in data.get('data', {}).get('cryptoCurrencyList', []):
        if coin['symbol'] == coin_name_or_symbol.upper() or coin['name'] == coin_name_or_symbol.capitalize():
            add_coin_to_db(coin['name'])
            return True
    return False


def get_coin_info(coin_name_list):
    percent_change = ()
    data = response()
    coin_data = []

    for coin_info in data.get('data').get('cryptoCurrencyList'):

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

    coin_data = sorted(coin_data, key=lambda x: x['name'])
    return coin_data
