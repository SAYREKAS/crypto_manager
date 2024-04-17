import datetime
import sqlite3


class Db:
    def __init__(self):
        self.db = sqlite3.connect('crypto_manager.db')
        self.cursor = self.db.cursor()

    def add_coin(self, coin_name: str) -> None:
        """Додаємо монету в базу даних"""

        coin_name = coin_name.lower().replace(' ', '_')
        with self.db:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {coin_name} "
                f"(id INTEGER PRIMARY KEY, "
                f"DATE TEXT, "
                f"TIME TEXT, "
                f"BUY INTEGER, "
                f"BUY_USD INTEGER, "
                f"SELL INTEGER, "
                f"SELL_USD INTEGER)")
            print(f"{coin_name} додано в БД")

    def dell_coin(self, coin_name: str) -> None:
        """Видаляємо монету з бази даних"""

        coin_name = coin_name.lower().replace(' ', '_')
        with self.db:
            self.cursor.execute(f"DROP TABLE IF EXISTS {coin_name}")
            print(f"{coin_name} видалено з БД")

    def by_or_sell_coin(self, coin_name: str, coin_amount: str, usd_amount: str, is_buy=True) -> None:
        """Додаємо запис про купівлю чи продаж монети в БД"""

        coin_name = coin_name.lower().replace(' ', '_')
        with self.db:
            date = str(datetime.datetime.now().strftime("%d-%m-%Y"))
            time = str(datetime.datetime.now().strftime("%H:%M"))
            buy_sell = "BUY" if is_buy else "SELL"
            self.cursor.execute(
                f"INSERT INTO {coin_name} (DATE, TIME, {buy_sell}, {buy_sell}_USD) VALUES (?, ?, ?, ?)",
                (date, time, float(coin_amount.replace(',', '.')), float(usd_amount.replace(',', '.'))))
            print(f"{coin_name} {'куплено' if is_buy else 'продано'} "
                  f"{coin_amount.replace(',', '.')} на {usd_amount.replace(',', '.')}")

    def all_coin_name(self) -> tuple:
        """Отримуємо імена всіх криптовалют із БД в вигляді кортежа, відсортованого по алфавіту.
         ('bitcoin', 'cardano', 'ethereum')"""

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = self.cursor.fetchall()
        return tuple(sorted(str(name[0]).replace('_', ' ') for name in table_names))

    def all_coin_operation(self) -> dict:
        """Отримуємо всі операції по всім монетам у вигляді словника
        {'монета': [(id, 'date', 'time', buy_coin, usd_value, sell_coin, usd_value), ...], ...}"""

        operations_dict = {}
        for coin in Db().all_coin_name():
            self.cursor.execute(f"SELECT * FROM `{coin.replace(' ', '_')}`")
            operations_dict[coin] = self.cursor.fetchall()
        return operations_dict

    @staticmethod
    def curr_coin_operation(coin_name: str) -> list[tuple]:
        """Отримуємо всі операції по конкретній монеті у вигляді списку з кортежами
        [(id, 'date', 'time', buy_coin, usd_value, sell_coin, usd_value), ...]"""

        return Db().all_coin_operation().get(coin_name.replace('_', ' '))

    def del_curr_coin_operation(self, coin_name: str, operation_id: int) -> None:
        """Видаляємо запис про купівлю/продаж по ID операції"""

        self.cursor.execute(f"DELETE FROM {coin_name.replace(' ', '_')} WHERE id = ?;", (operation_id,))
        self.db.commit()
        print(f"DELETE FROM {coin_name.replace(' ', '_')} WHERE id = {operation_id};")

    @staticmethod
    def get_buy_summ(coin_name: str) -> dict:
        """Сума куплених монет та usd по конкретній криптовалюті
        у вигляді словника {'coins': 41.81, 'usd': 774.1, 'avg': 18.5147}"""

        coin = 0
        usd = 0

        operations = Db.curr_coin_operation(coin_name.replace(' ', '_'))
        for f in operations:
            if f[3] is not None:
                coin += float(f[3])
            if f[4] is not None:
                usd += float(f[4])

        avg = usd / coin if coin != 0 else 0

        return {'coins': round(coin, 4), 'usd': round(usd, 4), 'avg': round(avg, 4)}

    @staticmethod
    def get_sell_summ(coin_name: str) -> dict:
        """Сума проданих монет та usd по конкретній криптовалюті
        у вигляді словника {'coins': 41.81, 'usd': 774.1, 'avg': 18.5147}"""

        coin = 0
        usd = 0

        operations = Db.curr_coin_operation(coin_name.replace(' ', '_'))
        for f in operations:
            if f[5] is not None:
                coin += float(f[5])
            if f[6] is not None:
                usd += float(f[6])

        avg = usd / coin if coin != 0 else 0

        return {'coins': round(coin, 4), 'usd': round(usd, 4), 'avg': round(avg, 4)}
