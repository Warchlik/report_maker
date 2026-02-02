from datetime import datetime
from typing import Any, Optional
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Report, ReportStatus, User
from app.db.session import db
from app.utils.csv_validator import generate_report
from app.utils.helper import save_file
from app.utils.validator import current_user_cookie


reports = APIRouter()


@reports.post("/reports/upload")
async def upload_job(
    background_task: BackgroundTasks,
    file: UploadFile = File(...),
    user: Optional[User] = Depends(current_user_cookie),
    db: AsyncSession = Depends(db),
) -> dict[str, Any]:
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_filename = f"{timestamp}_input.csv"
    if not input_filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid filename extention")

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400, detail="Csv has no enought data to create report"
        )

    # del content

    is_file_save = save_file(user.id, file, input_filename)
    if not is_file_save:
        raise HTTPException(status_code=400, detail="Error witch procesing file")

    report = Report(input_filename=input_filename, status=ReportStatus.ASSIGNED.value)
    try:
        db.add(report)
        await db.commit()
        await db.refresh(report)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    # TODO: finish background functionality to generate pdf
    background_task.add_task(generate_report, user.id, content)

    return {"id": report.id, "filename": report.input_filename, "user_id": user.id}


@reports.get("/reports")
async def list_jobs(
    user: Optional[User] = Depends(current_user_cookie),
    db: AsyncSession = Depends(db),
) -> list[dict[str, Any]]:
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    reports = (
        await db.scalars(
            select(Report)
            .where(Report.user_id == user.id)
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
    user: Optional[User] = Depends(current_user_cookie),
    db: AsyncSession = Depends(db),
):
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    report: Optional[Report] = (
        await db.scalars(
            select(Report).where(Report.id == report_id, Report.user_id == user.id)
        )
    ).one_or_none()

    if not report:
        raise HTTPException(status_code=400, detail="Can not find jobs witch this id")

    return report
