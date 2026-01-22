from typing import Any
from fastapi import APIRouter, Depends, File, HTTPException, Header, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Jobs
from app.db.session import db


jobs = APIRouter()


def _request_client_id(x_client_id: str | None) -> str:
    if not x_client_id:
        raise HTTPException(status_code=400, detail="None value in client_id")
    if len(x_client_id) > 64:
        raise HTTPException(status_code=400, detail="Invalid lenght for client_id")
    return x_client_id


@jobs.post("/jobs/upload")
async def upload_job(
    file: UploadFile = File(...),
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
) -> dict[str, Any]:
    owner_key: str = _request_client_id(x_client_id)

    filename = file.filename or "x_client_id_upload.csv"
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid filename extention")

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400, detail="Csv has no enought data to create report"
        )

    job = Jobs(status="PENDING", filename=filename)
    db.add(job)
    db.commit()
    db.refresh(job)

    # todo -> add calary

    return {"id": job.id, "filename": job.filename, "owner_key": owner_key}


@jobs.get("/jobs")
async def list_jobs(
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
) -> list[dict[str, Any]]:
    owner_key = _request_client_id(x_client_id)

    jobs = (
        db.execute(
            select(Jobs)
            .where(Jobs.user_id == owner_key)
            .order_by(Jobs.created_at.desc())
        )
        .scalars()
        .all()
    )

    return [
        {
            "id": job.id,
            "status": job.status,
            "created_at": job.created_at,
            "finished_at": job.finished_at,
            "filename": job.filename,
        }
        for job in jobs
    ]


@jobs.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    db: Session = Depends(db),
):
    owner_key = _request_client_id(x_client_id)

    job = db.execute(
        select(Jobs).where(Jobs.id == job_id, Jobs.user_id == owner_key)
    ).scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=400, detail="Can not find jobs witch this id")

    return job
