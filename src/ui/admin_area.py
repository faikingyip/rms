from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from qasync import asyncSlot

from src.ui.menus import Menus
from src.ui.tables import Tables
from src.ui.ui_utils import clear_layout


class AdminArea(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        items_button = QPushButton("Items")
        items_button.clicked.connect(self.on_items_button_clicked_handler)

        menus_button = QPushButton("Menus")
        menus_button.clicked.connect(self.on_menus_button_clicked_handler)

        tables_button = QPushButton("Tables")
        tables_button.clicked.connect(self.on_tables_button_clicked_handler)

        v_box_left = QVBoxLayout()
        v_box_left.addWidget(items_button)
        v_box_left.addWidget(menus_button)
        v_box_left.addWidget(tables_button)

        self.main_content_layout = QVBoxLayout()
        h_box = QHBoxLayout()
        h_box.addLayout(v_box_left, 1)
        h_box.addLayout(self.main_content_layout, 5)

        self.setLayout(h_box)

    @Slot()
    def on_items_button_clicked_handler(self):
        clear_layout(self.main_content_layout)
        pass
        # menus = Menus()
        # self.main_content_layout.addWidget(menus)

    @Slot()
    def on_menus_button_clicked_handler(self):
        clear_layout(self.main_content_layout)

        menus = Menus()
        self.main_content_layout.addWidget(menus)

    @Slot()
    def on_tables_button_clicked_handler(self):
        clear_layout(self.main_content_layout)

        tables = Tables()
        self.main_content_layout.addWidget(tables)
