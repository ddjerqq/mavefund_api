from __future__ import annotations

import logging
import os

import jose.exceptions
from jose import jwt


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
