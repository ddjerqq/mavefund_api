import asyncio as aio
from os.path import join, dirname, realpath

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

from .middleware import AuthMiddleware
from .data import ApplicationDbContext
from .routers import UserRouter, AuthRouter, RecordRouter, IndexRouter

load_dotenv()

PATH = dirname(dirname(realpath(__file__)))

# create the app
app = FastAPI()


async def main():
    # initialize the database in singleton manner
    # TODO rework to PostgresSQL
    db = await ApplicationDbContext.connect(join(PATH, "app.db"))

    # initialize routers
    user_router = UserRouter(db)
    record_router = RecordRouter(db)
    auth_router = AuthRouter(db)
    index_router = IndexRouter(db)

    ##########################
    # add routers            #
    ##########################
    app.include_router(user_router.router)
    app.include_router(record_router.router)
    app.include_router(auth_router.router)
    app.include_router(index_router.router)

    # mount static files
    app.mount("/static", StaticFiles(directory=join(PATH, "static")), name="static")

    ##########################
    # configure middleware   #
    ##########################
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        AuthMiddleware,
        database=db
    )

    # add HTTP*S*
    app.add_middleware(HTTPSRedirectMiddleware)
    # mount static files
    app.mount("/static", StaticFiles(directory=join(PATH, "static")), name="static")


# make https redirect work
if __name__ == "__main__":
    aio.run(main())
    uvicorn.run(
        app,
        ssl_certfile=join(PATH, "cert", "server.crt"),
        ssl_keyfile=join(PATH, "cert", "server.key"),
        loop="asyncio",
        host="0.0.0.0",
        port=443
    )
