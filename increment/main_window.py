from __future__ import annotations

from typing import Callable, Tuple, Optional

from increment.inc_state import calc_after, calc_before, calc_change
import increment.__data__ as __data__

from PySide2.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout, QRadioButton, QPushButton, QMessageBox
from PySide2.QtCore import Qt


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

    def make_edit(self, *args, placeholder, **kwargs):
        ret = QLineEdit(*args, **kwargs)
        ret.setPlaceholderText(placeholder)

        @ret.textChanged.connect
        def on_change(e):
            self.recalculate()

        return ret

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.before_edit: QLineEdit = None
        self.after_edit: QLineEdit = None
        self.change_edit: QLineEdit = None

        self.calc_function: Callable[[str, str, str], Tuple[str, Optional[str]]] = None
        self.calc_target: QLineEdit = None

        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout()

        main_layout.addWidget(QLabel("before:"), 0, 0)
        main_layout.addWidget(QLabel("after:"), 2, 0)
        main_layout.addWidget(QLabel("change:"), 4, 0)

        self.before_edit = self.make_edit(placeholder='before')
        self.after_edit = self.make_edit(placeholder='after')
        self.change_edit = self.make_edit(placeholder='change')

        calc_before_radio = self.make_calc_radio_button('calculate', calc_function=calc_before,
                                                        calc_target=self.before_edit)
        calc_after_radio = self.make_calc_radio_button('calculate', calc_function=calc_after,
                                                       calc_target=self.after_edit)
        calc_change_radio = self.make_calc_radio_button('calculate', calc_function=calc_change,
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
        self.recalculate()

    def recalculate(self):
        b = self.before_edit.text()
        a = self.after_edit.text()
        c = self.change_edit.text()

        try:
            result, stylesheet = self.calc_function(b, a, c)
        except (ValueError, ZeroDivisionError) as e:
            result = str(e)
            stylesheet = 'color: grey;'

        self.calc_target.setText(result)
        if stylesheet is True:
            stylesheet = 'color: grey;'
        if stylesheet is not None:
            self.calc_target.setStyleSheet(stylesheet)
