import os
import aiohttp
from fastapi import Request, HTTPException


RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET")


async def validate_captcha_token(request: Request):
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

    json = await request.json()
    token = json.get("token", None)

    payload = {
        "secret": RECAPTCHA_SECRET,
        "response": token,
        "remoteip": request.client.host,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(recaptcha_url, data=payload) as resp:
            result = await resp.json()

    if not result.get("success", False):
        raise HTTPException(status_code=400, detail="Invalid recaptcha response!")

    return True
