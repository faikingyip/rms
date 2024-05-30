import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.persistence.database.session import Base


class DbBase(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    created_on: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        nullable=False,
    )
    last_updated_on: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def has_changes(self, obj, comparison_keys):
        """
        Returns True if the specified object has all the keys and that the
        values of these keys are the same assigned to the Model, else False.
        """

        self_dict = self.__dict__

        for comparison_key in comparison_keys:
            if comparison_key not in obj or obj[comparison_key] != self_dict.get(
                comparison_key
            ):
                # Changes found.
                return True

        # No changes found.
        return False

    def assign_values(self, obj, keys):
        """
        The value of each of the specified keys of this model will be
        assigned the values of the specified object.
        """

        for key in keys:
            setattr(self, key, obj[key])
