from loguru import logger
from sqlalchemy import create_engine, func

from src.db.models import CoinsData
from src.db.config import sessionmaker
from src.db.common import BuyOrSellSum, CoinTransaction, CustomCoinError


class Db:

    def __init__(self, engine: create_engine):
        self.__session = sessionmaker(bind=engine)

    def add_coin(self, coin_name: str) -> None:
        """Додаємо монету в базу даних"""

        coin_name = coin_name.lower().replace(' ', '_')
        with self.__session() as session:
            new_coin = CoinsData(coin_name=coin_name)
            session.add(new_coin)
            try:
                session.commit()
                logger.success(f"{coin_name} додано в БД")
            except Exception as e:
                session.rollback()
                raise CustomCoinError(f"Помилка при додаванні монети: {e}")
            finally:
                session.close()

    def dell_coin(self, coin_name: str) -> None:
        """Видаляємо монету з бази даних"""

        coin_name = coin_name.lower().replace(' ', '_')

        with self.__session() as session:
            session.query(CoinsData).filter_by(coin_name=coin_name).delete()
            try:
                session.commit()
                logger.success(f"{coin_name} видалено з БД")
            except Exception as e:
                session.rollback()
                raise CustomCoinError(f"Помилка при видаленні монети: {e}")
            finally:
                session.close()

    def by_or_sell_coin(self, coin_name: str, coin_amount: int | float, usd_amount: int | float, is_buy=True) -> None:
        """Додаємо запис про купівлю чи продаж монети в БД"""

        coin_name = coin_name.lower().replace(' ', '_')
        coin_amount = float(coin_amount)
        usd_amount = float(usd_amount)

        with self.__session() as session:

            transaction = CoinsData(
                coin_name=coin_name,
                buy=coin_amount if is_buy else None,
                buy_usd=usd_amount if is_buy else None,
                sell=None if is_buy else coin_amount,
                sell_usd=None if is_buy else usd_amount,
            )

            session.add(transaction)

            try:
                session.commit()
                logger.success(f"{coin_name} {'куплено' if is_buy else 'продано'} {coin_amount} на {usd_amount}")
            except Exception as e:
                session.rollback()
                raise CustomCoinError(
                    f"Не вдалося додати запис про {'купівлю' if is_buy else 'продаж'} монети {coin_name}: {e}")
            finally:
                session.close()

    def all_coin_name(self) -> list:
        """Отримує всі імена криптовалют у вигляді відсортованого по алфавіту списку."""
        with self.__session() as session:
            data = session.query(CoinsData.coin_name).distinct().all()
        return [name[0] for name in data]

    def all_coin_transaction(self) -> dict:
        """
        Отримуємо всі операції по всім монетам у вигляді словника
        {'монета': [(id, buy_coin, usd_value, sell_coin, usd_value, 'date'), ...], ...}
        """
        transactions_dict = {}

        with self.__session() as session:
            all_transactions = session.query(CoinsData).all()

            for transaction in all_transactions:
                coin_name = transaction.coin_name

                if coin_name not in transactions_dict:
                    transactions_dict[coin_name] = []

                transaction_data = CoinTransaction(
                    id=transaction.id,
                    name=transaction.coin_name,
                    buy=transaction.buy,
                    buy_usd=transaction.buy_usd,
                    sell=transaction.sell,
                    sell_usd=transaction.sell_usd,
                    date=transaction.date
                )
                transactions_dict[coin_name].append(transaction_data)

        return transactions_dict

    def get_specific_coin_transaction(self, coin_name: str) -> list[CoinTransaction]:
        """Отримуємо всі операції по конкретній монеті у вигляді списку з кортежами
        [(id, 'date', 'time', buy_coin, usd_value, sell_coin, usd_value), ...]"""

        coin_name = coin_name.lower().replace(' ', '_')
        with self.__session() as session:
            data = session.query(CoinsData).filter(CoinsData.coin_name == coin_name).all()
            return [
                CoinTransaction(
                    id=transaction.id,
                    name=transaction.coin_name,
                    buy=transaction.buy,
                    buy_usd=transaction.buy_usd,
                    sell=transaction.sell,
                    sell_usd=transaction.sell_usd,
                    date=transaction.date)
                for transaction in data
            ]

    def del_curr_coin_operation(self, coin_name: str, operation_id: int) -> None:
        """Видаляємо запис про купівлю/продаж по ID операції"""

        with self.__session() as session:
            session.query(CoinsData).filter(CoinsData.id == operation_id, CoinsData.coin_name == coin_name).delete()
            try:
                session.commit()
                logger.success(f"Запис про купівлю/продаж {coin_name} з ID {operation_id} успішно видалено")
            except Exception as e:
                session.rollback()
                raise CustomCoinError(
                    f"Помилка при видаленні запису про купівлю/продаж {coin_name} з ID {operation_id}: {e}")
            finally:
                session.close()

    def get_buy_summ(self, coin_name: str) -> BuyOrSellSum:
        """Сума куплених монет та usd по конкретній криптовалюті
        у вигляді словника {'coins': 41.81, 'usd': 774.1, 'avg': 18.5147}"""

        with self.__session() as session:
            result = session.query(
                func.sum(CoinsData.buy).label('coin_sum'),
                func.sum(CoinsData.buy_usd).label('usd_sum')
            ).filter(CoinsData.coin_name == coin_name).first()

        return BuyOrSellSum(coin=result.coin_sum, usd=result.usd_sum)

    def get_sell_summ(self, coin_name: str) -> BuyOrSellSum:
        """Сума проданих монет та usd по конкретній криптовалюті
        у вигляді словника {'coins': 41.81, 'usd': 774.1, 'avg': 18.5147}"""

        with self.__session() as session:
            result = session.query(
                func.sum(CoinsData.sell).label('coin_sum'),
                func.sum(CoinsData.sell_usd).label('usd_sum')
            ).filter(CoinsData.coin_name == coin_name).first()

            return BuyOrSellSum(coin=result.coin_sum, usd=result.usd_sum)
