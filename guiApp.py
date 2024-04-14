from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import sys


# create a main window class
class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # configure the window
        self.setGeometry(200, 200, 1600, 1200)
        self.setWindowTitle("Text Replacer")
        self.setStyleSheet("background-color: #909090;")  # color of the border around the frames

        # create a frame that contains the main layout
        mainWidget = QFrame()
        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)    # remove the gaps between the frames

        leftFrame = FileDropArea()
        leftFrame.setStyleSheet("background-color: #e5e5e5; border: 1px solid black;")   # left frame style

        rightFrame = ReplacementFrame()
        rightFrame.setStyleSheet("background-color: #909090; border: 1px solid black;")  # right frame style

        # make left frame smaller than the right frame
        mainLayout.addWidget(leftFrame, stretch=2)
        mainLayout.addWidget(rightFrame, stretch=3)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)


# create a file drop area class
class FileDropArea(QFrame):
    def __init__(self):
        super().__init__()

        # allow files to be dragged and dropped
        self.setAcceptDrops(True)

        # format the file drop area
        # self.setStyleSheet("border: 2px dashed #aaaaaa;")
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        # add a file icon (emoji)
        self.fileIconLabel = QLabel("📁")
        self.fileIconLabel.setStyleSheet("font-size: 300px; text-align: center; border: none")
        layout.addWidget(self.fileIconLabel)

        # add a label to drag files there
        self.dragFileLabel = QLabel("Drag text file here or...")
        self.dragFileLabel.setStyleSheet("font-size: 40px; font-family: Verdana; text-align: left; border: none;")
        layout.addWidget(self.dragFileLabel)

        # add button to select file
        self.selectFileButton = QPushButton("...click to select file")
        self.selectFileButton.setStyleSheet("background-color: transparent; font-size: 40px; font-family: Verdana;"
                                            "text-align: right; border: none; color: blue;")
        self.selectFileButton.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.selectFileButton)

    # this function handles the drag functionality
    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # this function handles when files are dropped
    def drop_event(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if len(files) == 1:  # Process only the first file if multiple files are dropped
            self.process_file(files[0])

    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select files", "", "All Files (*)", options=options)
        if files:
            self.process_files(files)

    def process_file(self, files):
        # Process the list of files here
        print("Selected files:", files)


# create a class for the frame where the user enters the replacement to make
class ReplacementFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.numRows = 1

        # set to a grid layout
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        # create a maximum number of rows
        self.maxRows = 12

        # create placeholder rows for the rows allowed by the maximum
        for row in range(self.maxRows):
            self.add_placeholder_row(row)

        # create a label "Find"
        self.findLabel = QLabel("Find:")
        self.findLabel.setStyleSheet("font-size: 40px; font-family: Verdana; text-align: left; border: none;")

        # create a label "Replace with"
        self.replaceLabel = QLabel("Replace with:")
        self.replaceLabel.setStyleSheet("font-size: 40px; font-family: Verdana; text-align: right; border: none;")

        self.gridLayout.addWidget(self.findLabel, 0, 0)
        self.gridLayout.addWidget(self.replaceLabel, 0, 1)

        # button to add a row
        self.addRowButton = QPushButton("➕")
        self.addRowButton.setStyleSheet("font-size: 40px; text-align: right; border: none")
        self.addRowButton.clicked.connect(self.add_row)

        # button to delete a row
        self.deleteRowButton = QPushButton("❌")
        self.deleteRowButton.setStyleSheet("font-size: 40px; text-align: left; border: none")
        self.deleteRowButton.clicked.connect(self.delete_row)

        # add the initial first row
        self.add_row()

    # function to add placeholder rows. Used to create a grid that is filled up by default
    def add_placeholder_row(self, row):
        placeholder1 = QWidget()
        placeholder2 = QWidget()

        # make it so there is no border around the placeholder widgets
        placeholder1.setStyleSheet("border: none; height: 70px")
        placeholder2.setStyleSheet("border: none; height: 70px")

        self.gridLayout.addWidget(placeholder1, row, 0)  # Placeholder widget
        self.gridLayout.addWidget(placeholder2, row, 1)  # Placeholder widget

    # function to add a new row of line edits (text boxes)
    def add_row(self):
        if self.numRows < self.maxRows - 1:
            row = self.numRows

            # create the text boxes and default text
            findLineEdit = QLineEdit()
            findLineEdit.setPlaceholderText("Find in text...")

            replaceLineEdit = QLineEdit()
            replaceLineEdit.setPlaceholderText("Replace with...")

            # style the widgets
            findLineEdit.setStyleSheet("background-color: white; font-size: 30px; font-family: Verdana; height: 70px;")
            replaceLineEdit.setStyleSheet("background-color: white; font-size: 30px; font-family: Verdana; "
                                          "height: 70px;")

            # add the widgets
            self.gridLayout.addWidget(findLineEdit, row, 0)
            self.gridLayout.addWidget(replaceLineEdit, row, 1)

            # add the "add row button" and "delete row button"
            self.gridLayout.addWidget(self.addRowButton, row+1, 1)
            self.gridLayout.addWidget(self.deleteRowButton, row + 1, 0)

            self.numRows += 1


    # function to delete a row
    def delete_row(self):
        # make sure user can't delete the first row
        if self.numRows > 2:

            # replace the last row with a placeholder row
            self.add_placeholder_row(self.numRows-1)

            # bookkeeping
            self.numRows = self.numRows - 1

            # fix the positions of the + and x
            self.gridLayout.addWidget(self.addRowButton, self.numRows, 1)
            self.gridLayout.addWidget(self.deleteRowButton, self.numRows, 0)

            print(self.numRows)
