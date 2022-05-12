import sys

from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore    import *

# Create an instance of QApplication
myApp = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 App')

# Create an instance of the applications GUI
# window = QWidget()
# window.setWindowTitle('PyQt5 App')
# window.setGeometry(100, 100, 280, 280)
# window.move(60, 15)
# # [-] QLabel can accept HTML TAGS!
# helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
# helloMsg.move(60, 15)

layout = QGridLayout()
layout.addWidget(QLineEdit('HELLO!'), 0, 1)
layout.addWidget(QPushButton('Center'), 1, 1)
layout.addWidget(QPushButton('Right-Most'), 1, 2)

window.setLayout(layout)


# Show Application GUI
window.show()

# Run the application's event loop (or main loop)
sys.exit(myApp.exec_())