from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qasync import asyncSlot

from src.app.ops import app_ops_menu
from src.schemas.schema_menu import SchemaMenuCreate


class NewMenu(QWidget):
    on_menu_created = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        label_menu_name = QLabel("Menu name:")
        self.line_edit_menu_name = QLineEdit()
        form_layout = QHBoxLayout()
        form_layout.addWidget(label_menu_name)
        form_layout.addWidget(self.line_edit_menu_name)
        self.base_layout.addLayout(form_layout)

        save_menu_button = QPushButton("Save")
        save_menu_button.clicked.connect(self.on_save_clicked_handler)
        self.base_layout.addWidget(save_menu_button)

    @asyncSlot()
    async def on_save_clicked_handler(self):
        await app_ops_menu.create_menu(
            SchemaMenuCreate(name=self.line_edit_menu_name.text().strip())
        )
        self.on_menu_created.emit()
