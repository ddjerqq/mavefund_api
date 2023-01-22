from fastapi import Request, HTTPException


UNAUTHORIZED = HTTPException(status_code=401, detail="you are not authorized")
FORBIDDEN = HTTPException(status_code=403, detail="you do not have access to this resource")


def authenticated_only(req: Request):
    if req.user is None:
        raise UNAUTHORIZED


def subscriber_only(req: Request, q: str):
    if q in ["FB", "META", "AAPL", "AMZN", "NFLX", "GOOGL"]:
        return

    if req.user is None:
        raise UNAUTHORIZED

    if req.user.rank == -1:
        raise FORBIDDEN


def admin_only(req: Request):
    if req.user is None:
        raise UNAUTHORIZED

    if req.user.rank < 3:
        raise FORBIDDEN
