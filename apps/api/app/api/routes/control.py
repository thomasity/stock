from fastapi import APIRouter, Depends
from app.api.deps import require_admin

router = APIRouter()
_kill = {"enabled": False}

@router.get("/kill-switch")
def get_kill():
    return {"enabled": _kill["enabled"]}

@router.post("/kill-switch", dependencies=[Depends(require_admin)])
def toggle_kill():
    _kill["enabled"] = not _kill["enabled"]
    return {"enabled": _kill["enabled"]}