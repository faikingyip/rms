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

from src.app.ops import app_ops_menu


class EditMenu(QWidget):
    on_menu_updated = Signal()

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

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.base_layout.addWidget(scroll_area)

        menu_items = QWidget()
        menu_items_form_layout = QVBoxLayout()
        menu_items.setLayout(menu_items_form_layout)

        for i in range(20):
            label = QLabel(f"Label {i + 1}")
            menu_items_form_layout.addWidget(label)
            button = QPushButton(f"Button {i + 1}")
            menu_items_form_layout.addWidget(button)

        scroll_area.setWidget(menu_items)

        save_menu_button = QPushButton("Save")
        save_menu_button.clicked.connect(self.on_save_clicked_handler)
        self.base_layout.addWidget(save_menu_button)

    @asyncSlot()
    async def on_save_clicked_handler(self):
        # await app_ops_menu.create_menu(
        #     SchemaMenuCreate(name=self.line_edit_menu_name.text().strip())
        # )
        self.on_menu_updated.emit()
