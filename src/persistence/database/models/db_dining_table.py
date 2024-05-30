from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.persistence.database.models.db_base import DbBase


class DbDiningTable(DbBase):

    __tablename__ = "dining_table"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
