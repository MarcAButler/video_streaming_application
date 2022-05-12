# https://www.youtube.com/watch?v=dTDgbx-XelY

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

        # QLabel() is a widget that provides a text or image display--important for displaying video
        self.FeedLabel = QLabel()

        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)

        self.VBL.addWidget(self.CancelBTN)

        # Create an instance of a worker thread to display the video so that it does not catch the MainWindow class in an infinite loop
        self.Worker1 = Worker1()

        # Starts the Thread
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)

        self.setLayout(self.VBL)

    # Helps handled the emited signal
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    
    def run(self):
        self.ThreadActive = True
        # Uses the webcam
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # Convert the frame into an RGB image
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Flips the image on the vertical axis denoted by the "1"
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                # Sends a message to the main window class to be transmitted--stored in the Pic variable
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())