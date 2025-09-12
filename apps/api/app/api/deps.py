from fastapi import Depends, HTTPException, status, Request

def get_role(request: Request) -> str:
    return request.headers.get("x-user-role", "")

def require_admin(role: str = Depends(get_role)) -> None:
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin only")