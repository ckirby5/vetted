from api.models.base import Base
from sqlalchemy import Date, DateTime, String, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from datetime import date, datetime

from api.models.constants import ChecklistStatus
from api.models.program import Program

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    service_era_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    service_era_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    discharge_status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    disability_rating: Mapped[int | None] = mapped_column(nullable=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)

    saved_matches: Mapped[list["SavedMatch"]] = relationship("SavedMatch", back_populates="user_profile", cascade="all, delete-orphan")

class SavedMatch(Base):
    __tablename__ = "saved_matches"
    __table_args__ = (UniqueConstraint("user_id", "program_id"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)
    program_id: Mapped[UUID] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    checklist_status: Mapped[str] = mapped_column(String(255), nullable=False, default=ChecklistStatus.NOT_STARTED.value)

    user_profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="saved_matches")
    program: Mapped["Program"] = relationship("Program")