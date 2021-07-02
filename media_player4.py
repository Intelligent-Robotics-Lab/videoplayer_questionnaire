import sys
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QButtonGroup, QLabel, QLayout, QLineEdit, QPushButton, QSlider, QVBoxLayout, QWidget,QFileDialog, QGridLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer , QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget



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
        self.data = ''
        
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
        
        #might want to move this line somewhere else or readability
        self.dialog = video_player(self.data)

        #continue 
        self.nextPage.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        self.dialog.show()

    #slider value 
    def changeInValue(self):
        size = str(self.slider.value())
        self.sliderEdit.setText(size)
       
    #file selector
    def fileExplore(self):
        self.videoFile = QFileDialog.getOpenFileName(directory = "c://")
        self.txtBox.setText(self.videoFile[0])
        self.data = self.videoFile[0]
        

        
        

class video_player(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.grid = QVBoxLayout()
        self.setWindowTitle("Media Player")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()
        self.playButton = QPushButton()
        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(data)))
        self.grid.addWidget(videowidget)
        self.setLayout(self.grid)
        
        
        self.frame2()

    def frame2(self):
        #grid layout
        outer_layout2 = QHBoxLayout()
        top_layout2 = QHBoxLayout()
        bot_layout2 = QVBoxLayout()
        self.playButton.setText("play video")
        self.grid.addLayout(outer_layout2)
        outer_layout2.addWidget(self.playButton)
        self.playButton.clicked.connect(self.play_video)

    def play_video(self):
        self.mediaPlayer.play()
        

         
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = media_player()
    window.show()
    sys.exit(app.exec_())