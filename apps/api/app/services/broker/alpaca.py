import httpx, uuid, logging
from typing import Any, Dict, Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fastapi import HTTPException
from app.core.config import settings

log = logging.getLogger(__name__)

class AlpacaError(HTTPException):
    pass

def _headers() -> Dict[str, str]:
    if not settings.alpaca_api_key or not settings.alpaca_api_secret:
        raise AlpacaError(status_code=500, detail="Alpaca credentials not configured")
    return {
        "APCA-API-KEY-ID": settings.alpaca_api_key,
        "APCA-API-SECRET-KEY": settings.alpaca_api_secret,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

def _url(path: str) -> str:
    base = settings.alpaca_base_url.rstrip("/")
    return f"{base}/v2{path}"

retry_policy = dict(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(httpx.RequestError),
    reraise=True,
)

class AlpacaClient:
    @retry(**retry_policy)
    async def get_account(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(_url("/account"), headers=_headers())
        if r.status_code >= 400:
            raise AlpacaError(status_code=r.status_code, detail=r.text)
        return r.json()

    @retry(**retry_policy)
    async def get_positions(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(_url("/positions"), headers=_headers())
        if r.status_code >= 400:
            raise AlpacaError(status_code=r.status_code, detail=r.text)
        return r.json()

    @retry(**retry_policy)
    async def get_assets(
        self, status: str = "active", asset_class: str | None = "us_equity", tradable: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"status": status}
        if asset_class: params["asset_class"] = asset_class
        if tradable is not None: params["tradable"] = str(tradable).lower()
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(_url("/assets"), headers=_headers(), params=params)
            if r.status_code >= 400:
                raise AlpacaError(status_code=r.status_code, detail=r.text)
            return r.json()

    @retry(**retry_policy)
    async def get_orders(
        self
    ) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(_url("/orders"), headers=_headers())
        if r.status_code >= 400:
            raise AlpacaError(status_code=r.status_code, detail=r.text)
        return r.json()

    @retry(**retry_policy)
    async def place_order(
        self,
        *,
        symbol: str,
        qty: int | str | float,
        side: str,
        type: str = "market",
        time_in_force: str = "day",
        limit_price: float | None = None,
        stop_price: float | None = None,
        client_order_id: str | None = None,
        extended_hours: bool | None = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "symbol": symbol.upper(),
            "qty": qty,
            "side": side.lower(),
            "type": type.lower(),
            "time_in_force": time_in_force.lower(),
            "client_order_id": client_order_id or uuid.uuid4().hex,
        }
        if limit_price is not None: body["limit_price"] = limit_price
        if stop_price is not None: body["stop_price"] = stop_price
        if extended_hours is not None: body["extended_hours"] = extended_hours
        
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(_url("/orders"), headers=_headers(), json=body)
            if r.status_code >= 400:
                raise AlpacaError(status_code=r.status_code, detail=r.text)
            return r.json()

    @retry(**retry_policy)
    async def get_portfolio_history(
        self,
        *,
        period: Optional[str] = None,
        timeframe: str = "1D",
        start: Optional[str] = None,
        end: Optional[str] = None,
        intraday_reporting: Optional[str] = None,
        pnl_reset: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"timeframe": timeframe}
        if period: params["period"] = period
        if start: params["start"] = start
        if end: params["end"] = end
        if intraday_reporting: params["intraday_reporting"] = intraday_reporting
        if pnl_reset: params["pnl_reset"] = pnl_reset
        log.info("Fetching portfolio history: timeframe = %s, period = %s, start = %s, end = %s, intraday_reporting = %s, pnl_reset = %s",
                 timeframe, period, start, end, intraday_reporting, pnl_reset)

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(_url("/account/portfolio/history"), headers=_headers(), params=params)
            if r.status_code >= 400:
                raise AlpacaError(status_code=r.status_code, detail=r.text)
            return r.json()