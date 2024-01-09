import requests
from bs4 import BeautifulSoup


def get_coin_info(user_coin_name):
    try:
        url = f'https://coinmarketcap.com/currencies/{user_coin_name}/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        req = requests.get(url, headers=headers).text
        bs = BeautifulSoup(req, 'lxml')

        coin_info = bs.find('h1', class_="sc-f70bb44c-0 gYiXVQ").text.split()
        coin_price = float(
            bs.find('span', class_="sc-f70bb44c-0 jxpCgO base-text").text.replace('$', '').replace(',', ''))
        coin_name = coin_info[0]
        coin_symbol = coin_info[2]
        return coin_name, coin_symbol, coin_price
    except AttributeError:
        return False

