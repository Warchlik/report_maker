from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.celery_app import celery
from app.db.models import Report, ReportStatus
from app.db.session import SessionLocal


@celery.task(
    name="app.tasks.process_csv_job",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=3,
)
def process_report_generation(self, report_id: int):
    db: Session = SessionLocal()

    try:
        # db.execute(select(Report.input_filename).where(Report.id == report_id))
        # db.execute(
        #     update(Report)
        #     .where(Report.id == report_id)
        #     .values(status=ReportStatus.PENDING.value)
        # )

        report: Report | None = db.execute(
            select(Report).where(Report.id == report_id)
        ).scalar_one_or_none()

        if not report:
            raise

        report.status = ReportStatus.PENDING.value
        db.commit()

        # todo -> wywołanie funkjci do robienia raportu

        db.execute(
            update(Report)
            .where(Report.id == report_id)
            .values(status=ReportStatus.COMPLETE.value, finished_at=datetime.now)
        )
    except Exception:
        db.execute(
            update(Report)
            .where(Report.id == report_id)
            .values(status=ReportStatus.FAIL.value, finished_at=datetime.now)
        )
