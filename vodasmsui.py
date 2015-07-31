# -*- coding: utf-8 -*-
# VodaSMS - Vodafone Turkey WebSMS Application
# Aranel Surion <aranel@aranelsurion.org> @ January, 2011

#    This file is part of VodaSMS.
#
#    VodaSMS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VodaSMS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VodaSMS.  If not, see <http://www.gnu.org/licenses/>.
from vodasms import *
from PyQt4 import QtCore, QtGui
import os

numara = ""
mesaj = ""
kalanmesaj= ""

def setNumara(text):
  global numara
  numara = text

def bagla():
  global numara,tedit
  baglan(1,numara,mesaj)
  tedit.setPlainText("")

def kala():
  baglan(0,"0","0")

def hakkinda():
  os.system("python hakkindaui.py")

def ayarlar():
  os.system("python ayarlarui.py")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
	global tedit
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(560, 320, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 90, 741, 231))
        self.textEdit.setObjectName("textEdit")
        tedit = self.textEdit
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
	self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
	self.pushButton_2.setGeometry(QtCore.QRect(30, 320, 211, 71))
	font = QtGui.QFont()
	font.setPointSize(28)
	self.pushButton_2.setFont(font)
	self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit.setGeometry(QtCore.QRect(130, 20, 641, 71))
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhDialableCharactersOnly|QtCore.Qt.ImhPreferNumbers)
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(360, 310, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar_2)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menuBar.setObjectName("menuBar")
        self.menuSometin = QtGui.QMenu(self.menuBar)
        self.menuSometin.setObjectName("menuSometin")
        MainWindow.setMenuBar(self.menuBar)
        self.actionAyarlar_2 = QtGui.QAction(MainWindow)
        self.actionAyarlar_2.setObjectName("actionAyarlar_2")
        self.actionHakk_nda_2 = QtGui.QAction(MainWindow)
        self.actionHakk_nda_2.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionHakk_nda_2.setObjectName("actionHakk_nda_2")
        self.menuSometin.addSeparator()
        self.menuSometin.addAction(self.actionAyarlar_2)
        self.menuSometin.addAction(self.actionHakk_nda_2)
        self.menuBar.addAction(self.menuSometin.menuAction())
        
        def setMesaj():
	  global mesaj
	  mesaj = unicode(self.textEdit.toPlainText().toUtf8(), "utf-8")
	  ascii = mesaj.encode("ascii", "ignore")
	  i = 159 - len(mesaj)
	  self.label_3.setText(QtGui.QApplication.translate("MainWindow", str(i), None, QtGui.QApplication.UnicodeUTF8))
	  if ascii != mesaj:
	    self.textEdit.setPlainText(ascii)
	    cur = self.textEdit.textCursor()
	    cur.movePosition(QtGui.QTextCursor.End)
	    self.textEdit.setTextCursor(cur)
	    
	    
	  if (len(mesaj)) > 159:
	    print "[WARN-1] Mesaj 160 karakterden fazla?"
	    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Mesaj 160 karakterden fazla olamaz.'")
	    i = len(mesaj) - 159
	    mesaj = mesaj [:-i]
	    self.textEdit.setPlainText(mesaj)
	    cur = self.textEdit.textCursor()
	    cur.movePosition(QtGui.QTextCursor.End)
	    self.textEdit.setTextCursor(cur)
	    
	  
        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("textEdited(QString)"), setNumara)
        QtCore.QObject.connect(self.textEdit, QtCore.SIGNAL("textChanged()"), setMesaj)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), bagla)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), kala)
        QtCore.QObject.connect(self.actionHakk_nda_2, QtCore.SIGNAL("triggered()"), hakkinda)
        QtCore.QObject.connect(self.actionAyarlar_2, QtCore.SIGNAL("triggered()"), ayarlar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        




    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "VodaSMS", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Gönder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Kime:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "159", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Kalan", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_2.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSometin.setTitle(QtGui.QApplication.translate("MainWindow", "MainMenu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAyarlar_2.setText(QtGui.QApplication.translate("MainWindow", "Ayarlar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHakk_nda_2.setText(QtGui.QApplication.translate("MainWindow", "Hakkında", None, QtGui.QApplication.UnicodeUTF8))
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    

