import sys
from typing import Sized
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QButtonGroup, QLabel, QLayout, QLineEdit, QPushButton, QSlider, QVBoxLayout, QWidget,QFileDialog, QGridLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer , QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl






#main window
class media_player(QWidget): 
    def __init__(self):
        super().__init__()
 
        #window size and name
        self.setWindowTitle("Media Player")
        self.setFixedWidth(800)
        self.setFixedHeight(150)

        #creating widgts and call frame
        self.slider = QSlider()
        self.txtBox = QLineEdit()
        self.sliderEdit = QLineEdit()
        self.fileSelect = QPushButton()
        self.nextPage =QPushButton()
        
        self.videoFile = QFileDialog()
        self.data = ""
        self.sliderSize = ""
        
        self.frame1()
       
    def frame1(self):
        #grid layout
        grid = QVBoxLayout()
        outer_layout = QHBoxLayout()
        top_layout = QHBoxLayout()

        self.setLayout(grid)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.txtBox.setText("Select A file")
        self.fileSelect.setText("...")
        self.nextPage.setText("Continue")
        
        #setting size
        self.slider.setMaximumWidth(600)
        self.txtBox.setMaximumWidth(600)
        self.nextPage.setMaximumWidth(800)
        self.fileSelect.setMaximumWidth(150)
        self.sliderEdit.setMaximumWidth(150)

        #setting widgets frame1
        outer_layout.addWidget(self.txtBox)
        outer_layout.addWidget(self.fileSelect)
        grid.addLayout(outer_layout)
        top_layout.addWidget(self.slider)
        top_layout.addWidget(self.sliderEdit)
        grid.addLayout(top_layout)
        grid.addWidget(self.nextPage)

        #connect slider to textbox
        self.slider.valueChanged.connect(self.changeInValue)

        #connect fileselect and the file explore
        self.fileSelect.clicked.connect(self.fileExplore)
        
        #continue 
        self.nextPage.clicked.connect(self.on_continue_clicked)

    def on_continue_clicked(self):
        self.dialog = video_player(self.data, self.sliderSize)
        self.dialog.show()

    #slider value 
    def changeInValue(self):
        self.sliderSize = str(self.slider.value())
        self.sliderEdit.setText(self.sliderSize)
        
       
    #file selector
    def fileExplore(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        self.txtBox.setText(self.filename)
        self.data = self.filename
        
              
        
#start of video player class
class video_player(QWidget):
    

    def __init__(self, data, sliderSize):
        super().__init__()
        #data for the file name
        self.data = data
        #data for the slider length
        self.sliderSize = sliderSize
        print(self.sliderSize)
        self.setWindowTitle("Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.init_ui()
        self.show()
        
        
        
    def init_ui(self):

        #counter for freq
        self.frequencyCounter = []

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #Tells if video is running or not
        self.videoFlag = False


        #create videowidget object

        videowidget = QVideoWidget()

        self.setFile()

        #duration signal
        #self.mediaPlayer.durationChanged.connect(self.duration_changed)

        #create play button
        playBtn = QPushButton('play Video')
        playBtn.clicked.connect(self.play_video)

        #create pause button
        pauseBtn = QPushButton('pause Video')
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

    #not fully sure but is in all Qmedia code i find
    def setFile(self):
        if self.data != '': 
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.data)))
  
    #function to play viceo
    def play_video(self):     
        self.mediaPlayer.play()
        self.videoFlag = True

    #function to pause video
    def pause_video(self):
        self.mediaPlayer.pause()
        self.videoFlag = False

    def media_length(self):
       seconds = self.sliderSize

    #hotkey for chekcing data  
    def keyPressEvent(self, event):
        if self.videoFlag == True:

            if event.key() == Qt.Key_Z:
                print ("you pressed z")
                self.frequencyCounter.append(1)
                print(self.frequencyCounter)
        elif event.key() == Qt.Key_Z:
            print ("video must be playing to use hotkeys")


        
        

   

         
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = media_player()
    window.show()
    sys.exit(app.exec_())