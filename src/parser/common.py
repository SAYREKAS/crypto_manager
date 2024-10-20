from typing import Optional
from pydantic import BaseModel


class PercentChange(BaseModel):
    percentChange1h: float
    percentChange24h: float
    percentChange7d: float
    percentChange30d: float
    percentChange60d: float
    percentChange90d: float


class Parser(BaseModel):
    name: str
    symbol: str
    tags: list[str]
    price: float
    percent_change: PercentChange


class Quote(BaseModel):
    name: str
    price: float
    volume24h: float
    marketCap: float
    percentChange1h: float
    percentChange24h: float
    percentChange7d: float
    lastUpdated: str
    percentChange30d: float
    percentChange60d: float
    percentChange90d: float
    fullyDilluttedMarketCap: float
    marketCapByTotalSupply: float
    dominance: float
    turnover: float
    ytdPriceChangePercentage: float
    percentChange1y: float


class CryptoCurrency(BaseModel):
    id: int
    name: str
    symbol: str
    slug: str
    tags: list[str]
    cmcRank: int
    marketPairCount: int
    circulatingSupply: float
    selfReportedCirculatingSupply: float
    totalSupply: float
    maxSupply: Optional[float] = None
    isActive: int
    lastUpdated: str
    dateAdded: str
    quotes: list[Quote]
    isAudited: bool
    # auditInfoList: List[AuditInfo]
    badges: list[int]


class Data(BaseModel):
    cryptoCurrencyList: list[CryptoCurrency]
    totalCount: str


class Status(BaseModel):
    timestamp: str
    error_code: str
    error_message: str
    elapsed: str
    credit_count: int


class CryptoResponse(BaseModel):
    data: Data
    status: Status
