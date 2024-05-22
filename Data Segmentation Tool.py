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
        self.dataFrame_List = []

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

        self.setCentralWidget(self.centralwidget) 

    def importCSV(self):
        # Picks the file to be imported
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"CSV files (*.csv)")
        if fname[0]:
            self.df = pd.read_csv(fname[0])
            self.filePreview.setText(fname[0])
            self.create_checkboxes()

    def submitButtonClicked(self):
        self.segment_List = []
        # Checks which checkboxes are checked and adds them to a list
        for box in self.checkboxList:
            if box.isChecked():
                segment = int(box.text())
                self.segment_List.append(segment)

        # Loops over list of checked checkboxes to segment
        for segment in self.segment_List:
            time_range = self.timeRangeInput.toPlainText().split(',')

            # Converts Timestamp to a datetime so we can use within dataframes
            self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

            segment_df = self.df[self.df['Segment'] == segment]
            min_time = segment_df['Timestamp'].min()

            # Validate user input
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
                self.buttonConfirmation("Invalid Input Two Integers are needed. Format: -x,x ")
                return     

            if min_time + pd.Timedelta(seconds=time_range[0]) < smallest_time or min_time + pd.Timedelta(seconds=time_range[1]) > maximum_time:
                self.buttonConfirmation("Invalid Min or Max time. Format: -x,x")
                return
            
            else:
                # Converts the time_range user input
                start_time = min_time + pd.Timedelta(seconds=time_range[0])
                end_time = min_time + pd.Timedelta(seconds=time_range[1])

                # Makes a new dataframe from the start and end times selected and adds to a dataframe list
                new_df = self.df[(self.df['Timestamp'] >= start_time) & 
                                    (self.df['Timestamp'] <= end_time)]
                
                self.dataFrame_List.append(new_df)

        self.buttonConfirmation("Submission Successful, Click the Download Button to Save the CSV File/s")

    def exportCSV(self):
        # Saves csv files to a selected location
        for dataframe in self.dataFrame_List:
            fname = QFileDialog.getSaveFileName(self, 'Save file', 
                'c:\\',"CSV files (*.csv)")
            if fname[0]:
                dataframe.to_csv(fname[0], index=False)
    
    def buttonConfirmation(self, string):
        # Creates a button confirmation
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Confirmation")
        msgbox.setText(string)
        msgbox.exec()

    def create_checkboxes(self):
        self.clear_checkboxes()

        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(20) 

        # Get the unique segments from the 'Segment' column
        segments = self.df['Segment'].unique()
        
        # Create a checkbox for each segment
        for i, segment in enumerate(segments, start=1):
            # Create check boxes
            checkbox = QCheckBox(self.widget)
            # Use the segment value as the checkbox text
            checkbox.setText(f"   {segment}")  
            checkbox.setFont(font)
            # Adds correct spacing to larger number of segments
            if segments.size > 4:
                self.widget.setGeometry(QtCore.QRect(100, 300,81, 300))
            elif  segments.size <= 4:
                self.widget.setGeometry(QtCore.QRect(100, 300,81, 100))
            self.verticalLayout.addWidget(checkbox)
            self.checkboxList.append(checkbox)
            
        self.setCentralWidget(self.centralwidget)
        
    def clear_checkboxes(self):
        # Clear the list of checkboxes
        for checkbox in self.checkboxList:
            self.verticalLayout.removeWidget(checkbox)
            checkbox.deleteLater()  
        self.checkboxList.clear()  

        
app = QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec_())