from contextlib import asynccontextmanager

import uvicorn
from database import engine
from db_models import Base
from fastapi import FastAPI
from routers import items, users

description = """
Example API
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Permissioned routes example API",
    description=description,
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(items.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
