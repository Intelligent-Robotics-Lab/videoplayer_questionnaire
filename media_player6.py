
import sys
from typing import Sized
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QApplication, QButtonGroup, QInputDialog, QLabel, QLayout, QDesktopWidget, QTableView 
from PyQt5.QtWidgets import QLineEdit, QPushButton, QSlider, QVBoxLayout, QWidget,QFileDialog, QGridLayout, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QKeyEvent
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer , QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import os


#main window
class media_player(QWidget): 
    def __init__(self):
        super().__init__()
        
        #window size and name
        self.setWindowTitle("Media Player")
        self.resize(600,270)

        #flag for updater
        self.flagUpdate = False

        #creating widgts 
        self.slider = QSlider()
        self.txtBox = QLineEdit()
        self.sliderEdit = QLineEdit()
        self.fileSelect = QPushButton()
        self.nextPage = QPushButton()
        self.cModes = QComboBox()
        self.cLabels = QComboBox()
        self.hotKey = QPushButton("HotKey Setup")
        self.addBtn = QPushButton("Add")
        self.delBtn = QPushButton("Del")
        self.sliderLabel = QLabel()
 
        #Setting up file dialog 
        self.videoFile = QFileDialog()

        #creating variables for global use 
        self.data = ""
        self.sliderSize = ""
        self.comboList = []


        #creating window inst for hotkey  
        self.valueHK = hotKeyBinding()

        #makes sure we have default HK values
        self.defaultHK1 = self.valueHK.HKpass1
        self.defaultHK2 = self.valueHK.HKpass2 
        self.defaultHK3 = self.valueHK.HKpass3 
        self.defaultHK4 = self.valueHK.HKpass4 

        #update combo textbox on open
        self.ComboTextRead()
 
        #calling next frame
        self.frame1()
       
    def frame1(self):
        #grid layout
        grid = QVBoxLayout()
        outer_layout = QHBoxLayout()
        top_layout = QHBoxLayout()
        modes_hotkeys =QHBoxLayout()
        labels_layout = QHBoxLayout()
        self.setLayout(grid)

        #setting modes combo boxe up
        self.cModes.addItem("Modes")
        self.cModes.addItem("Duration")
        self.cModes.addItem("Frequency")
        self.cModes.addItem("Partial Time interval")
  
        #setup slider
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setRange(5,30)
        self.slider.setSingleStep(1)
        self.slider.setValue(5)
        self.sliderEdit.setText(str(5))
        self.sliderLabel.setText("Interval: ")

        #setup txtbox/nextPage
        self.txtBox.setText("Select A file")
        self.fileSelect.setText("...")
        self.nextPage.setText("Continue")

        #setting up cursor hover
        self.fileSelect.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.nextPage.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.cModes.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.cLabels.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.addBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.delBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.hotKey.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
       
        #adding widgets to layouts for grid
        outer_layout.addWidget(self.txtBox)
        outer_layout.addWidget(self.fileSelect)
        labels_layout.addWidget(self.cLabels)
        labels_layout.addWidget(self.addBtn)
        labels_layout.addWidget(self.delBtn)
       
        #modes and hotkey layout
        modes_hotkeys.addWidget(self.cModes)
        modes_hotkeys.addWidget(self.hotKey)
                
        #slider layout
        top_layout.addWidget(self.sliderLabel)
        top_layout.addWidget(self.slider)
        top_layout.addWidget(self.sliderEdit)
       
        #adding grid layouts 
        grid.addLayout(modes_hotkeys)
        grid.addLayout(labels_layout)
        grid.addLayout(outer_layout)
        grid.addLayout(top_layout)
        
        #continue button
        grid.addWidget(self.nextPage)

        #connect slider to textbox
        self.slider.valueChanged.connect(self.changeInValue)

        #connect fileselect and the file explore
        self.fileSelect.clicked.connect(self.fileExplore)
        
        #continue 
        self.nextPage.clicked.connect(self.on_continue_clicked)

        #showing hotkey window on press
        self.hotKey.clicked.connect(self.on_hotkey_clicked) 

        #connecting input dialog box 
        self.addBtn.clicked.connect(self.inputBoxes)

        #showing removeWindow on press
        self.delBtn.clicked.connect(self.on_del_clicked)


    #slider value 
    def changeInValue(self):
        self.sliderEdit.setText(str(self.slider.value()))
       
    #file selector
    def fileExplore(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        self.txtBox.setText(self.filename)
        self.data = self.filename
    
    #this updates values if the default ones arent wanted. comes from hotkey class
    def defaultUpdater(self, HKpass1, HKpass2, HKpass3, HKpass4):
        self.defaultHK1 = HKpass1
        self.defaultHK2 = HKpass2
        self.defaultHK3 = HKpass3
        self.defaultHK4 = HKpass4
        print(self.defaultHK2)
    
    #passes label names to main window from the hotkey class
    def LtxtGrab(self, Ltxt1, Ltxt2, Ltxt3, Ltxt4):
        self.Ltext1 = Ltxt1
        self.Ltext2 = Ltxt2
        self.Ltext3 = Ltxt3
        self.Ltext4 = Ltxt4

    #function to swap pages
    def on_continue_clicked(self):
        
        self.dialog = video_player(self.data, self.slider.value(), self.defaultHK1, self.defaultHK2
        ,self.defaultHK3, self.defaultHK4)
        
        self.dialog.show()
        
    #pass to hotey setting class
    def on_hotkey_clicked(self):
        self.valueHK.show()
    
    def on_del_clicked(self):
        self.removeCaller = removeWindow(self.comboList)
        self.comboList = []
        self.removeCaller.show()

    def closeLine(self):
        self.ComboTextRead()
    
    def removeLine(self, removeVal):
        self.RemoveVal = removeVal
 
        with open("comboFile.txt", "r") as input:
            with open("tempFile.txt", "w") as output:
                # iterate all lines from file
                for line in input:
                    # if text matches then don't write it
                    if line.strip("\n") != self.RemoveVal:
                        output.write(line)
        
        # replace file with original name
        os.replace('tempFile.txt', 'comboFile.txt')
        self.ComboTextRead()

    #Writing to text file and updating clabel on add
    def inputBoxes(self):
        self.text, addingInput = QInputDialog.getText(self, "Get text","New behavior:")

        if self.text:
            TempText1 = open("comboFile.txt", "a")

            self.textFixed = self.text.strip("\n")
            TempText1.write(self.text+ "\n")
            
            self.comboList.append(self.textFixed)
            TempText1.close()
            self.cLabels.addItem(self.textFixed)
            
    #Reading the file to populate clabel   
    def ComboTextRead(self):

        TempText1 = open("comboFile.txt", "r").readlines()
        self.cLabels.clear()

        for line in TempText1:
            textFixed = line.strip("\n")
            self.cLabels.addItem(textFixed)
            self.comboList.append(textFixed)
           
class removeWindow(QWidget):
       
    def __init__(self, comboBox):

        super().__init__()

        self.setWindowTitle("Remove Window")
        self.setGeometry(100, 100, 250, 100)

        self.comboList = comboBox
        print (self.comboList)
       
        self.init_ui()

    def init_ui(self):
        #creating layouts
        coreLayout = QVBoxLayout()
        removeLabelLayout = QHBoxLayout()
        comboBoxLayout = QHBoxLayout()
        confirmLayout = QHBoxLayout()

        #setting layouts
        coreLayout.addLayout(removeLabelLayout)
        coreLayout.addLayout(comboBoxLayout)
        coreLayout.addLayout(confirmLayout)
        self.setLayout(coreLayout)
       
        #creating widgets and adding to correct layout
        self.coreInfo = QLabel()
        self.comboInfo = QComboBox()
        self.cancelBtn = QPushButton()
        self.contBtn = QPushButton()

        removeLabelLayout.addWidget(self.coreInfo)
        comboBoxLayout.addWidget(self.comboInfo)
        confirmLayout.addWidget(self.cancelBtn)
        confirmLayout.addWidget(self.contBtn)

        #setting txt for widget
        self.cancelBtn.setText("Cancel")
        self.contBtn.setText("Save and Continue")

        #setting text for Qlabel
        self.coreInfo.setText("Select the behavior to remove and then press continue.")

        #populates list
        for x in self.comboList:
            self.comboInfo.addItem(x)

        #when clicked close 
        self.cancelBtn.clicked.connect(self.on_click_cancel)

        #when clicked update info close
        self.contBtn.clicked.connect(self.on_click_save)
        
    def on_click_cancel(self):
        window.closeLine()
        self.close()
    
    def on_click_save(self):
        
        self.removeValue = self.comboInfo.currentText() 
        window.removeLine(self.removeValue)   
        print (self.comboList)
        self.close()
                   

class hotKeyBinding(QWidget):
     
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotkey Settings")
        self.setGeometry(100, 100, 250, 100)
        
        #default values for hotkeys
        self.HKpass1 = "q"
        self.HKpass2 = "w"
        self.HKpass3 = "e"
        self.HKpass4 = "r"

        self.init_ui()  

    def init_ui(self):
        #creating layout
        coreLayout = QVBoxLayout()
        btnLayout1 = QHBoxLayout()
        btnLayout2 = QHBoxLayout()
        btnLayout3 = QHBoxLayout()
        btnLayout4 = QHBoxLayout()
           
        coreLayout.addLayout(btnLayout1)
        coreLayout.addLayout(btnLayout2)
        coreLayout.addLayout(btnLayout3)
        coreLayout.addLayout(btnLayout4)
        
        self.setLayout(coreLayout)

        #creating flag for HK and label
        self.HKflag = -1
        self.labelFlag = -1 

        #Qbuttons and labels for layout
        self.HKNum1 =QLabel("1.")
        self.HK1 = QPushButton("q")
        self.btnTxt1 = QLineEdit("")
        self.btnTxt1.setPlaceholderText("label name")
       
        self.HKNum2 =QLabel("2.")
        self.HK2 = QPushButton("w")
        self.btnTxt2 = QLineEdit("")
        self.btnTxt2.setPlaceholderText("label name")
       
        self.HKNum3 =QLabel("3.")
        self.HK3 = QPushButton("e")
        self.btnTxt3 = QLineEdit("")
        self.btnTxt3.setPlaceholderText("label name")
        
        self.HKNum4 =QLabel("4.")
        self.HK4 = QPushButton("r")
        self.btnTxt4 = QLineEdit("")
        self.btnTxt4.setPlaceholderText("label name")
             
        self.HKsave = QPushButton("save and exit")

        #connection
        self.HKsave.clicked.connect(self.HKSavenClose)

        #adding widgets
        btnLayout1.addWidget(self.HK1)
        btnLayout1.addWidget(self.btnTxt1)

        btnLayout2.addWidget(self.HK2)
        btnLayout2.addWidget(self.btnTxt2)

        btnLayout3.addWidget(self.HK3)
        btnLayout3.addWidget(self.btnTxt3)

        btnLayout4.addWidget(self.HK4)
        btnLayout4.addWidget(self.btnTxt4)

        coreLayout.addWidget(self.HKsave)

        #connect clicked with flags to stop multiple inputs on hotkey
        self.HK1.clicked.connect(self.HK1Clicked)
        self.HK2.clicked.connect(self.HK2Clicked)
        self.HK3.clicked.connect(self.HK3Clicked)
        self.HK4.clicked.connect(self.HK4Clicked)       

    # sets flag back to -1 and does hotkey setup
    def keyPressEvent(self, event: QEvent):
        if self.HKflag == 1:
            self.HK1.setText(event.text())
            self.HKpass1 = self.HK1.text()
            self.HKflag = -1
                     
        elif self.HKflag ==2:
            self.HK2.setText(event.text())
            self.HKpass2 = self.HK2.text()
            self.HKflag = -1
                  
        elif self.HKflag ==3:
            self.HK3.setText(event.text())
            self.HKpass3 = self.HK3.text()
            self.HKflag = -1
                     
        elif self.HKflag == 4:
            self.HK4.setText(event.text())
            self.HKpass4 = self.HK4.text()
            self.HKflag = -1
    
    #hotkey flag        
    def HK1Clicked(self):
        self.HKflag = 1
    def HK2Clicked(self):
        self.HKflag = 2
    def HK3Clicked(self):
        self.HKflag = 3
    def HK4Clicked(self):
        self.HKflag = 4
      
    #pass updated info back to main class
    def HKSavenClose(self):
        window.defaultUpdater( self.HKpass1, self.HKpass2, self.HKpass3, self.HKpass4)
        self.Ltxt1 = self.btnTxt1.text()
        self.Ltxt2 = self.btnTxt2.text()
        self.Ltxt3 = self.btnTxt3.text()
        self.Ltxt4 = self.btnTxt4.text() 
        window.LtxtGrab(self.Ltxt1, self.Ltxt2 , self.Ltxt3, self.Ltxt4)
        self.close()
       
#start of video player class
class video_player(QWidget):

    def __init__(self, data, sliderSize, hk1, hk2, hk3, hk4):
        super().__init__()
        
        #data for the file name
        self.data = data
        
        # this flag is so we can tell if the video is ready to be paused
        self.pauseFlag = True
        #data for the slider length
        self.sliderSize = int(sliderSize)
        
        self.setWindowTitle("Media Player")
        self.resize(700, 500)
        self.center()
        #save hk values
        self.HK1 = hk1 
        self.HK2 = hk2
        self.HK3 = hk3
        self.HK4 = hk4

        #flag for key press events
        self.iskeyPressed = False
        self.keyPressed = ""

        

        self.init_ui()
        self.show()
             
    def init_ui(self):

        #counter for freq
        self.frequencyCounter = []

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #set up signal
        self.mediaPlayer.positionChanged.connect(self.sliderTimer)
        # speed up the notify rate

        self.mediaPlayer.setNotifyInterval(10)

        #Tells if video is running or not
        self.videoFlag = False

        #create videowidget object

        videowidget = QVideoWidget()

        self.setFile()

        #create play button
        playBtn = QPushButton('play Video')
        playBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        playBtn.clicked.connect(self.play_video)

        #create pause button
        pauseBtn = QPushButton('pause Video')
        pauseBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        pauseBtn.clicked.connect(self.pause_video)
 
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(playBtn)
        hboxLayout.addWidget(pauseBtn)
        
        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.pause_video()
        event.accept() # let the window close


    #not fully sure but is in all Qmedia code i find
    def setFile(self):
        if self.data != '': 
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.data)))
  
    #function to play viceo
    def play_video(self):     
        self.mediaPlayer.play()
        self.videoFlag = True
        self.pauseFlag = True

    #function to pause video
    def pause_video(self):
        self.mediaPlayer.pause()
        self.videoFlag = False
        print("Pausing the Video.")

    
    def sliderTimer(self):
        #print("The time in the Video is: " , self.mediaPlayer.position())
        if self.pauseFlag == True:
            x = (self.sliderSize * 1000) 
            if (int(self.mediaPlayer.position()))  >= 1000:
                if (((self.mediaPlayer.position() % x) <= 5) | ((self.mediaPlayer.position() % x) >= (x - 5))):
                    print("The time in the Video is: " , self.mediaPlayer.position())
                    self.pauseFlag = False
                    self.pause_video()
                    if (self.iskeyPressed):
                        self.frequencyCounter.append(self.mediaPlayer.position()/1000)
                        self.frequencyCounter.append(self.keyPressed)
                    self.promptData()
                   

    def promptData(self):
        #popup box for data
        print(self.frequencyCounter)
        self.pop_up = popUpTable(self.frequencyCounter)


    #hotkey for logging  
    def keyPressEvent(self, e: QKeyEvent):
        pos = self.mediaPlayer.position()
        pos = pos/1000.0
        
        if self.videoFlag == True:

            if e.text() == self.HK1 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.iskeyPressed = True
                self.keyPressed = self.HK1
                print(self.frequencyCounter)
            
            elif e.text() == self.HK2 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.iskeyPressed = True
                self.keyPressed = self.HK2
                print(self.frequencyCounter)
            
            elif e.text() == self.HK3 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.iskeyPressed = True
                self.keyPressed = self.HK3
                print(self.frequencyCounter)
            
            elif e.text() == self.HK4 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.iskeyPressed = True
                self.keyPressed = self.HK4
                print(self.frequencyCounter)

        elif self.videoFlag == False:
            print ("video must be playing to use hotkeys")
    
    def keyReleaseEvent(self, e: QKeyEvent):
        pos = self.mediaPlayer.position()
        pos = pos/1000.0
        if self.videoFlag == True:

            if e.text() == self.HK1 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.frequencyCounter.append(self.HK1)
                self.iskeyPressed = False
                self.keyPressed = ""
                print(self.frequencyCounter)

            elif e.text() == self.HK2 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.frequencyCounter.append(self.HK2)
                self.iskeyPressed = False
                self.keyPressed = ""
                print(self.frequencyCounter)
                
            elif e.text() == self.HK3 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.frequencyCounter.append(self.HK3)
                self.iskeyPressed = False
                self.keyPressed = ""
                print(self.frequencyCounter)
            
            elif e.text() == self.HK4 and not e.isAutoRepeat():
                self.frequencyCounter.append(pos)
                self.frequencyCounter.append(self.HK4)
                self.iskeyPressed = False
                self.keyPressed = ""
                print(self.frequencyCounter)           
                
        elif self.videoFlag == False:
            print ("video must be playing to use hotkeys")

