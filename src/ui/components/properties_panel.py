from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.ui.components.drag_drop import ShapeInfo

MIN_SHAPE_WIDTH = MIN_SHAPE_HEIGHT = 50
MAX_SHAPE_WIDTH = MAX_SHAPE_HEIGHT = 200

# This needs to be calculated rather than be a constant
MIN_SHAPE_X = MIN_SHAPE_Y = 0
MAX_SHAPE_X = 1150
MAX_SHAPE_Y = 900


class PropertiesPanel(QWidget):
    on_shape_position_changed = Signal(ShapeInfo)
    on_shape_size_changed = Signal(ShapeInfo)
    on_shape_name_changed = Signal(ShapeInfo)
    on_delete_shape_confirmed = Signal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.shape_info = None
        self.programmatic_change = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Table Id
        table_id_label = QLabel("Table Id:")
        self.table_id_edit = QLineEdit()
        self.table_id_edit.setEnabled(False)
        layout.addWidget(table_id_label)
        layout.addWidget(self.table_id_edit)

        # Table Name
        table_name_label = QLabel("Table Name:")
        self.table_name_edit = QLineEdit()
        layout.addWidget(table_name_label)
        layout.addWidget(self.table_name_edit)
        self.table_name_edit.editingFinished.connect(self.on_shape_name_changed_handler)

        # X Position
        x_label = QLabel("X Position:")
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setMinimum(MIN_SHAPE_X)
        self.x_spinbox.setMaximum(MAX_SHAPE_X)
        layout.addWidget(x_label)
        layout.addWidget(self.x_spinbox)
        self.x_spinbox.editingFinished.connect(self.on_x_changed_handler)

        # Y Position
        y_label = QLabel("Y Position:")
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setMinimum(MIN_SHAPE_Y)
        self.y_spinbox.setMaximum(MAX_SHAPE_Y)
        layout.addWidget(y_label)
        layout.addWidget(self.y_spinbox)
        self.y_spinbox.editingFinished.connect(self.on_y_changed_handler)

        # Width
        width_label = QLabel("Width:")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setMinimum(MIN_SHAPE_WIDTH)
        self.width_spinbox.setMaximum(MAX_SHAPE_WIDTH)
        layout.addWidget(width_label)
        layout.addWidget(self.width_spinbox)
        self.width_spinbox.editingFinished.connect(self.on_width_changed_handler)

        # Height
        height_label = QLabel("Height:")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setMinimum(MIN_SHAPE_HEIGHT)
        self.height_spinbox.setMaximum(MAX_SHAPE_HEIGHT)
        layout.addWidget(height_label)
        layout.addWidget(self.height_spinbox)
        self.height_spinbox.editingFinished.connect(self.on_height_changed_handler)

        # Delete button
        self.push_button_delete = QPushButton()
        self.push_button_delete.setText("Delete")
        layout.addWidget(self.push_button_delete)
        self.push_button_delete.clicked.connect(
            self.on_delete_request_confirmation_handler
        )

        self.setLayout(layout)

    def on_shape_name_changed_handler(self):
        if self.programmatic_change:
            return
        self.shape_info.name = self.table_name_edit.text()
        self.on_shape_name_changed.emit(self.shape_info)

    def on_x_changed_handler(self):
        if self.programmatic_change:
            return
        self.shape_info.x = self.x_spinbox.value()
        self.on_shape_position_changed.emit(self.shape_info)

    def on_y_changed_handler(self):
        if self.programmatic_change:
            return
        self.shape_info.y = self.y_spinbox.value()
        self.on_shape_position_changed.emit(self.shape_info)

    def on_width_changed_handler(self):
        if self.programmatic_change:
            return
        self.shape_info.width = self.width_spinbox.value()
        self.on_shape_size_changed.emit(self.shape_info)

    def on_height_changed_handler(self):
        if self.programmatic_change:
            return
        self.shape_info.height = self.height_spinbox.value()
        self.on_shape_size_changed.emit(self.shape_info)

    def on_delete_request_confirmation_handler(self):
        if self.table_id_edit.text():
            # Don't ask for confirmation. Just delete.
            self.on_delete_shape_confirmed.emit(self.table_id_edit.text())

    def set_shape_info(self, shape_info: ShapeInfo):
        self.programmatic_change = True
        self.shape_info = shape_info
        self.x_spinbox.setValue(shape_info.x)
        self.y_spinbox.setValue(shape_info.y)
        self.width_spinbox.setValue(shape_info.width)
        self.height_spinbox.setValue(shape_info.height)
        self.table_name_edit.setText(shape_info.name)
        self.table_id_edit.setText(str(shape_info.id))
        self.programmatic_change = False

    def clear_shape_info(self):
        self.width_spinbox.setValue(50)
        self.height_spinbox.setValue(50)
        self.x_spinbox.setValue(0)
        self.y_spinbox.setValue(0)
        self.table_name_edit.setText("")
        self.table_id_edit.setText("")
        self.shape_info = None
