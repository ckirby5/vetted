from api.models.base import Base
from sqlalchemy import JSON, DateTime, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from datetime import datetime

class Program(Base):
    __tablename__ = "programs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    jurisdiction: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    last_scraped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    eligibility_rules: Mapped[list["EligibilityRule"]] = relationship("EligibilityRule", back_populates="program", cascade="all, delete-orphan")

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    program_id: Mapped[UUID] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    program: Mapped["Program"] = relationship("Program", back_populates="eligibility_rules")