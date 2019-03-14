from increment.main_window import MainWindow
from increment import get_resource
from PySide2.QtGui import QIcon


def main(args=None):
    import sys
    from PySide2.QtWidgets import QApplication

    if args is None:
        args = sys.argv
    app = QApplication(args)
    w = MainWindow()
    w.setWindowTitle('Increment2')
    icon = QIcon(get_resource('favicon.ico'))
    w.setWindowIcon(icon)
    w.show()
    app.exec_()


if __name__ == '__main__':
    main()
