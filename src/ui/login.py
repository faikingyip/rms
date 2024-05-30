from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLineEdit, QVBoxLayout, QWidget
from qasync import asyncSlot

from src.app.ops.app_ops_user import login
from src.schemas.schema_user import SchemaUserDisplay
from src.ui.components.pinpad import PinPad
from src.ui.user_type import UserType


class Login(QWidget):
    on_credentials_success = Signal(SchemaUserDisplay)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.user_selection = QComboBox(self)
        self.user_selection.addItems([UserType.USER.value, UserType.ADMIN.value])
        self.user_selection.setCurrentText(UserType.USER.value)
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.pinpad = PinPad()
        self.pinpad.on_button_pressed.connect(self.on_pinpad_button_clicked_handler)

        v_box = QVBoxLayout()

        v_box.addWidget(self.user_selection)
        v_box.addWidget(self.display)
        v_box.addWidget(self.pinpad)
        self.setLayout(v_box)

    @asyncSlot(str)
    async def on_pinpad_button_clicked_handler(self, clicked_text):
        current_text = self.display.text()
        if clicked_text == "X":
            self.display.clear()
        elif clicked_text == "GO":
            await self._login()
        else:
            self.display.setText(current_text + clicked_text)

    async def _login(self):
        user = await login(self.user_selection.currentText(), self.display.text())
        if user:
            self.on_credentials_success.emit(user)
