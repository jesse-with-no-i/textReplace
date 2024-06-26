from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from replacer import Replacer
import sys


# have a singleton class that has the attributes files and a list of replacers
# when the go button is pressed, signal the singleton to get all the data from each of the classes
# then call the execute function with files and replacers as the arguments
class WindowData:
    _instance = None

    def __init__(self):
        # Private constructor to prevent instantiation from outside
        if WindowData._instance is not None:
            raise Exception("This class is a singleton. Use WindowData.getInstance() to get an instance.")
        else:
            # Initialize attributes
            self.files = []
            self.replacers = []

    @staticmethod
    def getInstance():
        if WindowData._instance is None:
            WindowData._instance = WindowData()
        return WindowData._instance

    def get_files(self):
        return self.files

    def get_replacers(self):
        return self.replacers

    def set_files(self, files):
        self.files = files

    def add_replacer(self, replacer):
        self.replacers.append(replacer)


# create a main window class
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # list containing all the files the user wants to edit
        self.files = []

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
        self.files = []

        # label for what files have been selected
        self.fileLabel = QLabel("No Files Selected.")
        self.fileLabel.setStyleSheet("border: none; font-family: Verdana;")

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
        self.dragFileLabel = QLabel("Drag text files here or...")
        self.dragFileLabel.setStyleSheet("font-size: 40px; font-family: Verdana; text-align: left; border: none;")
        layout.addWidget(self.dragFileLabel)

        # add button to select file
        self.selectFileButton = QPushButton("...click to browse files")
        self.selectFileButton.setStyleSheet("background-color: transparent; font-size: 40px; font-family: Verdana;"
                                            "text-align: right; border: none; color: blue;")
        self.selectFileButton.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.selectFileButton)

        # add the label for selected files
        layout.addWidget(self.fileLabel)

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

    def process_files(self, files):
        # flag for all the files being the right type
        incorrectFormat = False

        # make sure each file is a text file
        for file in files:

            # if the file is not a text file, reject it and show a messagebox
            if file[-4:] != ".txt":
                # change flag to show that some files were rejected because they were the wrong type
                incorrectFormat = True

                # remove the non-text file from files
                files.remove(file)

        if incorrectFormat:
            message_box = QMessageBox()
            message_box.setWindowTitle("Wrong file type")
            message_box.setText("Some of your files are not formatted with '.txt' and will not be included")
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()

        # display the selected files on the screen
        fileNames = "Files selected:\n"

        for file in files:
            # add the file to the filenames string
            fileName = file.split('/')[-1]

            # if the filename is too long, only display part of it:
            if len(fileName) > 35:
                fileName = fileName[0:33] + " ..."

            fileNames = fileNames + fileName + '\n'

        # update the label that shows the selected files
        self.fileLabel.setText(fileNames)

        # add the files to the window data instance to be used later on
        WindowData.getInstance().set_files(files)


# create a class for the frame where the user enters the replacement to make
class ReplacementFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.numRows = 1

        # list of all find-replace line edit objects
        self.findLineEditObjects = []

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

        # create a label "Replace "
        self.replaceLabel = QLabel("Replace:")
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

        # button at the bottom that performs the replacements based on the text and files the user entered
        self.goButton = QPushButton("Go")
        self.goButton.clicked.connect(self.press_go)
        # format the button
        self.goButton.setStyleSheet("   background-color: #A4C639; font-family: Verdana; font-size: 40px;")
        self.gridLayout.addWidget(self.goButton, self.maxRows, 1)

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

            # add a new list to the findLineEditObjects list that contains both the findLineEdit
            # and replaceLineEdit objects
            findReplacePair = [findLineEdit, replaceLineEdit]
            self.findLineEditObjects.append(findReplacePair)

            # add the widgets
            self.gridLayout.addWidget(findLineEdit, row, 0)
            self.gridLayout.addWidget(replaceLineEdit, row, 1)

            # add the "add row button" and "delete row button"
            self.place_add_delete_buttons(row+1)

            self.numRows += 1

    # function to delete a row
    def delete_row(self):
        # make sure user can't delete the first row
        if self.numRows <= 2:
            return

        # replace the last row with a placeholder row
        self.add_placeholder_row(self.numRows)
        self.add_placeholder_row(self.numRows-1)

        # bookkeeping
        self.numRows -= 1

        # replace add and delete buttons
        self.place_add_delete_buttons(self.numRows)

        # delete the pair from the findLineEditObjects list
        self.findLineEditObjects.pop()

# function to place or replace the add and delete buttons
    def place_add_delete_buttons(self, row):
        # button to add a row
        self.addRowButton = QPushButton("➕")
        self.addRowButton.setStyleSheet("font-size: 40px; text-align: right; border: none")
        self.addRowButton.clicked.connect(self.add_row)

        # button to delete a row
        self.deleteRowButton = QPushButton("❌")
        self.deleteRowButton.setStyleSheet("font-size: 40px; text-align: left; border: none")
        self.deleteRowButton.clicked.connect(self.delete_row)

        # fix the positions of the + and x
        self.gridLayout.addWidget(self.addRowButton, row, 1)
        self.gridLayout.addWidget(self.deleteRowButton, row, 0)


    # function for when the "go" button is pressed:
    def press_go(self):
        # get an instance of the singleton class to store the data in
        windowInstance = WindowData.getInstance()

        # get the contents of all the replacement by extracting the text from the line edits
        replacementsList = []

        for pair in self.findLineEditObjects:
            findText = pair[0].text()
            replaceText = pair[1].text()

            # either one is blank, don't add it to the list
            if findText == "" or replaceText == "":
                continue

            replacementsList.append([findText, replaceText])

        # check if the user has selected any files yet
        if windowInstance.get_files() == []:
            return

        # since there are multiple files, we need to do this operation for every file in files
        for file in windowInstance.get_files():

            # create a new replacer object with the current file and a new file which extends the current file
            newFileName = file.split("\\")[-1][:-4] + "_replaced.txt"
            replacer = Replacer(file, newFileName)

            # add each replacement to the new replacer
            for replacement in replacementsList:
                replacer.add_replacement(replacement[0], replacement[1])

            replacer.replace_text()

        # notify the user that the process is complete and exit the app.
        message_box = QMessageBox()
        message_box.setWindowTitle("Process Complete")
        message_box.setText("The process is complete and the app will now close.")
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)

        # make it so that the message box closes the application when you press ok
        ok_button = message_box.button(QMessageBox.Ok)
        ok_button.clicked.connect(self.close_application)

        message_box.exec_()

    def close_application(self):
        # Close the application
        QApplication.instance().quit()
