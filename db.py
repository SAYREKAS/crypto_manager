import datetime
import sqlite3


def create_db():
    db = sqlite3.connect('crypto_manager.db')
    pass


# додаємо монету в базу даних
def add_coin_to_db(coin_name):
    with sqlite3.connect('crypto_manager.db') as db:
        cursor = db.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {str(coin_name).lower().replace(' ', '_')} (id INTEGER PRIMARY KEY, DATE TEXT, TIME TEXT, BUY INTEGER, BUY_USD INTEGER, SELL INTEGER, SELL_USD INTEGER)")
        db.commit()
        if coin_name != 'tether':
            print(f"{str(coin_name).lower().replace(' ', '_')} додано в БД")


# видаляємо монету з бази даних
def dell_coin_in_db(coin_name):
    with sqlite3.connect('crypto_manager.db') as db:
        cursor = db.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {coin_name.replace(' ', '_')}")
        print(f"{coin_name.replace(' ', '_')} видалено з БД")


# Додаємо запис про купівлю чи продаж монети в БД
def by_or_sell_coin(coin_name, coin_amount, usd_amount, is_buy=True):
    with sqlite3.connect('crypto_manager.db') as db:
        cursor = db.cursor()
        if coin_amount.replace(',', '').replace('.', '').isdigit() and usd_amount.replace(',', '').replace('.',
                                                                                                           '').isdigit():
            date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            time = str(datetime.datetime.now().strftime("%H:%M"))
            buy_sell = "BUY" if is_buy else "SELL"
            cursor.execute(
                f"INSERT INTO {coin_name.replace(' ', '_')} (DATE, TIME, {buy_sell}, {buy_sell}_USD) VALUES (?, ?, ?, ?)",
                (date, time, float(coin_amount.replace(',', '.')), float(usd_amount.replace(',', '.'))))
            db.commit()
            print(f"{coin_name.replace(' ', '_')} {'куплено' if is_buy else 'продано'} {coin_amount} на {usd_amount}")


# отримуємо імена всіх криптовалют із БД в вигляді списка ['bitcoin', 'cardano', 'ethereum']
def get_all_coin_name():
    coin_name = []
    with sqlite3.connect('crypto_manager.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        for name in table_names:
            if 'tether' not in name:
                coin_name.append(str(*name).replace('_', ' '))
    return sorted(coin_name)


# отримуємо всі операції по всім монетам у вигляді словника типу {монета: [(операція1), (операція2),]}
def get_all_coin_operation():
    coin_dict = {}
    with sqlite3.connect('crypto_manager.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        for name in table_names:
            for item in name:
                coin_dict[item] = ''
                read_date = f"SELECT * FROM `{item}`"
                cursor.execute(read_date)
                rows = cursor.fetchall()
                operation = []
                for rows in rows:
                    operation.append(rows)
                    coin_dict[item] = operation
    return coin_dict


# отримуємо всі операції по конкретній монеті
def get_curent_coin_operation(coin_name):
    main_list = []
    item = get_all_coin_operation()[coin_name.replace(' ', '_')]
    for f in item:
        main_list.append(f)
    return main_list


# видаляємо запис про купівлю/продаж по айді операції
def del_curent_coin_operation(coin_name, operation_id):
    with sqlite3.connect('crypto_manager.db') as db:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {coin_name.replace(' ', '_')} WHERE id = ?;", (operation_id,))
        db.commit()
        print(f"DELETE FROM {coin_name.replace(' ', '_')} WHERE id = {operation_id};")


# сума куплених монет та usd по конкретній криптовалюті у вигляді (0.50, 300.0, 600 ) (монети, долари, середня ціна)
def get_buy_summ(coin_name):
    coin = 0
    usd = 0

    for f in get_curent_coin_operation(coin_name.replace(' ', '_')):
        if f[3] is None:
            continue
        else:
            coin += float(f[3])
    for f in get_curent_coin_operation(coin_name.replace(' ', '_')):
        if f[4] is None:
            continue
        else:
            usd += float(f[4])
    try:
        avg = (usd / coin)
    except ZeroDivisionError:
        avg = 0
    return round(coin, 4), round(usd, 4), round(avg, 4)


# сума проданих монет та usd по конкретній криптовалюті у вигляді (0.50, 300.0, 600 ) (монети, долари, середня ціна)
def get_sell_summ(coin_name):
    coin = 0
    usd = 0

    for f in get_curent_coin_operation(coin_name.replace(' ', '_')):
        if f[5] is None:
            continue
        else:
            coin += float(f[5])
    for f in get_curent_coin_operation(coin_name.replace(' ', '_')):
        if f[6] is None:
            continue
        else:
            usd += float(f[6])
    try:
        avg = (usd / coin)
    except ZeroDivisionError:
        avg = 0
    return round(coin, 4), round(usd, 4), round(avg, 4)
