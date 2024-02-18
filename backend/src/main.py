from datetime import datetime

from fastapi import APIRouter, FastAPI
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

from src.api.dependencies import all_api_routers
from src.config import settings


app = FastAPI(title="Quicker API", version="1.0.0", docs_url="/api/docs/")


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
)


@app.get(path="/api/ping/", tags=["Health Check"])
async def ping() -> JSONResponse:
    return JSONResponse(content={"ping": "pong"}, status_code=status.HTTP_200_OK)


async def include_routers(routers: tuple) -> None:
    """Includes all routers specified in the routers tuple"""

    api_router = APIRouter(prefix="/api")

    for router in routers:
        api_router.include_router(router)

    app.include_router(api_router)


@app.on_event("startup")
async def startup() -> None:
    """Executed before the server starts"""

    start_time = datetime.now()

    await include_routers(all_api_routers)  # include all routers specified in the all_api_routers tuple

    end_time = datetime.now()

    print(f"Startup time: {end_time - start_time}")
