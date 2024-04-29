import csv
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QCheckBox, QMessageBox
from PyQt5 import QtGui, QtCore

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 800)
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("Data Segmentation Tool")
        self.centralwidget = QWidget()
        self.checkboxList = []



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
        ##self.uploadButton.clicked.connect(self.create_checkboxes(font)) 


        # fileName
        self.fileName = QTextEdit(self.centralwidget)
        self.fileName.setGeometry(QtCore.QRect(290, 190, 250, 30))

        # SegmantLabel   
        self.segmantLabel = QLabel(self.centralwidget)
        self.segmantLabel.setGeometry(QtCore.QRect(100, 260, 100, 31))
        self.segmantLabel.setText("Segmant:")
        font.setPointSize(14)
        self.segmantLabel.setFont(font)
        self.segmantLabel.setAlignment(QtCore.Qt.AlignCenter)

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
        self.submitButton.clicked.connect(self.submitButtonClicked)
            

        # downloadButton
        self.DownloadButton = QPushButton(self.centralwidget)
        self.DownloadButton.setGeometry(QtCore.QRect(305, 580, 120, 30))
        self.DownloadButton.setText("Download")
        self.DownloadButton.setFont(font)
        self.DownloadButton.clicked.connect(self.exportCSV)

        # verticalLayout
        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(110, 300, 81, 83))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)        


        # self.segmant1 = QCheckBox(self.widget)
        # self.segmant1.setText("   1")
        # self.segmant1.setFont(font)
        # self.verticalLayout.addWidget(self.segmant1)

        # self.segmant2 = QCheckBox(self.widget)
        # self.segmant2.setText("   2")
        # self.segmant2.setFont(font)
        # self.verticalLayout.addWidget(self.segmant2)

        # self.segmant3 = QCheckBox(self.widget)
        # self.segmant3.setText("   3")
        # self.segmant3.setFont(font)
        # self.verticalLayout.addWidget(self.segmant3)

        self.setCentralWidget(self.centralwidget) 


    def importCSV(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"CSV files (*.csv)")
        if fname[0]:
            self.df = pd.read_csv(fname[0])
            self.fileName.setText(fname[0])
            self.create_checkboxes()

    def submitButtonClicked(self):

        for box in self.checkboxList:
            if box.isChecked():
                segment = int(box.text())

        time_range = self.timeRangeInput.toPlainText().split(',')

        # Converts Timestamp to a datetime so we can use within dataframes
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

        segment_df = self.df[self.df['Segment'] == segment]
        min_time = segment_df['Timestamp'].min()

        #Validate user input
        smallest_time = self.df['Timestamp'].min()
        maximum_time = self.df['Timestamp'].max()

        # Check if time_range contains exactly two elements    
        if len(time_range) != 2:
            self.buttonConfirmation("Invalid Input two integers are needed. Format: -x,x")
            return

        # Check if both elements in time_range are integers
        try:
            time_range = [int(i) for i in time_range]
        except ValueError:
            self.buttonConfirmation("Invalid Input two integers are needed. Format: -x,x ")
            return     

        if min_time + pd.Timedelta(seconds=time_range[0]) < smallest_time or min_time + pd.Timedelta(seconds=time_range[1]) > maximum_time:
            self.buttonConfirmation("Invalid min or max time. Format: -x,x")
        else:
            start_time = min_time + pd.Timedelta(seconds=time_range[0])
            end_time = min_time + pd.Timedelta(seconds=time_range[1])

            self.new_df = self.df[(self.df['Timestamp'] >= start_time) & 
                                (self.df['Timestamp'] <= end_time)]

            self.buttonConfirmation("Submition Successful, Click the Download Button to Save the CSV")

    def exportCSV(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', 
            'c:\\',"CSV files (*.csv)")
        if fname[0]:
            self.new_df.to_csv(fname[0], index=False)
    
    def buttonConfirmation(self, string):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Confirmation")
        msgbox.setText(string)
        msgbox.exec()

    def create_checkboxes(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(30) 

        # Get the unique segments from the 'Segment' column
        segments = self.df['Segment'].unique()

        
        # Create a checkbox for each segment
        for i, segment in enumerate(segments, start=1):
            checkbox = QCheckBox(self.widget)
            checkbox.setText(f"   {segment}")  # Use the segment value as the checkbox text
            checkbox.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px;}")
            checkbox.setFont(font)

            self.widget.setGeometry(QtCore.QRect(100, 300,81, 300))
            self.verticalLayout.addWidget(checkbox)
            self.checkboxList.append(checkbox)
            
        self.setCentralWidget(self.centralwidget)
        

app = QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec_())