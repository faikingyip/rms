import asyncio
import os
import sys

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.app.ops import app_ops_user
from src.configuration import Configuration
from src.persistence.database import session

# Needed to create the database tables
from src.persistence.database.models import *
from src.schemas.schema_user import SchemaUserCreate
from src.ui.orderit import OrderItMainWindow


async def setup_database():
    await session.create_database_tables()
    await app_ops_user.create_user(
        SchemaUserCreate(
            username=Configuration.INITIAL_USER_1__USERNAME,
            password=Configuration.INITIAL_USER_1__PASSWORD,
        )
    )
    await app_ops_user.create_user(
        SchemaUserCreate(
            username=Configuration.INITIAL_USER_2__USERNAME,
            password=Configuration.INITIAL_USER_2__PASSWORD,
        )
    )


def setup():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    async def run_in_order():
        for func in [setup_database]:
            await func()

    with loop:
        loop.run_until_complete(run_in_order())

    print("Setup completed")


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = OrderItMainWindow(app)
    window.show()
    with loop:
        # This replaces app.exec()
        loop.run_forever()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
    else:
        main()
