import asyncio as aio
from os.path import dirname, realpath, join

import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv

from src.data import ApplicationDbContext
from src.routers import UserRouter, AuthRouter
from src.services import UserAuthService

PATH = dirname(dirname(realpath(__file__)))

load_dotenv()

# initialize the database in singleton manner
loop = aio.new_event_loop()
db = loop.run_until_complete(ApplicationDbContext.connect(join(PATH, "app.db")))
auth_service = UserAuthService(db)

# TODO add dependencies here to verify the token
#  dependencies=[Depends(verify_token)]
user_router = UserRouter(db, auth_service)
auth_router = AuthRouter(db)

app = FastAPI()
app.include_router(user_router.router, dependencies=[])
app.include_router(auth_router.router, dependencies=[])


if __name__ == "__main__":
    uvicorn.run(
        app,
        loop="asyncio",
        host="127.0.0.1",
        port=8000,
    )
