import asyncio

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from qasync import asyncSlot

from src.app.ops import app_ops_dining_table
from src.schemas.schema_dining_table import (
    SchemaDiningTableCreate,
    SchemaUpdateName,
    SchemaUpdatePosition,
    SchemaUpdateSize,
)
from src.ui.components.drag_drop import DragDrop, ShapeInfo
from src.ui.components.properties_panel import PropertiesPanel

DEFAULT_TABLE_NAME = "No name"
DEFAULT_TABLE_X = DEFAULT_TABLE_Y = 1
DEFAULT_TABLE_WIDTH = DEFAULT_TABLE_HEIGHT = 100


class Tables(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.drag_drop = DragDrop(self)
        self.drag_drop.on_shape_move_finished.connect(
            self.on_table_move_finished_handler
        )
        self.drag_drop.on_shape_clicked.connect(self.on_table_clicked_handler)

        self.create_table_button = QPushButton("Create Table")
        self.create_table_button.clicked.connect(self.on_create_table_handler)
        v_box = QVBoxLayout()
        v_box.addWidget(self.drag_drop)
        v_box.addWidget(self.create_table_button)

        self.properties_panel = PropertiesPanel()
        self.properties_panel.on_delete_shape_confirmed.connect(
            self.on_properties_panel_delete_confirmed_handler
        )
        self.properties_panel.on_shape_name_changed.connect(
            self.on_properties_panel_table_name_changed_handler
        )

        self.properties_panel.on_shape_position_changed.connect(
            self.on_properties_panel_table_position_changed_handler
        )

        self.properties_panel.on_shape_size_changed.connect(
            self.on_properties_panel_table_size_changed_handler
        )

        main_box = QHBoxLayout()
        main_box.addLayout(v_box, 3)
        main_box.addWidget(self.properties_panel, 1)
        self.setLayout(main_box)
        asyncio.ensure_future(self._load_existing_tables())

    async def _load_existing_tables(self):
        tables = await app_ops_dining_table.get_dining_table_list(0, 500, None)
        self.drag_drop.add_shapes(
            ShapeInfo(
                table.id,
                table.name,
                QRect(table.x, table.y, table.width, table.height),
            )
            for table in tables
        )

    def on_table_clicked_handler(self, shape_info: ShapeInfo):
        self.properties_panel.set_shape_info(shape_info)

    @asyncSlot()
    async def on_create_table_handler(self):
        new_record = await app_ops_dining_table.create_dining_table(
            SchemaDiningTableCreate(
                name=DEFAULT_TABLE_NAME,
                x=DEFAULT_TABLE_X,
                y=DEFAULT_TABLE_Y,
                width=DEFAULT_TABLE_WIDTH,
                height=DEFAULT_TABLE_HEIGHT,
            )
        )

        self.drag_drop.add_shapes(
            [
                ShapeInfo(
                    new_record.id,
                    new_record.name,
                    QRect(
                        new_record.x, new_record.y, new_record.width, new_record.height
                    ),
                )
            ]
        )

    @asyncSlot()
    async def on_properties_panel_table_position_changed_handler(
        self, shape_info: ShapeInfo
    ):
        self.drag_drop.update()
        await self.update_table_position(shape_info)

    @asyncSlot()
    async def on_properties_panel_table_size_changed_handler(
        self, shape_info: ShapeInfo
    ):
        self.drag_drop.update()
        await app_ops_dining_table.update_size(
            shape_info.id,
            SchemaUpdateSize(width=shape_info.width, height=shape_info.height),
        )

    @asyncSlot()
    async def on_properties_panel_table_name_changed_handler(
        self, shape_info: ShapeInfo
    ):
        self.drag_drop.update()
        await app_ops_dining_table.update_name(
            shape_info.id, SchemaUpdateName(name=shape_info.name)
        )

    @asyncSlot()
    async def on_properties_panel_delete_confirmed_handler(self, shape_id):
        await app_ops_dining_table.delete_dining_table(shape_id)
        self.properties_panel.clear_shape_info()
        self.drag_drop.remove_selected_shape()

    @asyncSlot()
    async def on_table_move_finished_handler(self, shape_info: ShapeInfo):
        await self.update_table_position(shape_info)

    async def update_table_position(self, shape_info: ShapeInfo):
        await app_ops_dining_table.update_position(
            shape_info.id,
            SchemaUpdatePosition(x=shape_info.x, y=shape_info.y),
        )
