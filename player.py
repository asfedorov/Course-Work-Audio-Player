# -*- coding: utf-8 -*-

import sys, os, time, tempfile, random
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon
from ui_mainform import Ui_MainWindow

##main window class
class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.metaInformationResolver = Phonon.MediaObject(self)
        self.mediaObject = Phonon.MediaObject(self)
        self.ui.seekSlider.setMediaObject(self.mediaObject)
        self.ui.volumeSlider.setAudioOutput(self.audioOutput)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        
        self.ui.display_songname.setText('No song')
        self.ui.display_songname.setMargin(50)
        
        ##connecting signals
        self.connect(self.ui.button_play, QtCore.SIGNAL('pressed()'),self.playPause)
        self.connect(self.ui.button_next, QtCore.SIGNAL('pressed()'),self.playNext)
        self.connect(self.ui.button_previous, QtCore.SIGNAL('pressed()'),self.playPrevious)
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'),self.close)
        self.connect(self.ui.actionOpen, QtCore.SIGNAL('triggered()'),self.openFile)
        self.connect(self.ui.actionAdd_Directory, QtCore.SIGNAL('triggered()'),self.openDir)
        self.connect(self.mediaObject, QtCore.SIGNAL("metaDataChanged()"),self.updateData)
        self.connect(self.mediaObject, QtCore.SIGNAL("aboutToFinish()"),self.queueSong)
        self.connect(self.ui.playlist, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"),self.playSelected)
        self.connect(self.ui.checkShuffle, QtCore.SIGNAL("stateChanged(int)"),self.playlistShuffle)
        self.connect(self.ui.button_add_s, QtCore.SIGNAL('pressed()'),self.openFile)
        self.connect(self.ui.button_add_d, QtCore.SIGNAL('pressed()'),self.openDir)
        self.connect(self.ui.button_rmv_s, QtCore.SIGNAL('pressed()'),self.removeFile)
        self.connect(self.ui.button_move_up, QtCore.SIGNAL('pressed()'),self.moveUp)
        self.connect(self.ui.button_move_down, QtCore.SIGNAL('pressed()'),self.moveDown)
        self.connect(self.ui.button_move_upup, QtCore.SIGNAL('pressed()'),self.moveUpUp)
        self.connect(self.ui.button_move_downdown, QtCore.SIGNAL('pressed()'),self.moveDownDown)
        
        self.filename=""
        self.playlist = []
        self.current_song = 0
    
    ##move audiofile to the bottm of the list
    def moveDownDown(self):
        if self.ui.playlist.row(self.ui.playlist.selectedItems()[0]) != self.ui.playlist.count()-1:
            self.ui.playlist.insertItem(self.ui.playlist.count()-1,self.ui.playlist.takeItem(self.ui.playlist.row(self.ui.playlist.selectedItems()[0])))
            self.ui.playlist.setCurrentItem(self.ui.playlist.item(self.ui.playlist.count()-1))
            if self.ui.checkShuffle.checkState() == 0:
                self.c_song_name = self.playlist[self.current_song]
                self.playlist = []
                i = 0
                while i != self.ui.playlist.count():
                    self.playlist.append(self.ui.playlist.item(i).text())            
                    i = i + 1
                self.current_song = self.playlist.index(self.c_song_name)
        else:
            pass
        self.mediaObject.clearQueue()
        
    ##move audiofile to the top of the list
    def moveUpUp(self):
        if self.ui.playlist.row(self.ui.playlist.selectedItems()[0]) != 0:
            self.ui.playlist.insertItem(0,self.ui.playlist.takeItem(self.ui.playlist.row(self.ui.playlist.selectedItems()[0])))
            self.ui.playlist.setCurrentItem(self.ui.playlist.item(0))
            if self.ui.checkShuffle.checkState() == 0:
                self.c_song_name = self.playlist[self.current_song]
                self.playlist = []
                i = 0
                while i != self.ui.playlist.count():
                    self.playlist.append(self.ui.playlist.item(i).text())            
                    i = i + 1
                self.current_song = self.playlist.index(self.c_song_name)
        else:
            pass
        self.mediaObject.clearQueue()
    
    ##move audiofile a position down in list
    def moveDown(self):
        if self.ui.playlist.row(self.ui.playlist.selectedItems()[0]) != self.ui.playlist.count()-1:
            self.ui.playlist.insertItem((self.ui.playlist.row(self.ui.playlist.selectedItems()[0])+1),self.ui.playlist.takeItem(self.ui.playlist.row(self.ui.playlist.selectedItems()[0])))
            self.ui.playlist.setCurrentItem(self.ui.playlist.item(self.ui.playlist.row(self.ui.playlist.selectedItems()[0])+1))
            if self.ui.checkShuffle.checkState() == 0:
                self.c_song_name = self.playlist[self.current_song]
                self.playlist = []
                i = 0
                while i != self.ui.playlist.count():
                    self.playlist.append(self.ui.playlist.item(i).text())            
                    i = i + 1
                self.current_song = self.playlist.index(self.c_song_name)
        else:
            pass
        self.mediaObject.clearQueue()
    
    ##move audiofile a position up in list
    def moveUp(self):
        if self.ui.playlist.row(self.ui.playlist.selectedItems()[0]) != 0:
            self.ui.playlist.insertItem((self.ui.playlist.row(self.ui.playlist.selectedItems()[0])-1),self.ui.playlist.takeItem(self.ui.playlist.row(self.ui.playlist.selectedItems()[0])))
            self.ui.playlist.setCurrentItem(self.ui.playlist.item(self.ui.playlist.row(self.ui.playlist.selectedItems()[0])-2))
            if self.ui.checkShuffle.checkState() == 0:
                self.c_song_name = self.playlist[self.current_song]
                self.playlist = []
                i = 0
                while i != self.ui.playlist.count():
                    self.playlist.append(self.ui.playlist.item(i).text())            
                    i = i + 1
                self.current_song = self.playlist.index(self.c_song_name)
        else:
            pass
        self.mediaObject.clearQueue()
        
    
    ##remove audiofile from list
    def removeFile(self):
        song = self.ui.playlist.selectedItems()[0]
        
        self.playlist.remove(unicode(song.text()))
        self.ui.playlist.takeItem(self.ui.playlist.row(song))
        self.mediaObject.clearQueue()

    ##check shuffle
    def playlistShuffle(self):
        if self.ui.checkShuffle.checkState() == 2:
            random.shuffle(self.playlist)
        if self.ui.checkShuffle.checkState() == 0:
            self.c_song_name = self.playlist[self.current_song]
            self.playlist = []
            i = 0
            while i != self.ui.playlist.count()-1:
                self.playlist.append(self.ui.playlist.item(i).text())            
                i = i + 1
            self.current_song = self.playlist.index(self.c_song_name)
        self.mediaObject.clearQueue()
    
    ##on double-click playing
    def playSelected(self):
        self.selected = unicode(self.ui.playlist.selectedItems()[0].text())
        self.current_song = self.playlist.index(self.selected)
        try:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(unicode(self.playlist[self.current_song])))
            self.mediaObject.play()
        except:
            self.playNext()
        self.mediaObject.clearQueue()
        if self.ui.checkShuffle.checkState() != 0:
            random.shuffle(self.playlist)
            
    ##queueing next song
    def queueSong(self):
        self.next_song = self.current_song + 1
        if self.playlist.__len__() <= self.next_song:
            self.next_song = 0

        self.mediaObject.enqueue(Phonon.MediaSource(unicode(self.playlist[self.next_song])))
    
    ##updating song data
    def updateData(self):
        self.artist = unicode(self.mediaObject.metaData().get(QtCore.QString('ARTIST'), [QtCore.QString()])[0])
        self.title = unicode(self.mediaObject.metaData().get(QtCore.QString('TITLE'), [QtCore.QString()])[0])
    
        self.ui.display_songname.setText(self.artist + ' - ' + self.title)
        self.mediaObject.clearQueue()
        
        self.playing_item = self.ui.playlist.findItems(unicode(self.mediaObject.currentSource().fileName()), QtCore.Qt.MatchExactly)
        self.ui.playlist.setCurrentItem(self.playing_item[0])
    
    ##close player
    def close(self):
        sys.exit()
    
    ##opening file or directory
    def openFile(self):
        self.filenames = QtGui.QFileDialog.getOpenFileNames(self, 'Open File')

        for filename in self.filenames:
            self.playlist.append(filename)
            self.ui.playlist.addItem(filename)
        self.mediaObject.clearQueue()
        if self.ui.checkShuffle.checkState() != 0:
            random.shuffle(self.playlist)

    ##adding files from directory
    def openDir(self):
        self.dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Add Directory'))
        
            
        dirs = []
        files = []
        for dirname, dirnames, filenames in os.walk(self.dir):
            dirs.append(dirname)
            for subdirname in dirnames:
                dirs.append(os.path.join(dirname, subdirname))
            for filename in filenames:
                files.append(os.path.join(dirname, filename)) 
                
        for x in files:
            self.playlist.append(x)
            self.ui.playlist.addItem(x)
        if self.ui.checkShuffle.checkState() != 0:
            random.shuffle(self.playlist)
    
    ##play/pause
    def playPause(self):
        if self.ui.playlist.selectedItems()[0] == None or unicode(self.ui.playlist.selectedItems()[0].text()) == unicode(self.playlist[self.current_song]):
            if self.mediaObject.state() == Phonon.PlayingState:
                self.mediaObject.pause()
            elif self.mediaObject.state() == Phonon.PausedState:
                self.mediaObject.play()
            else:
                if self.playlist != []:
                    self.mediaObject.setCurrentSource(Phonon.MediaSource(unicode(self.playlist[self.current_song])))
                else:
                    self.openFile()
                    self.current_song = 0
                    self.playPause()

                self.mediaObject.play()
        else:
            self.playSelected()
            
    ##next song
    def playNext(self):        
        self.current_song = self.current_song + 1
        if self.playlist.__len__() <= self.current_song:
            self.current_song = 0
        try:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(unicode(self.playlist[self.current_song])))
            self.mediaObject.play()
        except:
            self.playNext()
        self.mediaObject.clearQueue()
    
    ##previous song
    def playPrevious(self):
        self.current_song = self.current_song - 1
        if self.current_song < 0:
            self.current_song = self.playlist.__len__() - 1
        try:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(unicode(self.playlist[self.current_song])))
            self.mediaObject.play()
        except:
            self.playNext()
        self.mediaObject.clearQueue()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("JustSimpleAudioPlayer")
    myapp = StartQT4()
    myapp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass