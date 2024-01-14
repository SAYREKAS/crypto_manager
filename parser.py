import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_coin_info(coin_name_list):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for coin_name in coin_name_list:
                url = f'https://coinmarketcap.com/currencies/{coin_name}/'

                session.headers.update(headers)
                tasks.append(fetch(session, url))

            responses = await asyncio.gather(*tasks)
            coin_data = []
            for response in responses:
                bs = BeautifulSoup(response, 'lxml')
                coin_info = bs.find('h1', class_="sc-f70bb44c-0 gYiXVQ").text.split()
                coin_price = float(
                    bs.find('span', class_="sc-f70bb44c-0 jxpCgO base-text").text.replace('$', '').replace(',', ''))
                coin_name = coin_info[0]
                coin_symbol = coin_info[2]
                coin_data.append([coin_name, coin_symbol, coin_price])
            return sorted(coin_data)
    except Exception:
        return False


def check_for_exis_coin(coin_name):
    # парсимо Coin Market Cup на наявність монети, і отримуємо відповідь у вигляді True або False
    url = f'https://coinmarketcap.com/currencies/{coin_name}/'
    req = requests.get(url, headers=headers)
    if req:
        return True
    else:
        return False
# -------------------------------------------------------------------------------------------------------