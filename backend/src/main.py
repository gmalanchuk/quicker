from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI(title="Quicker API", version="1.0.0", docs_url="/api/docs/")


@app.get("/api/ping/")
async def ping() -> JSONResponse:
    return JSONResponse(content={"ping": "pong"}, status_code=status.HTTP_200_OK)


@app.get("/api/pong/")
async def pong() -> JSONResponse:
    return JSONResponse(content={"pong": "ping"}, status_code=status.HTTP_200_OK)
