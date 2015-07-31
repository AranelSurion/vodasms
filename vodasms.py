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

import mechanize
import os
import re
import vodasmsui

# Variables
env = os.getenv("HOME")
debug = True # debug anahtarı açıkken mesaj gönderme ve kalan mesaj çalışmayacaktır.

# Mechanize connection
def baglan(arg,numara,mesaj):
  # Reading Settings
  print "[INFO-8] Veriler okunuyor."
  try:
    f = open(env + '/.vodasms', 'r')
    lines = f.readlines()
    gsmno = lines[0].strip()
    mypass = lines[1].strip()
  except IOError:
    print "[WARN-3] Veri bulunamadı. Ayarlar yapılmalı."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'GSM Numaranızı ve parolanızı ayarlamalısınız.'")
    return
  if (len(numara) == 0):
    print "[WARN-1] Numara hanesi boş olamaz. Devam edilmeyecek."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Numarayı girmediniz.'")
    return
  if (len(mesaj) == 0):
    print "[WARN-2] Mesaj hanesi boş olamaz. Devam edilmeyecek."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Mesajı girmediniz.'")
    return
  # Start-up
  global b
  b=mechanize.Browser()
  print "[INFO-1] İşlem yapılıyor."
  os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'İşlem yapılıyor.'")
  def cleanexit():
    try:
      def account_id_finder(f):
	return f.attrs.get('id') == 'account'
      b.select_form(predicate=account_id_finder)
      i=b.submit()
      b.open('http://www.vodafone.com.tr/logout.php')
      print "[INFO-3] Temiz çıkış işlemi tamamlandı."
      return
    except:
      print "[ERR-4] Temiz Cikis yapilamadi. Cay doldurayim mi iceriz beraber?"
      os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Temiz çıkış hatası. Hesabınız 10 dakika kadar askıda kalabilir, bu sırada sms gönderemeyeceksiniz.'")
  try:
    b.open('https://www.vodafone.com.tr/MyVodafone/login.php')
    b.select_form(nr=1)
  except:
    print "[ERR-1] Baglanti hatasi."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Bağlantı hatası'")
    return
  print b
  # Vodafone Logging-in
  b["GsmNo"] = gsmno
  b["MyPass"] = mypass
  try:
    i = b.submit()
  except:
    print "[ERR-4] Baglanti hatasi."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Bağlantı hatası'")
    return
  # WebSMS Code
  try:
    output = b.open('https://www.vodafone.com.tr/MyVodafone/myvodafone.php?pageId=WebSms')
    i = output.read()
    re1='.*?'	# Non-greedy match on filler
    re2='(k)'	# Variable Name 1
    re3='.*?'	# Non-greedy match on filler
    re4='(<B>)'	# Tag 1
    re5='(\\d+)'	# Integer Number 1
    re6='(<\\/B>)'	# Tag 2
    re7='.*?'	# Non-greedy match on filler
    re8='(adet)'	# Word 1
    
    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m = rg.search(i)
    if m:
      var1=m.group(1)
      tag1=m.group(2)
      int1=m.group(3)
      tag2=m.group(4)
      word1=m.group(5)
      kalanmesaj = int1
    
    b.select_form(nr=1)
  except:
    print "[ERR-2] Baglanti hatasi."
    os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'WebSMS hatası, hakkınız dolmuş olabilir?'")
    return
  print b
  if (debug  != True):
    print "[INFO-2] Debug modu kapali, uygulama devam ediyor."
    if (arg == 1):
      print "[INFO-5] Kalan sorgulaması yapılmıyor, normal devam edecek."
      b["WebSimSmsUserGsmNo"] = numara
      b["WebSimSmsText"] = mesaj
      try:
	i=b.submit()
      except:
	print "[ERR-3] Mesaj gonderilirken hata."
	os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Mesaj gönderme hatası, hakkınız dolmuş olabilir?'")
	cleanexit()
	return
      km = int(kalanmesaj) - 1
      print "[INFO-4] Mesaj gönderildi! Kalan mesaj:" + str(km)
      os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Mesaj başarıyla gönderildi! Kalan hakkınız: " + str(km) + "'")
    elif (arg == 0):
      print "[INFO-6] Kalan sorgulaması yapılıyor. Mesaj gönderilmeyecek."
      print "[INFO-7] Kalan mesaj hakkı:" + kalanmesaj
      os.system("dbus-send --type=method_call --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.SystemNoteInfoprint string:'Kalan mesaj hakkınız: " + kalanmesaj + "'")
      
  # Clean Log-off
  cleanexit()
  b.close()