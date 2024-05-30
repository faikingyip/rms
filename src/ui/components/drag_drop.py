from dataclasses import dataclass

from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


@dataclass
class ShapeInfo:
    id: object
    name: str
    rect: QRect

    @property
    def x(self):
        return self.rect.x()

    @x.setter
    def x(self, new_x):
        self.rect.moveLeft(new_x)

    @property
    def y(self):
        return self.rect.y()

    @y.setter
    def y(self, new_y):
        self.rect.moveTop(new_y)

    @property
    def width(self):
        return self.rect.width()

    @width.setter
    def width(self, new_width):
        self.rect.setWidth(new_width)

    @property
    def height(self):
        return self.rect.height()

    @height.setter
    def height(self, new_height):
        self.rect.setHeight(new_height)


class DragDrop(QWidget):

    on_shape_clicked = Signal(ShapeInfo)
    on_shape_move_finished = Signal(ShapeInfo)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.shape_infos: list[ShapeInfo] = []

        self.dragging = False
        self.drag_offset = QPoint()
        self.dragged_shape_index = -1
        self.selected_index = -1
        self.shaped_moved = False

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw border around the drawing area
        border_rect = QRect(0, 0, self.width(), self.height())
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(border_rect)

        # Draw rectangles
        painter.setBrush(QColor(255, 0, 0))

        for index, shape_info in enumerate(self.shape_infos):
            if index == self.selected_index:
                # Set pen color and width for selected rectangle
                painter.setPen(QPen(QColor(0, 255, 0), 2))
            else:
                # Set pen color and width for unselected rectangles
                painter.setPen(QPen(QColor(0, 0, 255), 1))
            # Draw rectangle outline
            painter.drawRect(shape_info.rect)

            # Draw label inside the rectangle
            label_text = shape_info.name
            label_font = QFont("Arial", 12)
            painter.setFont(label_font)
            painter.drawText(shape_info.rect, Qt.AlignmentFlag.AlignCenter, label_text)

        painter.end()

    def add_shapes(self, shape_infos: list[ShapeInfo]):
        for shape_info in shape_infos:
            self.shape_infos.append(shape_info)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            for index, shape_info in enumerate(self.shape_infos):
                if shape_info.rect.contains(mouse_pos):
                    # print("Clicked inside rectangle")
                    self.dragging = True
                    self.dragged_shape_index = index
                    self.selected_index = index
                    self.drag_offset = mouse_pos - shape_info.rect.topLeft()
                    break

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = event.pos() - self.drag_offset
            # print(f"{event.pos()=} {self.drag_offset=} {new_pos=}")

            # Get the currently moved shape
            shape_info = self.shape_infos[self.dragged_shape_index]

            container_rect = self._calculate_movable_area(shape_info.rect)

            if container_rect.contains(new_pos):
                self.shaped_moved = True
                self.shape_infos[self.dragged_shape_index].rect.moveTopLeft(new_pos)

            # Redraw widget with new rectangle position
            self.update()

    def mouseReleaseEvent(self, event):
        # print("Mouse Release Event")
        if event.button() == Qt.MouseButton.LeftButton:

            # -1 means no shapes on there.
            if self.dragged_shape_index > -1:

                # Get the currently moved shape
                shape_info = self.shape_infos[self.dragged_shape_index]

                self.dragging = False
                self.dragged_shape_index = -1

                # Redraw widget with new rectangle position
                self.update()

                self.on_shape_clicked.emit(shape_info)

                if self.shaped_moved:
                    self.on_shape_move_finished.emit(shape_info)
                    self.shaped_moved = False

    def _calculate_movable_area(self, shape):
        """
        Calculates and returns the area in which
        the specified shape can move to.
        Adjusted to exclude the border and any
        padding or margins of the parent container
        """

        self_x = self.geometry().x()
        self_y = self.geometry().y()
        return self.geometry().adjusted(
            -self_x,
            -self_y,
            -(shape.width() + self_x),
            -(shape.height() + self_y),
        )

    def clear_selection(self):
        self.selected_index = -1

    def remove_selected_shape(self):
        self.shape_infos.pop(self.selected_index)
        self.selected_index = -1
        self.update()
