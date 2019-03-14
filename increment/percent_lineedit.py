from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QTextLayout, QPainter, QPen


class PercentLineEdit(QLineEdit):
    def paintEvent(self, event):
        super().paintEvent(event)
        text = self.text()
        if not text or text.endswith('%'):
            return
        self.ensurePolished()

        layout = QTextLayout('%', self.font())

        painter = QPainter(self)
        pos = (painter.boundingRect(self.rect(), Qt.AlignVCenter, text).topRight()
               + painter.boundingRect(self.rect(), Qt.AlignVCenter, text + '%').topRight()) \
              / 2

        layout.beginLayout()
        line = layout.createLine()
        line.setLineWidth(self.width() - pos.x())
        line.setPosition(pos)
        layout.endLayout()

        painter.setPen(QPen(Qt.gray, 1))
        layout.draw(painter, QPoint(0, 0))
