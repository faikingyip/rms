import asyncio

from PySide6.QtWidgets import QMainWindow

from src.app.ops.app_ops_dining_table import get_dining_table_list
from src.ui.admin_area import AdminArea
from src.ui.login import Login
from src.ui.user_type import UserType


class OrderItMainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        asyncio.ensure_future(get_dining_table_list(0, 10, None))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Order It!")
        self.setGeometry(100, 100, 800, 600)

        self.setup_menu_bar()

        self.display_login()

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)

    def quit(self):
        self.app.quit()

    def on_credentials_success_handler(self, user):
        if user.username == UserType.ADMIN.value:
            self.display_area_admin()
        elif user.username == UserType.USER.value:
            self.display_area_user()
        else:
            raise ValueError("Non-standard user detected.")

    def display_login(self):
        login = Login()
        login.on_credentials_success.connect(self.on_credentials_success_handler)
        self.setCentralWidget(login)

    def display_area_admin(self):
        admin_area = AdminArea()
        self.setCentralWidget(admin_area)

    def display_area_user(self):
        pass
