import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.common import BuyOrSellSum
from src.db.db import Db
from src.db.models import Base, CoinsData

db_file_name = "test_coins_data.db"


@pytest.fixture(autouse=True)
def create_db():
    if os.path.exists(db_file_name):
        os.remove(db_file_name)

    Base.metadata.create_all(bind=get_engine())

    yield

    if os.path.exists(db_file_name):
        os.remove(db_file_name)


def get_engine():
    engine = create_engine(f"sqlite:///{db_file_name}", echo=True)
    return engine


def get_session():
    session = sessionmaker(bind=get_engine())
    return session


def get_all_coins_data():
    session = get_session()()
    coins = session.query(CoinsData).all()
    session.close()
    return coins


def test_add_coin():
    Db(engine=get_engine()).add_coin(coin_name="Bitcoin")

    db = Db(engine=get_engine())
    db.add_coin(coin_name="EtHeReUm")

    coin_list2 = ["MoNero", "SUI", "APToS", ]
    for c in coin_list2:
        Db(engine=get_engine()).add_coin(coin_name=c)

    coin_list1 = ["CardAno", "ArbitruM", "Solana", ]
    for c in coin_list1:
        db.add_coin(coin_name=c)

    coin_names = [coin.coin_name for coin in get_all_coins_data()]
    assert len(coin_names) == 8
    assert "bitcoin" in coin_names
    assert "cardano" in coin_names
    assert "arbitrum" in coin_names
    assert "solana" in coin_names
    assert "ethereum" in coin_names
    assert "monero" in coin_names
    assert "sui" in coin_names
    assert "aptos" in coin_names
    assert "test" not in coin_names


def test_dell_coin():
    db = Db(engine=get_engine())

    db.add_coin(coin_name="BitcoiN")
    db.add_coin(coin_name="EthereuM")
    db.add_coin(coin_name="CARdano")

    coin_name = [coin.coin_name for coin in get_all_coins_data()]
    assert len(coin_name) == 3
    assert "bitcoin" in coin_name
    assert "ethereum" in coin_name
    assert "cardano" in coin_name

    db.dell_coin(coin_name="BitCoin")
    db.dell_coin(coin_name="EtherEuM")

    coin_name = [coin.coin_name for coin in get_all_coins_data()]
    assert len(coin_name) == 1
    assert "bitcoin" not in coin_name
    assert "ethereum" not in coin_name
    assert "cardano" in coin_name


def test_by_or_sell_coin_success_buy():
    """Тест для успішного додавання купівлі монети."""
    db = Db(engine=get_engine())
    db.by_or_sell_coin(coin_name="Bitcoin", coin_amount=1.5, usd_amount=150000, is_buy=True)

    with get_session()() as session:
        coin_data = session.query(CoinsData).filter_by(coin_name="bitcoin").first()
        assert coin_data is not None
        assert coin_data.buy == 1.5
        assert isinstance(coin_data.buy, float)
        assert coin_data.buy_usd == 150000
        assert isinstance(coin_data.buy_usd, float)
        assert coin_data.sell is None
        assert coin_data.sell_usd is None


def test_by_or_sell_coin_success_sell():
    """Тест для успішного додавання купівлі монети."""
    db = Db(engine=get_engine())
    db.by_or_sell_coin(coin_name="Bitcoin", coin_amount=1.5, usd_amount=150000, is_buy=False)

    with get_session()() as session:
        coin_data = session.query(CoinsData).filter_by(coin_name="bitcoin").first()
        assert coin_data is not None
        assert coin_data.buy is None
        assert coin_data.buy_usd is None
        assert coin_data.sell == 1.5
        assert isinstance(coin_data.sell, float)
        assert coin_data.sell_usd == 150000
        assert isinstance(coin_data.sell_usd, float)


def test_all_coin_name():
    coin_list = ['Bitcoin', 'ethereum', 'cardAno', 'arbitruM', 'soLana', ]
    coin_list_lower = [coin.lower() for coin in coin_list]

    db = Db(engine=get_engine())
    for c in coin_list:
        db.add_coin(coin_name=c)

    coin_list_result = db.all_coin_name()
    assert len(coin_list_result) == 5
    assert all(coin in coin_list_lower for coin in coin_list_result)
    assert sorted(coin_list_result) == sorted(coin_list_lower)


