import atexit
import os
from os.path import join
from subprocess import Popen

import stripe
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from src import PATH
from src.middleware import AuthMiddleware
from src.data import ApplicationDbContext
from src.routers import ApiRouter
from src.utilities import SinglePageApplication

stripe.api_key = os.getenv("STRIPE_SECRET_API_KEY")

# create the app
app = FastAPI(
    docs_url=None,
    redoc_url=None,
)


@app.on_event("startup")
async def startup():
    db = await ApplicationDbContext.connect(
        host=os.getenv("POSTGRES_HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="postgres"
    )
    await db.migrate()

    # # initialize routers
    # index_router = IndexRouter(db)

    api = ApiRouter(db)

    ##########################
    # add routers            #
    ##########################
    # app.include_router(index_router.router)

    app.include_router(api.router)

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


    # mount static
    app.mount(
        path="/",
        app=SinglePageApplication(directory=join(PATH, "static")),
        name="static"
    )
    # app.mount("/static", StaticFiles(directory=join(PATH, "static")), name="static")


# make https redirect work
if __name__ == "__main__":

    process = Popen(["python", join(PATH, "src", "https_redirect.py")])
    atexit.register(process.terminate)

    uvicorn.run(
        "__main__:app",
        ssl_certfile=join(PATH, "cert", "server.crt"),
        ssl_keyfile=join(PATH, "cert", "server.key"),
        loop="asyncio",
        host="0.0.0.0",
        port=443,
        # reload=True,
        env_file="../.env",
        # reload_dirs=["../"],
        # reload_includes=["../static", "../templates"],
    )
