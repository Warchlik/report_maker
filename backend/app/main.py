from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.auth_routes import auth
from app.api.report_routes import reports
from app.db.session import Base, engine


# Method for development, in ending backend need alembic migration to succesfuly integration with production setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database connection and datatables prepearing succesfuly")

    yield

    print("Database connection closed")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(reports, prefix="/v1")
app.include_router(auth, prefix="/auth")
