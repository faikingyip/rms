from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget

PINPAD_BUTTONS_MAP = {
    "1": (0, 0),
    "2": (0, 1),
    "3": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (2, 0),
    "8": (2, 1),
    "9": (2, 2),
    "0": (3, 1),
    "X": (3, 0),
    "GO": (3, 2),
}


def create_buttons_to_grid_layout(
    pinpad_buttons_map,
    grid_layout: QGridLayout,
    parent_widget,
    on_button_clicked_handler,
):
    for button_text, index in pinpad_buttons_map.items():
        button = QPushButton(button_text, parent_widget)
        button.clicked.connect(on_button_clicked_handler)
        grid_layout.addWidget(button, *index)


class PinPad(QWidget):
    on_button_pressed = Signal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()

        create_buttons_to_grid_layout(
            PINPAD_BUTTONS_MAP, grid, self, self.on_button_clicked_handler
        )

        self.setLayout(grid)

    @Slot()
    def on_button_clicked_handler(self):
        sender = self.sender()
        text = sender.text()
        self.on_button_pressed.emit(text)
