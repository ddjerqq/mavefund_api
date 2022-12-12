import os
import time
from os.path import join, dirname, realpath

import stripe
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

from .utilities import render_template
from .middleware import AuthMiddleware
from .data import ApplicationDbContext
from .routers import UserRouter, RecordRouter, IndexRouter, ApiRouter

load_dotenv()

PATH = dirname(dirname(realpath(__file__)))

stripe.api_key = os.getenv("STRIPE_SECRET_API_KEY")

# create the app
app = FastAPI(
    docs_url=None,
    redoc_url=None,
)


@app.exception_handler(500)
async def internal_server_error_handler(req: Request, _exc: Exception):
    return render_template(
        "error.html",
        {"request": req, "error_message": None},
        status_code=500
    )


@app.exception_handler(404)
async def not_found_error_handler(req: Request, _exc: Exception):
    return render_template("not_found.html", {"request": req}, status_code=404)


@app.exception_handler(403)
async def forbidden_error_handler(req: Request, _exc: Exception):
    return render_template(
        "error.html",
        {"request": req, "error_message": "You do not have access to this resource."},
        status_code=403
    )


@app.on_event("startup")
async def startup():
    db = await ApplicationDbContext.connect(
        host="postgres",
        user="postgres",
        password="password",
        database="mavefund"
    )

    # initialize routers
    index_router = IndexRouter(db)

    api = ApiRouter(db)

    ##########################
    # add routers            #
    ##########################
    app.include_router(index_router.router)

    app.include_router(api.router)

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
    time.sleep(3)
    uvicorn.run(
        app,
        ssl_certfile=join(PATH, "cert", "server.crt"),
        ssl_keyfile=join(PATH, "cert", "server.key"),
        loop="asyncio",
        host="0.0.0.0",
        port=443
    )
