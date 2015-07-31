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

import os
from PyQt4 import QtCore, QtGui

kullanici = ""
parola = ""
env = os.getenv("HOME")

def setKull(text):
  global kullanici
  kullanici = text

def setParol(text):
  global parola
  parola = text

def kaydet():
  global kullanici, parola
  if (len(kullanici) == 0):
    print "[WARN] GSM NO (kullanici) Alanı boş geçilemez."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'GSM Numaranızı girmediniz.'")
  if (len(parola) == 0):
    print "[WARN] Parola Alanı boş geçilemez."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Parolanızı girmediniz.'")
  
  if (len(parola) > 0 and len(kullanici) > 0):
    print "[INFO] Veriler yazılıyor."
    f = open (env + '/.vodasms', 'w')
    f.write (kullanici + '\n' + parola )
    f.close()
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Ayarlar kaydedildi.'")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 60, 641, 71))
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhDialableCharactersOnly|QtCore.Qt.ImhPreferNumbers)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 20, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 190, 641, 71))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 150, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 270, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("textEdited(QString)"), setKull)
        QtCore.QObject.connect(self.lineEdit_2, QtCore.SIGNAL("textEdited(QString)"), setParol)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), kaydet)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Ayarlar", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "GSM Numarası", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Parola", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Kaydet", None, QtGui.QApplication.UnicodeUTF8))
        try:
	  f = open(env + '/.vodasms', 'r')
	  lines = f.readlines()
	  gsmno = lines[0].strip()
	  mypass = lines[1].strip()
	  self.lineEdit.setText(QtGui.QApplication.translate("MainWindow", gsmno, None, QtGui.QApplication.UnicodeUTF8))
	  self.lineEdit_2.setText(QtGui.QApplication.translate("MainWindow", mypass, None, QtGui.QApplication.UnicodeUTF8))
	except IOError:
	  print "[INFO] Kayıtlı ayar bulunamadı, boş kutular gösteriliyor."
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
