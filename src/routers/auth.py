from __future__ import annotations

import os
from datetime import datetime

from jose import JWTError, jwt
from datetime import timedelta

from fastapi import APIRouter, Depends, Header, Response, Request
from fastapi import HTTPException

from src.main import oauth2_scheme
from src.models.user import User
from src.services.user_service import UserService
from src.utilities.password_hasher import Password

router = APIRouter()

