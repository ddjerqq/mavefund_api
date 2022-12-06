from __future__ import annotations

import logging
import os

import jose.exceptions
from fastapi import HTTPException
from fastapi import Header
from jose import JWTError
from jose import jwt

UNAUTHORIZED = HTTPException(status_code=401, detail="invalid authorization header")


def extract_claims_from_jwt(token: str) -> dict[str, ...] | None:
    """Extract claims from JWT token

    returns the claims: ("sub", "exp") if the JWT is valid and signed correctly, None otherwise
    """
    try:
        return jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )
    except jose.exceptions.ExpiredSignatureError:
        return None
    except Exception as e:
        logging.error(f"JWTError {e}", exc_info=True)
        return None


def validate_jwt(x_authorization: str = Header()) -> bool:
    """Validate JWT token

    return boolean whether or not JWT is valid
    """
    if x_authorization is None:
        return False

    if (claims := extract_claims_from_jwt(x_authorization)) is None:
        return False

    if not all(key in claims for key in ("sub", "exp", "iat")):
        return False

    return True


def verify_jwt(x_authorization: str = Header()):
    """Verify JWT token

    raise 401 HTTPException if token is invalid
    """
    if x_authorization is None:
        raise UNAUTHORIZED

    if (claims := extract_claims_from_jwt(x_authorization)) is None:
        raise UNAUTHORIZED

    if not all(key in claims for key in ("sub", "exp", "iat")):
        raise UNAUTHORIZED


def admin_only(x_authorization: str = Header()) -> None:
    """Limit access to admin only

    raise 403 HTTPException if token is invalid or user is not admin
    """
    claims = extract_claims_from_jwt(x_authorization)
    if claims["role"] != "admin":
        raise HTTPException(status_code=403, detail="admin only")
