import asyncio as aio
import os
from os.path import dirname, realpath, join

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from dotenv import load_dotenv

from data import ApplicationDbContext
from routers import UserRouter, AuthRouter, RecordRouter
from services import UserAuthService

# C:/work/python/mavefund_api
PATH = dirname(dirname(realpath(__file__)))

load_dotenv()

# initialize the database in singleton manner
loop = aio.new_event_loop()
db = loop.run_until_complete(ApplicationDbContext.connect(join(PATH, "app.db")))
auth_service = UserAuthService(db)

# initialize routers
user_router = UserRouter(db, auth_service)
record_router = RecordRouter(db, auth_service)
auth_router = AuthRouter(db)

# add routers
app = FastAPI()
app.include_router(user_router.router)
app.include_router(record_router.router)
app.include_router(auth_router.router)


# configure middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add HTTP*S*
app.add_middleware(HTTPSRedirectMiddleware)

# make https redirect work
if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        ssl_certfile=join(PATH, "cert", "server.crt"),
        ssl_keyfile=join(PATH, "cert", "server.key"),
        loop="asyncio",
        host="127.0.0.1",
        port=443,
        reload=True,
        debug=True,
    )
