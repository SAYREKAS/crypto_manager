import requests
from db import add_coin_to_db


def response():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                             '537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    url = (f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/'
           f'listing?start=1&limit=200&sortBy=market_cap&sortType=desc&convert=USD,BTC,'
           f'ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,'
           f'cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,'
           f'self_reported_circulating_supply,self_reported_market_cap')

    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        print(f"дані про монети отримано, статус код - {req.status_code}")
        return req.json()

    else:
        print(f"помилка при підключенні, статус код - {req.status_code}")


def check_for_exis_coin(coin_name_or_symbol):
    for coin in response()['data']['cryptoCurrencyList']:
        if coin['symbol'] == coin_name_or_symbol.upper() or coin['name'] == coin_name_or_symbol.capitalize():
            add_coin_to_db(coin['name'])
            return True
        else:
            continue
    return False


def get_coin_info(coin_name_list):
    coin_data = []

    for coin_info in response()['data']['cryptoCurrencyList']:
        name = coin_info['name']
        symbol = coin_info['symbol']
        price = round(float(coin_info['quotes'][2]["price"]), 2)

        if name.lower() in coin_name_list:
            coin_data.append({'name': name, 'symbol': symbol, 'price': price})

    return coin_data
