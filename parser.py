import requests
from bs4 import BeautifulSoup


def get_coin_info(coin_name_list):
    list1 = []
    try:
        for f in coin_name_list:
            url = f'https://coinmarketcap.com/currencies/{f}/'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

            with requests.Session() as session:
                session.headers.update(headers)
                req = session.get(url).text
                bs = BeautifulSoup(req, 'lxml')

                coin_info = bs.find('h1', class_="sc-f70bb44c-0 gYiXVQ").text.split()
                coin_price = float(
                    bs.find('span', class_="sc-f70bb44c-0 jxpCgO base-text").text.replace('$', '').replace(',', ''))
                coin_name = coin_info[0]
                coin_symbol = coin_info[2]
                list1.append([coin_name, coin_symbol, coin_price])
        return sorted(list1)
    except AttributeError:
        return False


def check_for_exis_coin(coin_name):
    try:
        url = f'https://coinmarketcap.com/currencies/{coin_name}/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        req = requests.get(url, headers=headers).text
        bs = BeautifulSoup(req, 'lxml')
        coin_info = bs.find('h1', class_="sc-f70bb44c-0 gYiXVQ").text.split()
        return True
    except AttributeError:
        return False
