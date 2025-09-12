from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.api.deps import require_admin
from app.schemas.broker import AccountOut, PositionOut, AssetOut, OrderIn, OrderOut
from app.services.broker.alpaca import AlpacaClient

router = APIRouter()
_client = AlpacaClient()

@router.get("/account", response_model=AccountOut)
async def get_account():
    data = await _client.get_account()
    return AccountOut(**data)

@router.get("/positions", response_model=List[PositionOut])
async def get_positions():
    data = await _client.get_positions()
    return [PositionOut(**p) for p in data]

@router.get("/assets", response_model=List[AssetOut])
async def get_assets(
    status: str = Query("active"),
    asset_class: Optional[str] = Query("us_equity"),
    tradable: Optional[bool] = Query(True),
):
    data = await _client.get_assets(status=status, asset_class=asset_class, tradable=tradable)
    return [AssetOut(**a) for a in data]

@router.get("/orders", response_model=List[OrderIn])
async def get_orders():
    data = await _client.get_orders()
    return [OrderIn(**o) for o in data]

@router.post("/orders", response_model=OrderOut, dependencies=[Depends(require_admin)])
async def create_order(payload: OrderIn):
    data = await _client.place_order(**payload.model_dump(exclude_none=True))
    return OrderOut(**data)
