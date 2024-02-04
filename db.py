import datetime
import sqlite3

db = sqlite3.connect('crypto_manager.db')
cursor = db.cursor()


def add_coin_to_db(coin_name):
    """Додаємо монету в базу даних"""

    coin_name = coin_name.lower().replace(' ', '_')
    with db:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {coin_name} (id INTEGER PRIMARY KEY, DATE TEXT, TIME TEXT, BUY INTEGER, BUY_USD INTEGER, SELL INTEGER, SELL_USD INTEGER)")
        print(f"{coin_name} додано в БД")


def dell_coin_in_db(coin_name):
    """Видаляємо монету з бази даних"""

    coin_name = coin_name.lower().replace(' ', '_')
    with db:
        cursor.execute(f"DROP TABLE IF EXISTS {coin_name}")
        print(f"{coin_name} видалено з БД")


def by_or_sell_coin(coin_name, coin_amount, usd_amount, is_buy=True):
    """Додаємо запис про купівлю чи продаж монети в БД"""

    coin_name = coin_name.lower().replace(' ', '_')
    with db:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        time = str(datetime.datetime.now().strftime("%H:%M"))
        buy_sell = "BUY" if is_buy else "SELL"
        cursor.execute(
            f"INSERT INTO {coin_name} (DATE, TIME, {buy_sell}, {buy_sell}_USD) VALUES (?, ?, ?, ?)",
            (date, time, float(coin_amount.replace(',', '.')), float(usd_amount.replace(',', '.'))))
        print(f"{coin_name} {'куплено' if is_buy else 'продано'} "
              f"{coin_amount.replace(',', '.')} на {usd_amount.replace(',', '.')}")


def get_all_coin_name():
    """Отримуємо імена всіх криптовалют із БД в вигляді кортежа, відсортованого по алфавіту.
     ('bitcoin', 'cardano', 'ethereum')"""

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    return tuple(sorted(str(name[0]).replace('_', ' ') for name in table_names))


def get_all_coin_operation():
    """Отримуємо всі операції по всім монетам у вигляді словника
    {'монета': [(id, 'data', 'time', buy_coin, usd_value, sell_coin, usd_value), ...], ...}"""

    operations_dict = {}
    for coin in get_all_coin_name():
        cursor.execute(f"SELECT * FROM `{coin.replace(' ', '_')}`")
        operations_dict[coin] = cursor.fetchall()
    return operations_dict


def get_current_coin_operation(coin_name):
    """Отримуємо всі операції по конкретній монеті у вигляді списку з кортежами
    [(id, 'data', 'time', buy_coin, usd_value, sell_coin, usd_value), ...]"""

    return get_all_coin_operation().get(coin_name.replace('_', ' '))


def del_current_coin_operation(coin_name, operation_id):
    """Видаляємо запис про купівлю/продаж по ID операції"""

    cursor.execute(f"DELETE FROM {coin_name.replace(' ', '_')} WHERE id = ?;", (operation_id,))
    db.commit()
    print(f"DELETE FROM {coin_name.replace(' ', '_')} WHERE id = {operation_id};")


def get_buy_summ(coin_name):
    """Сума куплених монет та usd по конкретній криптовалюті
    у вигляді словника {'coins': 41.81, 'usd': 774.1, 'avg': 18.5147}"""

    coin = 0
    usd = 0

    operations = get_current_coin_operation(coin_name.replace(' ', '_'))
    for f in operations:
        if f[3] is not None:
            coin += float(f[3])
        if f[4] is not None:
            usd += float(f[4])

    avg = usd / coin if coin != 0 else 0

    return {'coins': round(coin, 4), 'usd': round(usd, 4), 'avg': round(avg, 4)}


def get_sell_summ(coin_name):
    """Сума проданих монет та usd по конкретній криптовалюті
    у вигляді словника {'coins': 41.81, 'usd': 774.1, 'avg': 18.5147}"""

    coin = 0
    usd = 0

    operations = get_current_coin_operation(coin_name.replace(' ', '_'))
    for f in operations:
        if f[5] is not None:
            coin += float(f[5])
        if f[6] is not None:
            usd += float(f[6])

    avg = usd / coin if coin != 0 else 0

    return {'coins': round(coin, 4), 'usd': round(usd, 4), 'avg': round(avg, 4)}
