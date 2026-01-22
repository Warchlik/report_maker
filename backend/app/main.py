from fastapi import FastAPI

from app.api.auth import auth
from app.api.jobs import jobs

app = FastAPI()

app.include_router(jobs, prefix="/v1")
app.include_router(auth, prefix="/auth")
