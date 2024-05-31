import asyncio

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from qasync import asyncSlot

from src.app.ops import app_ops_menu
from src.ui.edit_menu import EditMenu
from src.ui.new_menu import NewMenu
from src.ui.ui_utils import clear_layout

MENUS_PAGE_INDEX = 0
MENUS_PAGE_SIZE = 50
MENUS_SORT_BY = "name"


class Menus(QWidget):
    def __init__(self):
        super().__init__()
        asyncio.ensure_future(self.init_ui())

    async def init_ui(self):
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)
        await self._load_content()

    def on_create_menu_requested_handler(self):
        clear_layout(self.base_layout)
        new_menu = NewMenu()
        new_menu.on_menu_created.connect(self.on_menu_created_handler)
        self.base_layout.addWidget(new_menu)

    @asyncSlot()
    async def on_menu_created_handler(self):
        await self._load_content()

    async def _load_content(self):
        clear_layout(self.base_layout)

        menus = await app_ops_menu.get_menu_list(
            MENUS_PAGE_INDEX, MENUS_PAGE_SIZE, MENUS_SORT_BY
        )
        for menu in menus:
            menu_button = QPushButton(menu.name)
            menu_button.clicked.connect(self.on_menu_selected_handler)
            self.base_layout.addWidget(menu_button)

        create_menu_button = QPushButton("Create Menu")
        create_menu_button.clicked.connect(self.on_create_menu_requested_handler)
        self.base_layout.addWidget(create_menu_button)

    @Slot()
    def on_menu_selected_handler(self):
        clear_layout(self.base_layout)
        edit_menu = EditMenu()
        edit_menu.on_menu_updated.connect(self.on_menu_updated_handler)
        self.base_layout.addWidget(edit_menu)

    @asyncSlot()
    async def on_menu_updated_handler(self):
        await self._load_content()
