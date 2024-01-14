import datetime
import sqlite3


def create_db():
    db = sqlite3.connect('crypto_manager.db')


def add_coin_to_db(coin_name):
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()

    # додаємо монету в базу даних
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {coin_name} (id INTEGER PRIMARY KEY, DATE TEXT, TIME TEXT, BUY INTEGER, BUY_USD INTEGER, SELL INTEGER, SELL_USD INTEGER)")
    db.commit()


def dell_coin_in_db(coin_name):
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {coin_name}")


def by_coin(coin_name, coin_amount, usd_amount):
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()

    # купуємо монету
    date = str(datetime.datetime.now().strftime("%d-%m-%Y"))
    time = str(datetime.datetime.now().strftime("%H:%M"))
    cursor.execute(
        f"INSERT INTO {coin_name} (DATE, TIME, BUY, BUY_USD) VALUES (?, ?, ?, ?)",
        (date, time, coin_amount, usd_amount))
    db.commit()


def sell_coin(coin_name, coin_amount, usd_amount):
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()

    # продаємо монету
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    time = str(datetime.datetime.now().strftime("%H:%M"))
    cursor.execute(
        f"INSERT INTO {coin_name} (DATE, TIME, SELL, SELL_USD) VALUES (?, ?, ?, ?)",
        (date, time, coin_amount, usd_amount))
    db.commit()


def get_all_coin_name():
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()

    # отримуємо імена всіх криптовалют із БД в вигляді списка ['bitcoin', 'cardano', 'ethereum']
    coin_name = []
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    for name in table_names:
        coin_name.append(*name)
    return sorted(coin_name)


def get_all_coin_operation():
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()

    # отримуємо всі операції по всім монетам у вигляді словника типу {монета: [(операція1), (операція2),]}
    coin_dict = {}
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


def get_curent_coin_operation(coin_name):
    # отримуємо всі операції по конкретній монеті
    main_list = []
    item = get_all_coin_operation()[coin_name]
    for f in item:
        main_list.append(f)
    return main_list


def del_curent_coin_operation(coin_name, operation_id):
    db = sqlite3.connect('crypto_manager.db')
    cursor = db.cursor()

    cursor.execute(f"DELETE FROM {coin_name} WHERE id = ?;", (operation_id,))
    db.commit()
    print(f"DELETE FROM {coin_name} WHERE id = {operation_id};")


def get_buy_summ(coin_name):
    # сума куплених монет та usd по конкретній криптовалюті у вигляді (0.50, 300.0, 600 )
    coin = 0
    usd = 0

    for f in get_curent_coin_operation(coin_name):
        if f[3] is None:
            continue
        else:
            coin += float(f[3])

    for f in get_curent_coin_operation(coin_name):
        if f[4] is None:
            continue
        else:
            usd += float(f[4])
    try:
        avg = (usd / coin)
    except ZeroDivisionError:
        avg = 0
    return round(coin, 4), round(usd, 4), round(avg, 4)


def get_sell_summ(coin_name):
    # сума проданих монет та usd по конкретній криптовалюті у вигляді (0.50, 300.0, 600 )
    coin = 0
    usd = 0
    for f in get_curent_coin_operation(coin_name):
        if f[5] is None:
            continue
        else:
            coin += float(f[5])

    for f in get_curent_coin_operation(coin_name):
        if f[6] is None:
            continue
        else:
            usd += float(f[6])
    try:
        avg = (usd / coin)
    except ZeroDivisionError:
        avg = 0
    return round(coin, 4), round(usd, 4), round(avg, 4)
