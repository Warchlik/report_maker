from fastapi import APIRouter, Depends, File, Header, UploadFile
from sqlalchemy.orm import Session

from app.db.session import db


jobs = APIRouter()


@jobs.post("generate_report")
def generate_report(
    file: UploadFile = File(...),
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
):
    pass
