import requests
from fake_useragent import UserAgent
from db import add_coin_to_db

ua = UserAgent()
headers = {'User-Agent': ua.random}

url = (f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/'
       f'listing?start=1&limit=200&sortBy=market_cap&sortType=desc&convert=USD,BTC,'
       f'ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,'
       f'cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,'
       f'self_reported_circulating_supply,self_reported_market_cap')


def get_coin_info(coin_name_list):
    coin_data = []
    req = requests.get(url, headers=headers).json()

    for coin in req['data']['cryptoCurrencyList']:

        name = coin['name']
        symbol = coin['symbol']
        price = round(float(coin['quotes'][2]["price"]), 2)

        if name.lower() in coin_name_list:
            coin_data.append([name, symbol, price])

    return sorted(coin_data)


def check_for_exis_coin(coin_name_or_symbol):
    req = requests.get(url, headers=headers).json()

    for coin in req['data']['cryptoCurrencyList']:

        if coin['symbol'] == coin_name_or_symbol.upper() or coin['name'] == coin_name_or_symbol.capitalize():
            add_coin_to_db(coin['name'])
            return True

        else:
            continue

    return False
