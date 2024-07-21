import sys
from PyQt5.QtWidgets import QApplication
from src.clock import Clock

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Clock()
    sys.exit(app.exec_())
