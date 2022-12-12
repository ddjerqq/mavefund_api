from fastapi import Request, HTTPException


async def authenticated_only(req: Request):
    if req.user is None:
        raise HTTPException(status_code=401, detail="you are not authorized")


async def admin_only(req: Request):
    if req.user is None:
        raise HTTPException(status_code=401, detail="you are not authorized")

    if req.user.rank < 3:
        raise HTTPException(status_code=403, detail="you are not authorized")