def test_all_coin_transaction():
    """Тест для перевірки методу all_coin_transaction."""

    db = Db(engine=get_engine())

    db.by_or_sell_coin(coin_name="bitcoiN", coin_amount=1.5, usd_amount=15000, is_buy=True)
    db.by_or_sell_coin(coin_name="biTcoin", coin_amount=0.5, usd_amount=5000, is_buy=False)
    db.by_or_sell_coin(coin_name="ethEreum", coin_amount=10, usd_amount=3500, is_buy=True)

    transactions = db.all_coin_transaction()

    assert isinstance(transactions, dict)
    assert "bitcoin" in transactions
    assert "ethereum" in transactions

    assert len(transactions["bitcoin"]) == 2
    assert len(transactions["ethereum"]) == 1

    bitcoin_transactions = transactions["bitcoin"]
    assert bitcoin_transactions[0].buy == 1.5
    assert bitcoin_transactions[0].buy_usd == 15000
    assert bitcoin_transactions[0].sell is None
    assert bitcoin_transactions[1].sell == 0.5
    assert bitcoin_transactions[1].sell_usd == 5000

    ethereum_transactions = transactions["ethereum"]
    assert ethereum_transactions[0].buy == 10
    assert ethereum_transactions[0].buy_usd == 3500
    assert ethereum_transactions[0].sell is None


def test_empty_transactions():
    """Тест для перевірки порожньої бази даних."""
    db = Db(engine=get_engine())
    transactions = db.all_coin_transaction()

    assert transactions == {}


def test_specific_coin_transaction_bitcoin():
    db = Db(engine=get_engine())

    db.by_or_sell_coin(coin_name="BItcoin", coin_amount=1.5, usd_amount=150000, is_buy=True)
    db.by_or_sell_coin(coin_name="BitCoin", coin_amount=3, usd_amount=500000, is_buy=False)

    result = db.get_specific_coin_transaction(coin_name="BitcoiN")
    assert len(result) == 2
    assert result[0].buy == 1.5
    assert result[0].buy_usd == 150000.0
    assert result[0].sell is None
    assert result[0].sell_usd is None

    assert result[1].buy is None
    assert result[1].buy_usd is None
    assert result[1].sell == 3
    assert result[1].sell_usd == 500000.0


def test_specific_coin_transaction_ethereum():
    db = Db(engine=get_engine())

    db.by_or_sell_coin(coin_name="ETHereUm", coin_amount=1, usd_amount=10000, is_buy=True)
    db.by_or_sell_coin(coin_name="ETHereUm", coin_amount=0.5, usd_amount=20000, is_buy=False)
    result = db.get_specific_coin_transaction(coin_name="ETHEREum")
    assert len(result) == 2
    assert result[0].buy == 1.0
    assert result[0].buy_usd == 10000.0
    assert result[0].sell is None
    assert result[0].sell_usd is None

    assert result[1].buy is None
    assert result[1].buy_usd is None
    assert result[1].sell == 0.5
    assert result[1].sell_usd == 20000.0


def test_specific_coin_transaction_no_data():
    db = Db(engine=get_engine())

    result = db.get_specific_coin_transaction(coin_name="test")
    assert len(result) == 0


def test_del_curr_coin_operation():
    db = Db(engine=get_engine())

    db.by_or_sell_coin(coin_name="ETHereUm", coin_amount=1, usd_amount=10000, is_buy=True)
    db.by_or_sell_coin(coin_name="ETHereUm", coin_amount=0.5, usd_amount=20000, is_buy=True)
    db.by_or_sell_coin(coin_name="ETHereUm", coin_amount=2, usd_amount=3000, is_buy=False)
    db.by_or_sell_coin(coin_name="ETHereUm", coin_amount=1.5, usd_amount=4000, is_buy=False)

    all_coins_transaction = db.get_specific_coin_transaction(coin_name="ETHEREUM")
    assert len(all_coins_transaction) == 4

    id_ = all_coins_transaction[0].id
    coin_name = all_coins_transaction[0].name
    db.del_curr_coin_operation(coin_name=coin_name, operation_id=id_)

    id_ = all_coins_transaction[3].id
    coin_name = all_coins_transaction[3].name
    db.del_curr_coin_operation(coin_name=coin_name, operation_id=id_)

    all_coins_transaction = db.get_specific_coin_transaction(coin_name="ETHEREUM")
    assert len(all_coins_transaction) == 2


def test_get_buy_summ():
    db = Db(engine=get_engine())

    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=True)
    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=True)
    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=True)
    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=False)

    result = db.get_buy_summ(coin_name='bitcoin')

    assert isinstance(result, BuyOrSellSum)
    assert result.coin == 3.0
    assert result.usd == 150000.0
    assert result.avg == 50000.00


def test_get_sell_summ():
    db = Db(engine=get_engine())

    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=False)
    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=False)
    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=False)
    db.by_or_sell_coin(coin_name='bitcoin', coin_amount=1, usd_amount=50000, is_buy=True)

    result = db.get_sell_summ(coin_name='bitcoin')

    assert isinstance(result, BuyOrSellSum)
    assert result.coin == 3.0
    assert result.usd == 150000.0
    assert result.avg == 50000.00
