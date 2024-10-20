import datetime
import os.path

from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, Integer, DateTime, Float, VARCHAR

from config import engine


class Base(DeclarativeBase):
    id: Mapped[int] = Column(Integer, primary_key=True)


class CoinsData(Base):
    __tablename__ = 'coins_data'

    coin_name: Mapped[str] = Column(VARCHAR(50), nullable=False)
    buy: Mapped[float] = Column(Float, nullable=True, default=None)
    buy_usd: Mapped[float] = Column(Float, nullable=True, default=None)
    sell: Mapped[float] = Column(Float, nullable=True, default=None)
    sell_usd: Mapped[float] = Column(Float, nullable=True, default=None)
    date: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


def recreate_all_tables():
    from config import db_name
    if os.path.exists(db_name):
        os.remove(db_name)
    Base.metadata.create_all(engine)
