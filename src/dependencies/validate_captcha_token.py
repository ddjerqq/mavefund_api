import os
import requests
from fastapi import Request, HTTPException


RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET")


async def validate_captcha_token(request: Request):
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

    json = await request.json()
    token = json.get("recaptcha_token", None)

    # this is commented out because there was an issue
    # with dependency management on docker.
    # todo fix this.
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(recaptcha_url, data=payload) as resp:
    #         result = await resp.json()


    resp = requests.post(
        recaptcha_url,
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=f"secret={RECAPTCHA_SECRET}&response={token}&remoteip={request.client.host}"
    )
    result = resp.json()
    print(result)

    if not result.get("success", False):
        raise HTTPException(status_code=400, detail="Invalid recaptcha response!")

    return True
