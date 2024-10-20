import datetime
from typing import Optional, Union

from pydantic import BaseModel, model_validator


class CustomCoinError(Exception):
    pass


class CoinTransaction(BaseModel):
    id: int
    name: Optional[str]
    buy: Union[float, None]
    buy_usd: Union[float, None]
    sell: Union[float, None]
    sell_usd: Union[float, None]
    date: Optional[datetime.datetime] = None


class BuyOrSellSum(BaseModel):
    coin: Optional[float] = 0.0
    usd: Optional[float] = 0.0
    avg: float = 0.0

    @model_validator(mode='after')
    def calculate_avg(self) -> 'BuyOrSellSum':
        """Обчислює середню вартість за монету."""
        self.avg = round(self.usd / self.coin if self.coin > 0 else 0.0, 2)
        return self
