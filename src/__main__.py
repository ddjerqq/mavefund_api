import os
from os.path import join
from subprocess import Popen

import stripe
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from src import PATH
from src.utilities import render_template
from src.middleware import AuthMiddleware
from src.data import ApplicationDbContext
from src.routers import IndexRouter, ApiRouter


stripe.api_key = os.getenv("STRIPE_SECRET_API_KEY")

# create the app
app = FastAPI(
    docs_url=None,
    redoc_url=None,
)


@app.exception_handler(Exception)
async def internal_server_error_handler(req: Request, _exc: Exception):
    return render_template(
        "error.html",
        {
            "request": req,
            "error_message": None,
            "title": "internal server error",
        },
        status_code=500
    )


@app.exception_handler(403)
async def forbidden_error_handler(req: Request, _exc: Exception):
    return render_template(
        "error.html",
        {
            "request": req,
            "error_message": "You do not have access to this resource.",
            "title": "forbidden",
        },
        status_code=403
    )


@app.exception_handler(401)
async def unauthorized_error_handler(req: Request, _exc: Exception):
    return render_template(
        "error.html",
        {
            "request": req,
            "error_message": "You must login to access this resource.",
            "title": "unauthorized",
        },
        status_code=401
    )


@app.exception_handler(404)
async def not_found_error_handler(req: Request, _exc: Exception):
    return render_template("not_found.html", {"request": req, "title": "not found"}, status_code=404)




@app.on_event("startup")
async def startup():
    db = await ApplicationDbContext.connect(
        host=os.getenv("POSTGRES_HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="postgres"
    )

    # initialize routers
    index_router = IndexRouter(db)

    api = ApiRouter(db)

    ##########################
    # add routers            #
    ##########################
    app.include_router(index_router.router)

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


    # mount static files
    app.mount("/static", StaticFiles(directory=join(PATH, "static")), name="static")


# make https redirect work
if __name__ == "__main__":

    Popen(["python", join(PATH, "src", "https_redirect.py")])

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
