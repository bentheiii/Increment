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

        cr = self.cursorRect()

        pos = painter.boundingRect(self.rect(), Qt.AlignVCenter, text).topRight() + QPoint(cr.width() // 2,
                                                                                           cr.top() // 4)

        layout.beginLayout()
        line = layout.createLine()
        line.setLineWidth(self.width() - pos.x())
        line.setPosition(pos)
        layout.endLayout()

        painter.setPen(QPen(Qt.gray, 1))
        layout.draw(painter, QPoint(0, 0))


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication([])
    w = PercentLineEdit()
    w.show()
    app.exec_()
