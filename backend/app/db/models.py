from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ReportStatus(Enum):
    ASSIGNED = 1
    PENDING = 2
    COMPLETE = 3
    FAIL = 0


class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    owner_key: Mapped[str] = mapped_column(String(32), nullable=True, unique=True)
    input_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    output_filename: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    finished_at: Mapped[DateTime | None] = mapped_column(
        DateTime, default=None, nullable=True, onupdate=datetime.now
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    # relationship
    user: Mapped["User | None"] = relationship(back_populates="reports")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # relationship
    reports: Mapped[list["Report"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