class popUpTable(QWidget):
    def __init__(self, data):
        super().__init__()
        
        #data for the file name
        self._data = data
        self._convertedData = self.convertTo2DArray(self._data)
        print(self._convertedData)
        self.setWindowTitle("Data")
        self.resize(700, 500)
        self.center()
        self.init_ui()

        
        self.show()

        
    
    def init_ui(self):

        self.grid = QVBoxLayout()
        self.buttons = QHBoxLayout()
        self.setLayout(self.grid)

        self.redoData = QPushButton()
        self.saveData = QPushButton()
        
        self.buttons.addWidget(self.redoData) 
        self.buttons.addWidget(self.saveData)
        self.grid.addLayout(self.buttons)
        if self._convertedData:
            self.tableWidget = QTableView()
            self.model = TableModel(self._convertedData)
            self.tableWidget.setModel(self.model)
            self.grid.addWidget(self.tableWidget)

        else:
            self.listLabel = QLabel()
            self.listLabel.setText(str(self._data))
            self.grid.addWidget(self.listLabel)

    def convertTo2DArray(self, data):
        if len(data) > 3:
            final = []
            for i in range(0, int(len(data)/3)):
                tmp = []
                for j in range(0, 3):
                    tmp.append(data[0])
                    data.pop(0)

                final.append(tmp) 

            return final

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = media_player()
    window.show()
    sys.exit(app.exec_())

