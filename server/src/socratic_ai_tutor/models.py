from enum import Enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

class Base(DeclarativeBase):
    pass


class TutorMode(str, Enum):
    SOCRATIC = "socratic"
    DIRECT = "direct"


class TutorConversation(Base):
    __tablename__ = "tutor_conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    messages: Mapped[list] = mapped_column(
        MutableList.as_mutable(JSONB), default=list
    )
    tutor_mode: Mapped[TutorMode] = mapped_column(
        SQLEnum(TutorMode),
        default=TutorMode.SOCRATIC,
        nullable=False
    )
    context_tokens: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="conversations")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    membership_plan: Mapped[str] = mapped_column(
        String, nullable=False, default="free"
    )
    membership_expire_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    conversations: Mapped[list["TutorConversation"]] = relationship(
        back_populates="user"
    )
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"
    )

    lifetime_conversations: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    daily_conversations: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    daily_reset_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # tutor_mode: Mapped[TutorMode] = mapped_column(
    #     SQLEnum(TutorMode),
    #     default=TutorMode.SOCRATIC,
    #     nullable=False
    # )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    plan_code: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        String, default="pending", nullable=False
    )

    payment_provider: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(back_populates="orders")
