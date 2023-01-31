import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.route("/{_:path}")
async def https_redirect(request: Request):
    return RedirectResponse(
        request.url.replace(scheme="https"),
        status_code=301,
    )


# if __name__ == "__main__":
#     uvicorn.run(app, port=80, host="0.0.0.0")
