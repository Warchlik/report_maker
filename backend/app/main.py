from fastapi import FastAPI

from app.api.auth_routes import auth
from app.api.report_routes import reports

app = FastAPI()

app.include_router(reports, prefix="/v1")
app.include_router(auth, prefix="/auth")
