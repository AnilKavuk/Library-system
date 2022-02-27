# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 16:15:12 2020

@author: anlka
"""


#------------------Kütüphaneler-------------------#
import sys
import sqlite3
from PyQt5 import *
from PyQt5.QtWidgets import *
from library import *
#------------------Kütüphaneler-------------------#

#-------Library penceresini aç----------------#
Uygulama = QApplication(sys.argv)
penAnasayfa = QMainWindow()
ui = Ui_MainWindow()             #  1. EKRANDAKİ İŞLEMLER İÇİN Uİ TANIMLI #
ui.setupUi(penAnasayfa)
penAnasayfa.show()
#-------Library penceresini aç----------------#

#-------------veritabanı oluştur---------------#
global curs
global conn

conn=sqlite3.connect('kutuphane.db') #veri tabanı oluştur.
curs=conn.cursor()
kutuphane_db=("CREATE TABLE IF NOT EXISTS kayitlar(\
          Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
              KitapNo TEXT NOT NULL UNIQUE,\
                  KitapAdi TEXT NOT NULL UNIQUE,\
                      YazarAdi TEXT NOT NULL,\
                          YayinEvi TEXT NOT NULL,\
                              YayinTarihi TEXT NOT NULL,\
                                  Tur TEXT NOT NULL,\
                                      RafNo INTEGER NOT NULL,\
                                          RafAyrac TEXT NOT NULL,\
                                              Dil TEXT NOT NULL,\
                                                  Icerik TEXT NOT NULL)")
curs.execute(kutuphane_db)
conn.commit()   
#-------------veritabanı oluştur---------------#

#---------------------Sisteme kayıt ekle--------------------------------#
def ekle():
    kitapNo=ui.kitapNo.text()
    kitapAdi=ui.kitapAdi.text()
    yazarAdi=ui.yazarAdi.text()
    yayinEvi=ui.yayinEvi.text()
    cmbTarihi=ui.cmbTarihi.currentText()
    tur=ui.tur.text()
    rafNo=ui.rafNo.value()
    rafAyrac=ui.rafAyrac.currentText()
    dil=ui.dil.text()
    icerik=ui.icerik.toPlainText()
    curs.execute("INSERT INTO kayitlar\
                       (KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik)\
                           VALUES(?,?,?,?,?,?,?,?,?,?)",(kitapNo,kitapAdi,yazarAdi,yayinEvi,cmbTarihi,tur,rafNo,rafAyrac,dil,icerik))
    conn.commit()
    listele()  



#---------------------Sisteme kayıt ekle--------------------------------#


#--------------------Sisteme kayıt listele------------------------------#
def listele():
    tblLibrary=ui.tblLibrary.clear()
    ui.tblLibrary.setHorizontalHeaderLabels(('Kitap No','Kitap Adı','Yazar Adı', 'Yayın Evi',\
                                                           'Yayın Tarihi','Tür','Raf No','Raf Ayraç', \
                                                               'Dil','İçerik'))
    ui.tblLibrary.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgular=curs.execute("SELECT KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik  FROM kayitlar")
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblLibrary.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.kitapNo.clear()
    ui.kitapAdi.clear()
    ui.yazarAdi.clear()
    ui.yayinEvi.clear()
    ui.cmbTarihi.setCurrentIndex(-1)
    ui.tur.clear()
    ui.rafNo.setValue(1)
    ui.rafAyrac.setCurrentIndex(-1)
    ui.dil.clear()
    ui.icerik.clear()
    
    curs.execute("SELECT COUNT(*) FROM kayitlar")
    sorguSayisi=curs.fetchone()
    ui.kayitSayisi.setText(" Kayıtlı Kitap Sayısı :"+str(sorguSayisi[0]))        
listele()                    
                





#--------------------Sisteme kayıt listele------------------------------#



#--------------------Sisteme kayıt sil------------------------------#
def Sil():
    Soru2=QMessageBox.question(penAnasayfa, "Kayıt Sil", "Kaydı silmek istediğinize emin misiniz ?",\
                              QMessageBox.Yes | QMessageBox.No)
    if(Soru2==QMessageBox.Yes):
            secili=ui.tblLibrary.selectedItems()
            silinecek=secili[0].text()
            try:
                curs.execute("DELETE FROM kayitlar WHERE KitapNo='%s' "%(silinecek))
                conn.commit()
                listele()
                ui.statusbar.showMessage("Kayıt silme işlemi başarıyla gerçekleşti...",10000)
            except Exception as Hata:
                 ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Kayıt silme işlemi iptal edildi...",10000)


#--------------------Sisteme kayıt sil------------------------------#


#--------------------Sisteme kayıt doldur------------------------------#
def doldur():
    try:
        secili1=ui.tblLibrary.selectedItems()
        ui.kitapNo.setText(secili1[0].text())            #Table widget verileri yukardaki yazdıklarımız yeri aynen geçiriyor.
        ui.kitapAdi.setText(secili1[1].text())
        ui.yazarAdi.setText(secili1[2].text())
        ui.yayinEvi.setText(secili1[3].text())
        ui.cmbTarihi.setCurrentText(secili1[4].text())
        ui.tur.setText(secili1[5].text())
        ui.rafNo.setValue(int(secili1[6].text()))
        ui.rafAyrac.setCurrentText(secili1[7].text())          
        ui.dil.setText(secili1[8].text())
        ui.icerik.setText(secili1[9].text())
        
        
    except Exception as hata:
        ui.statusbar.showMessage("bir hata tespit edildil....:"+str(hata),10000)
#--------------------Sisteme kayıt doldur------------------------------#


#--------------Sistemi Güncelle---------------------------------------#
def guncelle():
    Soru3=QMessageBox.question(penAnasayfa, "Kaydı Güncelle", "Kaydı güncellemek istediğinize emin misiniz ?",\
                              QMessageBox.Yes | QMessageBox.No)
    if(Soru3==QMessageBox.Yes):
        try:
            secili2=ui.tblLibrary.selectedItems()
            KitapNo1=secili2[0].text()
            kitapNo=ui.kitapNo.text()
            kitapAdi=ui.kitapAdi.text()
            yazarAdi=ui.yazarAdi.text()
            yayinEvi=ui.yayinEvi.text()
            cmbTarihi=ui.cmbTarihi.currentText()
            tur=ui.tur.text()
            rafNo=ui.rafNo.value()
            rafAyrac=ui.rafAyrac.currentText()
            dil=ui.dil.text()
            icerik=ui.icerik.toPlainText()
            curs.execute("UPDATE kayitlar SET \
                       KitapNo=?,KitapAdi=?,YazarAdi=?,YayinEvi=?,YayinTarihi=?,\
                           Tur=?,RafNo=?,RafAyrac=?,Dil=?,Icerik=? WHERE KitapNo=?",\
                               (kitapNo,kitapAdi,yazarAdi,yayinEvi,cmbTarihi,tur, \
                                rafNo,rafAyrac,dil,icerik,KitapNo1))

                           
            conn.commit()
            listele()
            ui.statusbar.showMessage("Kayıt güncelleme işlemi başarıyla gerçekleşti...",10000)
        except Exception as hata:
            print(str(hata))
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(hata),10000)
    else:
        ui.statusbar.showMessage("Kayıt Güncelleme işlemi iptal edildi...",10000)






#--------------Sistemi Güncelle---------------------------------------#


#--------------Sistemi Ara---------------------------------------#
def ara1():
    aranan1=ui.aranacakKelime.text()
    
    
    curs.execute("SELECT KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik FROM kayitlar WHERE KitapAdi=?   ",\
                 (aranan1,))
    conn.commit()
    ui.tblLibrary.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblLibrary.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.tblLibrary.setHorizontalHeaderLabels(('Kitap No','Kitap Adı','Yazar Adı', 'Yayın Evi',\
                                                           'Yayın Tarihi','Tür','Raf No','Raf Ayraç', \
                                                               'Dil','İçerik'))   


def ara2():
    aranan2=ui.aranacakKelime.text()
    
    
    curs.execute("SELECT KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik FROM kayitlar WHERE YazarAdi=?   ",\
                 (aranan2,))
    conn.commit()
    ui.tblLibrary.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblLibrary.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.tblLibrary.setHorizontalHeaderLabels(('Kitap No','Kitap Adı','Yazar Adı', 'Yayın Evi',\
                                                           'Yayın Tarihi','Tür','Raf No','Raf Ayraç', \
                                                               'Dil','İçerik'))   


def ara3():
    aranan3=ui.aranacakKelime.text()
    
    
    curs.execute("SELECT KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik FROM kayitlar WHERE YayinEvi=?   ",\
                 (aranan3,))
    conn.commit()
    ui.tblLibrary.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblLibrary.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.tblLibrary.setHorizontalHeaderLabels(('Kitap No','Kitap Adı','Yazar Adı', 'Yayın Evi',\
                                                           'Yayın Tarihi','Tür','Raf No','Raf Ayraç', \
                                                               'Dil','İçerik'))   

def ara4():
    aranan4=ui.aranacakKelime.text()
    
    
    curs.execute("SELECT KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik FROM kayitlar WHERE Dil=?   ",\
                 (aranan4,))
    conn.commit()
    ui.tblLibrary.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblLibrary.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.tblLibrary.setHorizontalHeaderLabels(('Kitap No','Kitap Adı','Yazar Adı', 'Yayın Evi',\
                                                           'Yayın Tarihi','Tür','Raf No','Raf Ayraç', \
                                                               'Dil','İçerik'))
def ara5():
    aranan4=ui.aranacakKelime.text()
    
    
    curs.execute("SELECT KitapNo,KitapAdi,YazarAdi,YayinEvi,YayinTarihi,Tur,RafNo,RafAyrac,Dil,Icerik FROM kayitlar WHERE Tur=?   ",\
                 (aranan4,))
    conn.commit()
    ui.tblLibrary.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblLibrary.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.tblLibrary.setHorizontalHeaderLabels(('Kitap No','Kitap Adı','Yazar Adı', 'Yayın Evi',\
                                                           'Yayın Tarihi','Tür','Raf No','Raf Ayraç', \
                                                               'Dil','İçerik'))
#--------------Sistemi Ara---------------------------------------#



#---------------kayıt ekle sinyal slotu------------------------------#
ui.kayitEkle.clicked.connect(ekle)
#---------------kayıt ekle sinyal slotu------------------------------#


#---------------kayıt listele sinyal slotu------------------------------#
ui.kayitListele.clicked.connect(listele)
#---------------kayıt listele sinyal slotu------------------------------#

#---------------kayıt Sil sinyal slotu------------------------------#
ui.kayitSil.clicked.connect(Sil)
#---------------kayıt Sil sinyal slotu------------------------------#

#---------------------Sistem doldur sinyal slot-----------------------#
#--------------------------------------------------------------------#
ui.tblLibrary.itemSelectionChanged.connect(doldur)
#---------------------Sistem doldur sinyali slot-----------------------#
#---------------------------------------------------------------------#


#---------------------Sistem Güncelle sinyal slot-----------------------#
#--------------------------------------------------------------------#
ui.kayitGuncelle.clicked.connect(guncelle)
#---------------------Sistem Güncelle sinyali slot-----------------------#
#---------------------------------------------------------------------#


#---------------------Sistem kayit adi bul sinyal slot-----------------------#
#--------------------------------------------------------------------#
ui.kitap_Adi.clicked.connect(ara1)
ui.yazar_Adi.clicked.connect(ara2)
ui.yayin_Evi.clicked.connect(ara3)
ui.dil_1.clicked.connect(ara4)
ui.tur_1.clicked.connect(ara5)
#---------------------Sistem Güncelle sinyali slot-----------------------#
#---------------------------------------------------------------------#



sys.exit(Uygulama.exec_())