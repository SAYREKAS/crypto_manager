import json
import time
import requests
from db import add_coin_to_db

coin_limit: int = 200
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
                f.write(req.text)
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


def check_for_exis_coin(coin_name_or_symbol):
    response()
    try:
        with open('coin info.json', 'r', encoding='utf8') as file:
            data: dict = json.load(file)
            for coin in data['data']['cryptoCurrencyList']:

                if coin['symbol'] == coin_name_or_symbol.upper() or coin['name'] == coin_name_or_symbol.capitalize():
                    add_coin_to_db(coin['name'])
                    return True
                else:
                    continue

            return False

    except KeyError:
        return False


def get_coin_info(coin_name_list):
    response()
    coin_data = []
    try:
        with open('coin info.json', 'r', encoding='utf8') as file:
            data: dict = json.load(file)
            for coin_info in data['data']['cryptoCurrencyList']:
                name = coin_info['name']
                symbol = coin_info['symbol']
                price = round(float(coin_info['quotes'][2]["price"]), 2)

                if name.lower() in coin_name_list:
                    coin_data.append({'name': name, 'symbol': symbol, 'price': price})

        return coin_data
    except KeyError:
        return []


def get_percent_change(coin_name):
    coin_data = ()
    with open('coin info.json', 'r', encoding='utf8') as file:
        data = json.load(file)
        for f in data["data"]["cryptoCurrencyList"]:

            if str(f['name']).lower() != str(coin_name).replace('_', ' ').lower():
                continue
            for n in f["quotes"]:
                if n['name'] != 'USD':
                    continue
                coin_data = (
                    round(float(n['percentChange1h']), 2),
                    round(float(n['percentChange24h']), 2),
                    round(float(n['percentChange7d']), 2),
                    round(float(n['percentChange30d']), 2),
                    round(float(n['percentChange60d']), 2),
                    round(float(n['percentChange90d']), 2),
                )
    return coin_data
