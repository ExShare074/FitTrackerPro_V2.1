from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Test PyQt5")
window.show()
sys.exit(app.exec_())