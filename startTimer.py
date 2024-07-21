import sys
from PyQt5.QtWidgets import QApplication
from src.timer import Timer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = Timer()
    sys.exit(app.exec_())
