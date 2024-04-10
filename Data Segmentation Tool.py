import csv
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QCheckBox, QFileDialog
from PyQt5 import QtGui, QtCore

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 800)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Data Segmentation Tool")
        self.centralwidget = QWidget()
        
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)

        # Header 
        self.Header = QLabel(self.centralwidget)
        self.Header.setGeometry(QtCore.QRect(40, 25, 520, 70))
        self.Header.setText("Detecting the Onset of Cybersickness \n" " using Physiological Data")
        self.Header.setFont(font)
        self.Header.setAlignment(QtCore.Qt.AlignCenter)
        
        # uploadButton
        self.uploadButton = QPushButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(90, 190, 120, 30))
        self.uploadButton.setText("Upload")
        font.setPointSize(10)
        self.uploadButton.setFont(font)
        self.uploadButton.clicked.connect(self.importCSV)

        # filePreview
        self.filePreview = QTextEdit(self.centralwidget)
        self.filePreview.setGeometry(QtCore.QRect(290, 160, 250, 60))
        self.filePreview.setReadOnly(True)

        # segmentLabel   
        self.segmentLabel = QLabel(self.centralwidget)
        self.segmentLabel.setGeometry(QtCore.QRect(100, 260, 100, 31))
        self.segmentLabel.setText("Segment:")
        font.setPointSize(14)
        self.segmentLabel.setFont(font)
        self.segmentLabel.setAlignment(QtCore.Qt.AlignCenter)

        # UploadLabel
        self.uploadLabel = QLabel(self.centralwidget)
        self.uploadLabel.setGeometry(QtCore.QRect(90, 150, 121, 31))
        self.uploadLabel.setText("File Upload:")
        self.uploadLabel.setFont(font)
        self.uploadLabel.setAlignment(QtCore.Qt.AlignCenter)

        # TimeRangeLabel
        self.timeRangeLabel = QLabel(self.centralwidget)
        self.timeRangeLabel.setGeometry(QtCore.QRect(300, 260, 131, 31))
        self.timeRangeLabel.setText("Time Range:")
        self.timeRangeLabel.setFont(font)
        self.timeRangeLabel.setAlignment(QtCore.Qt.AlignCenter)

        # TimeRangeInput
        self.timeRangeInput = QTextEdit(self.centralwidget)
        self.timeRangeInput.setGeometry(QtCore.QRect(305, 300, 121, 31))
        self.timeRangeInput.setObjectName("timeRangeInput")

        # submitButton
        self.submitButton = QPushButton(self.centralwidget)
        self.submitButton.setGeometry(QtCore.QRect(305, 540, 120, 30))
        self.submitButton.setText("Submit")
        font.setPointSize(10)
        self.submitButton.setFont(font)

        # downloadButton
        self.DownloadButton = QPushButton(self.centralwidget)
        self.DownloadButton.setGeometry(QtCore.QRect(305, 580, 120, 30))
        self.DownloadButton.setText("Download")
        self.DownloadButton.setFont(font)

        # verticalLayout
        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(110, 300, 81, 83))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)        

        self.segment1 = QCheckBox(self.widget)
        self.segment1.setText("   1")
        self.segment1.setFont(font)
        self.verticalLayout.addWidget(self.segment1)

        self.segment2 = QCheckBox(self.widget)
        self.segment2.setText("   2")
        self.segment2.setFont(font)
        self.verticalLayout.addWidget(self.segment2)

        self.segment3 = QCheckBox(self.widget)
        self.segment3.setText("   3")
        self.segment3.setFont(font)
        self.verticalLayout.addWidget(self.segment3)

        self.setCentralWidget(self.centralwidget) 

    def importCSV(self):
        file, _ = QFileDialog.getOpenFileName(self,"Open CSV File", "","CSV Files (*.csv)")
        if file:
            with open(file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                # Skip first row (of headings) 
                next(reader)

                data = []
                for row in reader:
                    data.append(row)

                self.filePreview.setText("Loaded: " + file.split("/")[-1] + "\nTotal Entries: " + str(len(data)) + ".")

    def exportCSV(self):
        pass
    
app = QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec_())