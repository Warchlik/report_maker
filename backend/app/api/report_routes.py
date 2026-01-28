from datetime import datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, File, HTTPException, Header, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.models import Report, ReportStatus
from app.db.session import db
from app.utils.helper import save_file


reports = APIRouter()


async def _request_client_id(x_client_id: str | None) -> str:
    if not x_client_id:
        raise HTTPException(status_code=400, detail="None value in client_id")
    if len(x_client_id) > 64:
        raise HTTPException(status_code=400, detail="Invalid lenght for client_id")
    return x_client_id


@reports.post("/reports/upload")
async def upload_job(
    file: UploadFile = File(...),
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
) -> dict[str, Any]:
    owner_key: str = await _request_client_id(x_client_id)

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

    # TODO: -> add calary or background task | background task would by better in my situation

    return {"id": report.id, "filename": report.input_filename, "owner_key": owner_key}


@reports.get("/reports")
async def list_jobs(
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: AsyncSession = Depends(db),
) -> list[dict[str, Any]]:
    owner_key = await _request_client_id(x_client_id)

    reports = (
        await db.scalars(
            select(Report)
            .where(Report.user_id == owner_key)
            .order_by(Report.created_at.desc())
        )
    ).all()

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


@reports.get("/report/{report_id}")
async def get_report(
    report_id: int,
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: AsyncSession = Depends(db),
):
    owner_key = await _request_client_id(x_client_id)

    report: Optional[Report] = (
        await db.scalars(
            select(Report).where(Report.id == report_id, Report.user_id == owner_key)
        )
    ).one_or_none()

    if not report:
        raise HTTPException(status_code=400, detail="Can not find jobs witch this id")

    return report
