from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.controllers.post_controller import router as post_router
from app.core.database import Base, engine
from app.services.post_service import PostNotFoundError


def create_app(*, initialize_database: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        if initialize_database:
            Base.metadata.create_all(bind=engine)
        yield

    application = FastAPI(
        title="Simple Board API",
        description="FastAPI 3-tier CRUD learning project",
        version="1.0.0",
        lifespan=lifespan,
    )

    @application.exception_handler(PostNotFoundError)
    async def post_not_found_handler(
        _: Request, exc: PostNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    application.include_router(post_router, prefix="/api")
    return application


app = create_app()

