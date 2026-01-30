from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI

from app.api.auth_routes import auth
from app.api.report_routes import reports
from app.db.session import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Tworzę tabele w bazie danych...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabele gotowe!")

    yield

    print("Zamykam połączenie z bazą...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health() -> dict[str, Any]:
    return {"status": 200}


app.include_router(reports, prefix="/v1")
app.include_router(auth, prefix="/auth")
