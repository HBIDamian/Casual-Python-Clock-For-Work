import sys
from PyQt5.QtWidgets import QApplication
from src.stopwatch import Stopwatch

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    sys.exit(app.exec_())
