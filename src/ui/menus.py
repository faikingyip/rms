import asyncio

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from qasync import asyncSlot


class Menus(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.create_menu_button = QPushButton("Create Menu")
        self.create_menu_button.clicked.connect(self.on_create_menu_handler)
        v_box = QVBoxLayout()
        v_box.addWidget(self.create_menu_button)

        self.setLayout(v_box)
        asyncio.ensure_future(self._load_existing_menus())

    async def _load_existing_menus(self):
        pass
        # menus = await app_ops_menu.get_menu_list(0, 50, "name")

    @asyncSlot()
    async def on_create_menu_handler(self):
        pass
        # new_record = await app_ops_dining_table.create_dining_table(
        #     SchemaDiningTableCreate(
        #         name=DEFAULT_TABLE_NAME,
        #         x=DEFAULT_TABLE_X,
        #         y=DEFAULT_TABLE_Y,
        #         width=DEFAULT_TABLE_WIDTH,
        #         height=DEFAULT_TABLE_HEIGHT,
        #     )
        # )
