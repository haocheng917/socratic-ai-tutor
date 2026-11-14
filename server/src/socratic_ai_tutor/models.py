from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class TutorSession(Base):
    __tablename__ = "tutor_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list] = mapped_column(JSONB, default=list)