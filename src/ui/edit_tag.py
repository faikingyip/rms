from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from qasync import asyncSlot

from src.app.ops import app_ops_tag
from src.schemas import schema_tag


class EditTag(QWidget):
    on_tag_updated = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        label_tag_name = QLabel("Tag name:")
        self.line_edit_tag_name = QLineEdit()
        form_layout = QHBoxLayout()
        form_layout.addWidget(label_tag_name)
        form_layout.addWidget(self.line_edit_tag_name)
        self.base_layout.addLayout(form_layout)

        save_tag_button = QPushButton("Save")
        save_tag_button.clicked.connect(self.on_save_clicked_handler)
        self.base_layout.addWidget(save_tag_button)

    @asyncSlot()
    async def on_save_clicked_handler(self):
        # await app_ops_tag.update_name(
        #     schema_tag.SchemaUpdateName(name=self.line_edit_tag_name.text().strip())
        # )
        self.on_tag_updated.emit()
