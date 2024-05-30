from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.persistence.database.models.db_base import DbBase


class DbMenu(DbBase):

    __tablename__ = "menu"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
