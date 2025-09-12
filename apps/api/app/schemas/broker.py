from pydantic import BaseModel, Field, conint, confloat
from typing import Optional, Literal

class AccountOut(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    buying_power: Optional[str] = None
    equity: Optional[str] = None
    cash: Optional[str] = None
    portfolio_value: Optional[str] = None

class PositionOut(BaseModel):
    symbol: str
    qty: str
    avg_entry_price: Optional[str] = None
    market_value: Optional[str] = None
    unrealized_pl: Optional[str] = None
    side: Optional[str] = None

class AssetOut(BaseModel):
    id: Optional[str] = None
    symbol: str
    name: Optional[str] = None
    tradable: Optional[bool] = None
    status: Optional[str] = None
    asset_class: Optional[str] = None

class OrderIn(BaseModel):
    symbol: str = Field(..., min_length=1)
    qty: confloat(gt=0) | conint(gt=0)
    side: Literal["buy", "sell"] = "buy"
    type: Literal["market", "limit", "stop", "stop_limit", "trailing_stop"] = "market"
    time_in_force: Literal["day", "gtc", "opg", "cls", "ioc", "fok"] = "day"
    limit_price: Optional[confloat(gt=0)] = None
    stop_price: Optional[confloat(gt=0)] = None
    client_order_id: Optional[str] = None
    extended_hours: Optional[bool] = None

class OrderOut(BaseModel):
    id: str
    client_order_id: Optional[str] = None
    symbol: str
    qty: str
    side: str
    type: str
    time_in_force: str
    status: str
    submitted_at: Optional[str] = None
