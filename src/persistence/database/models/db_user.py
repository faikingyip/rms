from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.persistence.database.models.db_base import DbBase


class DbUser(DbBase):

    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(300), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

    # Add multiple composite unique constraints
    __table_args__ = (
        UniqueConstraint("username"),
        # Add more UniqueConstraint objects if needed
    )
