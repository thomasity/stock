import logging
from fastapi import APIRouter, Query, Request
from typing import Optional, Dict, Any, List
from app.services.broker.alpaca import AlpacaClient

router = APIRouter()
_client = AlpacaClient()
log = logging.getLogger(__name__)

def _epoch_to_iso(ts_list: List[int]) -> List[str]:
    from datetime import datetime, timezone
    return [datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() for ts in ts_list]

@router.get("/")
def portfolio_health():
    return {
        "status": "ok",
    }

@router.get("/history")
async def portfolio_history(
    request: Request,
    period: Optional[str] = Query(None, description='e.g. "30D", "1D", "1M"'),
    timeframe: str = Query("1D", description='"1Min","5Min","15Min","1D"'),
    start: Optional[str] = Query(None, description="ISO date/time"),
    end: Optional[str] = Query(None, description="ISO date/time"),
    intraday_reporting: Optional[str] = Query(None, description='"regular_hours","extended_hours","continuous"'),
    pnl_reset: Optional[str] = Query(None, description='"daily","no_reset"'),
) -> Dict[str, Any]:
    log.info("Request: %s", str(request.url))
    log.info("Fetching portfolio history: timeframe = %s, period = %s, start = %s, end = %s, intraday_reporting = %s, pnl_reset = %s",
                 timeframe, period, start, end, intraday_reporting, pnl_reset)
    data = await _client.get_portfolio_history(
        period=period,
        timeframe=timeframe,
        start=start,
        end=end,
        intraday_reporting=intraday_reporting,
        pnl_reset=pnl_reset,
    )
    out = {
        "timeframe": data.get("timeframe"),
        "period": data.get("period"),
        "timestamp": _epoch_to_iso(data.get("timestamp")),
        "equity": data.get("equity", []),
        "profit_loss": data.get("profit_loss", []),
        "profit_loss_pct": data.get("profit_loss_pct", []),
    }
    return out