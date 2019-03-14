from __future__ import annotations

from typing import Callable, Tuple, Optional

from increment.inc_state import calc_after, calc_before, calc_change
from increment.percent_lineedit import PercentLineEdit
import increment.__data__ as __data__

from PySide2.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout, QRadioButton, QPushButton, QMessageBox, \
    QApplication
from PySide2.QtCore import Qt, QSettings


class MainWindow(QWidget):
    def make_calc_radio_button(self, *args, calc_function, calc_target, **kwargs):
        ret = QRadioButton(*args, **kwargs)
        ret.setFocusPolicy(Qt.ClickFocus)

        @ret.toggled.connect
        def on_toggle(b):
            if b:
                self.calc_function = calc_function
                self.calc_target = calc_target
                self.target_changed()

        return ret

    def make_edit(self, *args, placeholder, font_size, **kwargs):
        ret = QLineEdit(*args, **kwargs)
        ret.setPlaceholderText(placeholder)

        @ret.textEdited.connect
        def on_change(e):
            self.recalculate()

        if font_size:
            font = ret.font()
            font.setPointSize(font_size)
            ret.setFont(font)

        return ret

    def make_change_edit(self, *args, placeholder, font_size, **kwargs):
        ret = PercentLineEdit(*args, **kwargs)
        ret.setPlaceholderText(placeholder)

        @ret.textEdited.connect
        def on_change(e):
            self.recalculate()

        if font_size:
            font = ret.font()
            font.setPointSize(font_size)
            ret.setFont(font)

        return ret

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.before_edit: QLineEdit = None
        self.after_edit: QLineEdit = None
        self.change_edit: QLineEdit = None

        self.calc_function: Callable[[str, str, str], Tuple[str, Optional[str]]] = None
        self.calc_target: QLineEdit = None

        self.settings: QSettings = None

        self.non_percent_flag = False

        self.init_ui()

    def init_ui(self):
        self.settings = QSettings(__data__.__author__, __data__.__name__)
        font_size = self.settings.value('line_edit_font_size', 0)

        main_layout = QGridLayout()

        main_layout.addWidget(QLabel("before:"), 0, 0)
        main_layout.addWidget(QLabel("after:"), 2, 0)
        main_layout.addWidget(QLabel("change:"), 4, 0)

        self.before_edit = self.make_edit(placeholder='before', font_size=font_size)
        self.after_edit = self.make_edit(placeholder='after', font_size=font_size)
        self.change_edit = self.make_change_edit(placeholder='change', font_size=font_size)

        calc_before_radio = self.make_calc_radio_button(calc_function=calc_before,
                                                        calc_target=self.before_edit)
        calc_after_radio = self.make_calc_radio_button(calc_function=calc_after,
                                                       calc_target=self.after_edit)
        calc_change_radio = self.make_calc_radio_button(calc_function=calc_change,
                                                        calc_target=self.change_edit)

        main_layout.addWidget(self.before_edit, 1, 0)
        main_layout.addWidget(calc_before_radio, 1, 1)

        main_layout.addWidget(self.after_edit, 3, 0)
        main_layout.addWidget(calc_after_radio, 3, 1)

        main_layout.addWidget(self.change_edit, 5, 0)
        main_layout.addWidget(calc_change_radio, 5, 1)

        self.setLayout(main_layout)

        about_btn = QPushButton('about...')
        about_btn.setFocusPolicy(Qt.ClickFocus)

        @about_btn.clicked.connect
        def show_help(event):
            message = '\n'.join([
                __data__.__name__ + ' v' + __data__.__version__,
                f'by ' + __data__.__author__
            ])
            QMessageBox.information(self, 'about increment', message)

        main_layout.addWidget(about_btn, 0, 1)

        calc_change_radio.setChecked(True)

    def target_changed(self):
        for edit in (self.before_edit,
                     self.after_edit,
                     self.change_edit):
            edit.setReadOnly(edit is self.calc_target)
            edit.setStyleSheet('')
            edit.setClearButtonEnabled(edit is not self.calc_target)
            if edit is not self.calc_target:
                if edit.text().startswith('!err'):
                    edit.clear()
                edit.setFocusPolicy(Qt.FocusPolicy(Qt.ClickFocus | Qt.TabFocus))
            else:
                edit.setFocusPolicy(Qt.ClickFocus)

        self.recalculate()

    def recalculate(self):
        b = self.before_edit.text()
        a = self.after_edit.text()
        c = self.change_edit.text()+'%'

        try:
            result, stylesheet = self.calc_function(b, a, c)
        except (ValueError, ZeroDivisionError) as e:
            result = '!err' + str(e)
            stylesheet = 'color: grey;'

        self.calc_target.setText(result)
        if stylesheet is True:
            stylesheet = 'color: grey;'
        if stylesheet is not None:
            self.calc_target.setStyleSheet(stylesheet)

    def closeEvent(self, event):
        if self.settings:
            self.settings.setValue('line_edit_font_size', self.before_edit.font().pointSize())
        super().closeEvent(event)

    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            point_delta = event.angleDelta().y() // 120
            for edit in (self.before_edit,
                         self.after_edit, self.change_edit):
                font = edit.font()
                size = font.pointSize() + point_delta
                if size > 0:
                    font.setPointSize(size)
                    edit.setFont(font)
        else:
            super().wheelEvent(event)
