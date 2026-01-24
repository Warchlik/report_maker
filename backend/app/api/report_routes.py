from datetime import datetime
from typing import Any
from fastapi import APIRouter, Depends, File, HTTPException, Header, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Report, ReportStatus
from app.db.session import db
from app.utils.helper import save_file


jobs = APIRouter()


def _request_client_id(x_client_id: str | None) -> str:
    if not x_client_id:
        raise HTTPException(status_code=400, detail="None value in client_id")
    if len(x_client_id) > 64:
        raise HTTPException(status_code=400, detail="Invalid lenght for client_id")
    return x_client_id


@jobs.post("/reports/upload")
async def upload_job(
    file: UploadFile = File(...),
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
) -> dict[str, Any]:
    owner_key: str = _request_client_id(x_client_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_filename = f"{timestamp}_input.csv"
    if not input_filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid filename extention")

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400, detail="Csv has no enought data to create report"
        )

    del content

    is_file_save = save_file(owner_key, file, input_filename)
    if not is_file_save:
        raise HTTPException(status_code=400, detail="Error witch procesing file")

    report = Report(input_filename=input_filename, status=ReportStatus.ASSIGNED.value)
    db.add(report)
    db.commit()
    db.refresh(report)

    # todo -> add calary

    return {"id": report.id, "filename": report.input_filename, "owner_key": owner_key}


@jobs.get("/reports")
async def list_jobs(
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
) -> list[dict[str, Any]]:
    owner_key = _request_client_id(x_client_id)

    reports = (
        db.execute(
            select(Report)
            .where(Report.user_id == owner_key)
            .order_by(Report.created_at.desc())
        )
        .scalars()
        .all()
    )

    return [
        {
            "id": r.id,
            "status": r.status,
            "created_at": r.created_at,
            "finished_at": r.finished_at,
            "filename": r.output_filename,
        }
        for r in reports
    ]


@jobs.get("/report/{report_id}")
def get_job(
    report_id: int,
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
):
    owner_key = _request_client_id(x_client_id)

    report = db.execute(
        select(Report).where(Report.id == report_id, Report.user_id == owner_key)
    ).scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=400, detail="Can not find jobs witch this id")

    return report
