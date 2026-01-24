from __future__ import annotations

from celery import Celery
from app.core.config import settings

celery = Celery(
    "reports_generator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks"],
)

celery.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_queue="default",
    task_routes={
        "app.tasks.process_csv_job": {"queue": "default"},
    },
)
