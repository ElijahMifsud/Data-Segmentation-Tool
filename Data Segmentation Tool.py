import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("Data Segmentation Tool")
        self.mainWidget = QWidget()
        self.checkboxList = []
        self.dataFrame_List = []

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)

        # Header 
        self.Header = QLabel(self.mainWidget)
        self.Header.setGeometry(QtCore.QRect(50, 0, 500, 51))
        self.Header.setText("Data Segmentation Tool")
        self.Header.setFont(font)
        self.Header.setAlignment(QtCore.Qt.AlignCenter)

        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)

        # Header 2
        self.Header2 = QLabel(self.mainWidget)
        self.Header2.setGeometry(QtCore.QRect(40, 25, 520, 70))
        self.Header2.setText("Detecting the Onset of Motion Sickness in VR using Physiological Data.")
        self.Header2.setFont(font)
        self.Header2.setAlignment(QtCore.Qt.AlignCenter)

        font.setBold(True)
        font.setPointSize(10)        

        # uploadButton
        self.uploadButton = QPushButton(self.mainWidget)
        self.uploadButton.setGeometry(QtCore.QRect(90, 130, 120, 30))
        self.uploadButton.setText("Upload")
        self.uploadButton.setFont(font)
        self.uploadButton.clicked.connect(self.importCSV)

        # filePathPreview
        self.filePathPreview = QTextEdit(self.mainWidget)
        self.filePathPreview.setGeometry(QtCore.QRect(290, 135, 250, 60))
        self.filePathPreview.setReadOnly(True)

        font.setPointSize(14)

        # UploadLabel
        self.uploadLabel = QLabel(self.mainWidget)
        self.uploadLabel.setGeometry(QtCore.QRect(75, 100, 150, 30))
        self.uploadLabel.setText("(1) File Upload:")
        self.uploadLabel.setFont(font)
        self.uploadLabel.setAlignment(QtCore.Qt.AlignCenter)

        # PathPreviewLabel
        self.pathPreviewLabel = QLabel(self.mainWidget)
        self.pathPreviewLabel.setGeometry(QtCore.QRect(290, 100, 140, 30))
        self.pathPreviewLabel.setText("Path Preview:")
        self.pathPreviewLabel.setFont(font)
        self.pathPreviewLabel.setAlignment(QtCore.Qt.AlignCenter)

        # SegmentLabel   
        self.segmentLabel = QLabel(self.mainWidget)
        self.segmentLabel.setGeometry(QtCore.QRect(50, 220, 210, 30))
        self.segmentLabel.setText("(2) Select Segment/s:")
        self.segmentLabel.setFont(font)
        self.segmentLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        # Line
        self.line = QFrame(self.mainWidget)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setGeometry(QtCore.QRect(60, 240, 200, 31))

        # TimeRangeLabel
        self.timeRangeLabel = QLabel(self.mainWidget)
        self.timeRangeLabel.setGeometry(QtCore.QRect(290, 220, 161, 31))
        self.timeRangeLabel.setText("(3) Time Range:")
        self.timeRangeLabel.setFont(font)
        self.timeRangeLabel.setAlignment(QtCore.Qt.AlignCenter)

        # submit/downloadLabel
        self.submitDownloadLabel = QLabel(self.mainWidget)
        self.submitDownloadLabel.setGeometry(QtCore.QRect(290, 510, 250, 31))
        self.submitDownloadLabel.setText("(4) Submit & Download:")
        self.submitDownloadLabel.setFont(font)
        self.submitDownloadLabel.setAlignment(QtCore.Qt.AlignCenter)

        font.setPointSize(10)
        font.setBold(False)

        # TimeRangeText
        self.timeRangeText = QLabel(self.mainWidget)
        self.timeRangeText.setFont(font)
        self.timeRangeText.setWordWrap(True)
        self.timeRangeText.setText("Input a time range (in seconds) separated by a comma to designate partition." +
                                    "\nFor Example: \n" + 
                                    "\n• Input \'0,0\' to extract the, unchanged, selected partitions. \n" + 
                                    "\n• Input \'5,-5\' to remove 5 seconds from the start and end of the selected partitions.\n" + 
                                    "\n• Input \'-10,10\' to capture 10 seconds above and below the selected segments.\n")
        self.timeRangeText.setGeometry(QtCore.QRect(295, 200, 250, 400))

        # TimeRangeInput
        self.timeRangeInput = QTextEdit(self.mainWidget)
        self.timeRangeInput.setGeometry(QtCore.QRect(295, 255, 121, 31))
        self.timeRangeInput.setObjectName("timeRangeInput")
        self.timeRangeInput.setAlignment(QtCore.Qt.AlignCenter)
        
        font.setBold(True)

        # submitButton
        self.submitButton = QPushButton(self.mainWidget)
        self.submitButton.setGeometry(QtCore.QRect(295, 550, 120, 30))
        self.submitButton.setText("Submit")
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.submitButtonClicked)
            
        # downloadButton
        self.DownloadButton = QPushButton(self.mainWidget)
        self.DownloadButton.setGeometry(QtCore.QRect(420, 550, 120, 30))
        self.DownloadButton.setText("Download")
        self.DownloadButton.setFont(font)
        self.DownloadButton.clicked.connect(self.exportCSV)

        # verticalLayout
        self.widget = QWidget(self.mainWidget)
        self.widget.setGeometry(QtCore.QRect(110, 200, 80, 100))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.mainWidget) 

    def importCSV(self):
        # Picks the file to be imported
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"CSV files (*.csv)")
        if fname[0]:
            self.df = pd.read_csv(fname[0])
            self.filePathPreview.setText(fname[0])
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

            # Get segment information
            segment_df = self.df[self.df['Segment'] == segment]
            min_time = segment_df['Timestamp'].min()
            max_time = segment_df['Timestamp'].max()

            # Check if time_range contains exactly two elements    
            if len(time_range) != 2:
                self.buttonConfirmation("Invalid Input. Please input two integers. Format: -x,x")
                return

            # Check if both elements in time_range are integers
            try:
                time_range = [int(i) for i in time_range]
            except ValueError:
                self.buttonConfirmation("Invalid Input. Please input two integers. Format: -x,x ")
                return     

            # Calculate the target time
            start_time = min_time + pd.Timedelta(seconds=time_range[0])
            end_time = max_time + pd.Timedelta(seconds=time_range[1])

            # Create new dataframe and add to list of complete segmentations 
            self.dataFrame_List.append(self.df[(self.df['Timestamp'] >= start_time) & (self.df['Timestamp'] <= end_time)])

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
                self.widget.setGeometry(QtCore.QRect(100, 270, 81, 300))
            elif segments.size <= 4:
                self.widget.setGeometry(QtCore.QRect(100, 270, 81, 100))
            self.verticalLayout.addWidget(checkbox)
            self.checkboxList.append(checkbox)
            
        self.setCentralWidget(self.mainWidget)
        
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