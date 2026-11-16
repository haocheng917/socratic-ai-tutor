from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    pass


class TutorSession(Base):
    __tablename__ = "tutor_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list] = mapped_column(JSONB, default=list)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="sessions")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    sessions: Mapped[list["TutorSession"]
                     ] = relationship(back_populates="user")
