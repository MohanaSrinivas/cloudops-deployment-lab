from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    applications: Mapped[list["Application"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(160), index=True)
    role: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(32), default="saved", index=True)
    job_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner: Mapped[User] = relationship(back_populates="applications")
