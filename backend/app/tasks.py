from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Report, ReportStatus
from app.db.session import SessionLocal


# TODO: i think this have to be deleted to analise
async def process_report_generation(report_id: int):
    db: AsyncSession = SessionLocal()

    try:
        report: Report | None = await db.scalar(
            select(Report).where(Report.id == report_id)
        )

        if not report:
            raise

        report.status = ReportStatus.PENDING.value
        await db.commit()

        # todo -> wywołanie funkjci do robienia raportu

        await db.execute(
            update(Report)
            .where(Report.id == report_id)
            .values(status=ReportStatus.COMPLETE.value, finished_at=datetime.now)
        )
    except Exception:
        await db.execute(
            update(Report)
            .where(Report.id == report_id)
            .values(status=ReportStatus.FAIL.value, finished_at=datetime.now)
        )
