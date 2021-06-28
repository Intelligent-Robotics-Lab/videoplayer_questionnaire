import sys
from PyQt5.QtWidgets import QApplication, QButtonGroup, QLabel, QLineEdit, QPushButton, QSlider, QVBoxLayout, QWidget,QFileDialog, QGridLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import *

#main window
class media_player:

    #constructor 
    def __init__(self):
        self.media="media_player"

widgets = {
    "fileButton": [],
    "frameButton": [],
    "slider": [],
    "lineEdit":[],
    "replayButton":[],
    "nextButton":[]
}

grid = QGridLayout()
    
def frame1():

    #change slidder value
    def changeInValue():
        size = str(slider.value())
        lineEdit.setText(size)

    #call frame2 from frame 1 
    def callFrame2():
        frame2()

    #widget clearing
    def clear_widgets():
        for widget in widgets:
            if widgets[widget] != []:
                widgets[widget][-1].hide()
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()
              

    # File select function
    def fileExplore():
        videoFile = QFileDialog.getOpenFileName(directory = "c://home")
        Qt.Key_MediaPlay
    
    #button for file
    fileButton = QPushButton("Select a file")
    fileButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    fileButton.setStyleSheet(
        "border: 4px solid;"
        "border-radius: 45px;"
        "padding:15px 0;"
        )
    widgets["fileButton"].append(fileButton)
    fileButton.clicked.connect(fileExplore)

    #button for next frame
    frameButton =QPushButton("continue")
    frameButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    frameButton.setStyleSheet(
        "border: 4px solid;"
        "border-radius: 45px;"
        "padding:15px 0;"
        )
    widgets["frameButton"].append(frameButton)
    frameButton.clicked.connect(clear_widgets)
    frameButton.clicked.connect(callFrame2)
    
    #slider
    slider = QSlider()
    slider.setOrientation(Qt.Horizontal)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setTickInterval(1)
    slider.setMinimum(1)
    slider.setMaximum(60)
    slider.setMaximumWidth(600)
    slider.valueChanged.connect(changeInValue)
    widgets["slider"].append(slider)

    #lineEdit
    lineEdit =QLineEdit()
    lineEdit.setMaximumWidth(350)
    widgets["lineEdit"].append(lineEdit)

    
    #adding all frame1 widgets
    grid.addWidget(widgets["fileButton"][-1], 0, 0, 1, 1)
    grid.addWidget(widgets["frameButton"][-1], 0, 1, 1, 1)
    grid.addWidget(widgets["slider"][-1], 1, 0)
    grid.addWidget(widgets["lineEdit"][-1], 1, 1)

def frame2():
    
    #button for replay
    replayButton = QPushButton("replay video")
    replayButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    replayButton.setStyleSheet(
        "border: 4px solid;"
        "border-radius: 45px;"
        "padding:15px 0;"
        )
    widgets["replayButton"].append(replayButton)

    #button for next segment
    nextButton = QPushButton("next video")
    nextButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    nextButton.setStyleSheet(
        "border: 4px solid;"
        "border-radius: 45px;"
        "padding:15px 0;"
        )
    widgets["nextButton"].append(nextButton)
    
    #add all frame2 widgets
    grid.addWidget(widgets["replayButton"][-1], 1, 0, 1, 1)    
    grid.addWidget(widgets["nextButton"][-1], 1, 1, 1, 1)
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Media Player")
    window.setFixedWidth(1000)
    window.move(200, 200)
    window.setLayout(grid) 
    frame1()
    window.show()
    sys.exit(app.exec_())
