import asyncio

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from qasync import asyncSlot

from src.app.ops import app_ops_tag
from src.ui.edit_tag import EditTag
from src.ui.new_tag import NewTag
from src.ui.ui_utils import clear_layout

TAGS_PAGE_INDEX = 0
TAGS_PAGE_SIZE = 50
TAGS_SORT_BY = "name"


class Tags(QWidget):
    def __init__(self):
        super().__init__()
        asyncio.ensure_future(self.init_ui())

    async def init_ui(self):
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)
        await self._load_content()

    def on_create_tag_requested_handler(self):
        clear_layout(self.base_layout)
        new_tag = NewTag()
        new_tag.on_tag_created.connect(self.on_tag_created_handler)
        self.base_layout.addWidget(new_tag)

    @asyncSlot()
    async def on_tag_created_handler(self):
        await self._load_content()

    async def _load_content(self):
        clear_layout(self.base_layout)

        tags = await app_ops_tag.get_tag_list(
            TAGS_PAGE_INDEX, TAGS_PAGE_SIZE, TAGS_SORT_BY
        )
        for tag in tags:
            tag_button = QPushButton(tag.name)
            tag_button.clicked.connect(self.on_tag_selected_handler)
            self.base_layout.addWidget(tag_button)

        create_tag_button = QPushButton("Create Tag")
        create_tag_button.clicked.connect(self.on_create_tag_requested_handler)
        self.base_layout.addWidget(create_tag_button)

    @Slot()
    def on_tag_selected_handler(self):
        clear_layout(self.base_layout)
        edit_tag = EditTag()
        edit_tag.on_tag_updated.connect(self.on_tag_updated_handler)
        self.base_layout.addWidget(edit_tag)

    @asyncSlot()
    async def on_tag_updated_handler(self):
        await self._load_content()
