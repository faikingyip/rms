from PySide6.QtWidgets import QLayout


def clear_layout(layout: QLayout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)
