import sys
import sqlite3  # EKLENDİ: Veritabanı modülü
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QAbstractItemView
from PySide6.QtCore import Qt, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon
import kaynaklar_rc


class UygulamaYonetimi:
    def __init__(self):
        self.loader = QUiLoader()

        # 1. Form nesneleri oluşturuluyor
        self.splash_formu = self.loader.load("splash.ui")
        self.ana_form = self.loader.load("anaekran.ui")
        self.crud_form = self.loader.load("crud.ui")
        self.kitaplik_form = self.loader.load("kitaplik.ui")

        # 2. Üst çerçeveyi gizle
        self.splash_formu.setWindowFlags(Qt.FramelessWindowHint)

        # 3. Timer  Ayarları
        self.timer = QTimer()
        self.timer.setInterval(4000)  # 4 saniye
        self.timer.timeout.connect(self.ana_ekrana_gec)

        # 4. Sistemi Başlat
        self.splash_formu.show()
        self.timer.start()

        # 5. Form Geçişleri
        self.ana_form.kitap_islem.clicked.connect(self.crud_ekranini_ac)
        self.crud_form.geri_don.clicked.connect(self.ana_ekrana_don)

        self.ana_form.kitap_inceleme.clicked.connect(self.kitap_islem_gec)
        self.kitaplik_form.geri_don_2.clicked.connect(self.ana_ekrana_don_2)

        # 6. CRUD Buton Bağlantıları
        self.crud_form.pushButton.clicked.connect(self.kitap_ekle)
        self.crud_form.pushButton_2.clicked.connect(self.kitap_sil)
        self.crud_form.pushButton_3.clicked.connect(self.kitap_guncelle)

        # 7. Sistem ilk açıldığında listeleri ve barı doldur (DÜZELTİLDİ)
        self.tabloyu_doldur()
        self.bar_guncelle()

        #8 elle düzeltme kapalı
        self.crud_form.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.kitaplik_form.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # --- GEÇİŞ FONKSİYONLARI ---
    def ana_ekrana_gec(self):
        self.timer.stop()
        self.ana_form.showMaximized()
        self.splash_formu.close()

    def crud_ekranini_ac(self):
        self.ana_form.hide()
        self.crud_form.showMaximized()

    def ana_ekrana_don(self):
        self.crud_form.hide()
        self.ana_form.showMaximized()

    def ana_ekrana_don_2(self):
        self.kitaplik_form.hide()
        self.ana_form.showMaximized()

    def kitap_islem_gec(self):
        self.ana_form.hide()
        self.kitaplik_form.showMaximized()
        # YENİ: Kitaplık formuna geçer geçmez o formdaki tabloyu doldurur
        self.kitaplik_tabloyu_doldur()

    def kitap_islem_don(self):
        self.kitaplik_form.hide()
        self.ana_form.showMaximized()

    # --- ARAYÜZ YENİLEME FONKSİYONLARI ---
    def bar_guncelle(self):
        try:
            conn = sqlite3.connect("kutuphane.db")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM kitaplar WHERE durum = 1")
            biten = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM kitaplar")
            toplam = cursor.fetchone()[0]
            conn.close()

            if toplam > 0:
                self.ana_form.progressBar.setMaximum(toplam)
                self.ana_form.progressBar.setValue(biten)
                self.ana_form.progressBar.setFormat(f"Biten: %v / Toplam: %m (%p%)")
            else:
                self.ana_form.progressBar.setValue(0)
                self.ana_form.progressBar.setFormat("Henüz kitap eklenmedi")
        except Exception as e:
            print(f"Bar hatası: {e}")

    def tabloyu_doldur(self):
        # CRUD Formundaki tabloyu doldurur
        try:
            self.crud_form.tableWidget.clearContents()
            conn = sqlite3.connect("kutuphane.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kitaplar")
            kitaplar = cursor.fetchall()
            conn.close()

            self.crud_form.tableWidget.setRowCount(len(kitaplar))

            for satir_indeksi, kitap_verisi in enumerate(kitaplar):
                for sutun_indeksi, hucre_verisi in enumerate(kitap_verisi):
                    if sutun_indeksi == 4:
                        gosterilecek_metin = "Bitti" if hucre_verisi == 1 else "Bitmedi"
                    else:
                        gosterilecek_metin = str(hucre_verisi)

                    item = QTableWidgetItem(gosterilecek_metin)
                    self.crud_form.tableWidget.setItem(satir_indeksi, sutun_indeksi, item)
        except Exception as e:
            print(f"CRUD Tablo hatası: {e}")

    # YENİ: KİTAPLIK FORMUNDAKİ TABLOYU DOLDURACAK FONKSİYON
    def kitaplik_tabloyu_doldur(self):
        try:
            self.kitaplik_form.tableWidget.clearContents()
            conn = sqlite3.connect("kutuphane.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kitaplar")
            kitaplar = cursor.fetchall()
            conn.close()

            self.kitaplik_form.tableWidget.setRowCount(len(kitaplar))

            for satir_indeksi, kitap_verisi in enumerate(kitaplar):
                for sutun_indeksi, hucre_verisi in enumerate(kitap_verisi):
                    if sutun_indeksi == 4:
                        gosterilecek_metin = "Bitti" if hucre_verisi == 1 else "Bitmedi"
                    else:
                        gosterilecek_metin = str(hucre_verisi)

                    item = QTableWidgetItem(gosterilecek_metin)
                    self.kitaplik_form.tableWidget.setItem(satir_indeksi, sutun_indeksi, item)
        except Exception as e:
            print(f"Kitaplık Tablo hatası: {e}")

    # --- CRUD FONKSİYONLARI ---
    def kitap_ekle(self):
        ad = self.crud_form.lineEdit_2.text()
        yazar = self.crud_form.lineEdit_3.text()
        sayfa = self.crud_form.lineEdit_4.text()

        durum = 1 if self.crud_form.radioButton.isChecked() else 0

        if ad != "":
            try:
                conn = sqlite3.connect("kutuphane.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO kitaplar (kitap_adi, yazar, sayfa_sayisi, durum) 
                    VALUES (?, ?, ?, ?)
                """, (ad, yazar, sayfa, durum))
                conn.commit()
                conn.close()

                self.crud_form.lineEdit_2.clear()
                self.crud_form.lineEdit_3.clear()
                self.crud_form.lineEdit_4.clear()
                self.crud_form.radioButton.setChecked(True)

                self.tabloyu_doldur()
                self.bar_guncelle()
                QMessageBox.information(None, "Başarılı", "Kitap başarıyla eklendi.")

            except Exception as e:
                QMessageBox.critical(None, "Hata", f"ekleme hatası: {e}")
        else:
            QMessageBox.warning(None, "Uyarı", "Lütfen eklemek istediğiniz kitabın bilgilerini düzgün şekilde yazın!")

    def kitap_sil(self):
        secili_satir = self.crud_form.tableWidget.currentRow()

        if secili_satir >= 0:
            ad = self.crud_form.tableWidget.item(secili_satir, 1).text()
            try:
                conn = sqlite3.connect("kutuphane.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM kitaplar WHERE kitap_adi = ?", (ad,))
                conn.commit()
                conn.close()

                self.tabloyu_doldur()
                self.bar_guncelle()
                QMessageBox.information(self.crud_form, "Başarılı", "Kitap başarıyla silindi.")
            except Exception as e:
                QMessageBox.critical(self.crud_form, "Hata", f"Silme hatası: {e}")
        else:
            QMessageBox.warning(self.crud_form, "Uyarı", "Lütfen silmek istediğiniz kitabı tablodan seçin!")

    def kitap_guncelle(self):
        secili_satir = self.crud_form.tableWidget.currentRow()

        if secili_satir >= 0:
            hucre = self.crud_form.tableWidget.item(secili_satir, 1)
            if hucre is None:
                QMessageBox.warning(None, "Uyarı", "Geçersiz veya boş bir satır seçtiniz!")
                return

            hedef_kitap_adi = hucre.text()

            yeni_ad = self.crud_form.lineEdit_2.text()
            yeni_yazar = self.crud_form.lineEdit_3.text()
            yeni_sayfa = self.crud_form.lineEdit_4.text()


            yeni_durum = 1 if self.crud_form.radioButton.isChecked() else 0


            eski_yazar = self.crud_form.tableWidget.item(secili_satir, 2).text()
            eski_sayfa = self.crud_form.tableWidget.item(secili_satir, 3).text()


            guncel_ad = yeni_ad if yeni_ad != "" else hedef_kitap_adi
            guncel_yazar = yeni_yazar if yeni_yazar != "" else eski_yazar
            guncel_sayfa = yeni_sayfa if yeni_sayfa != "" else eski_sayfa

            try:
                conn = sqlite3.connect("kutuphane.db")
                cursor = conn.cursor()


                cursor.execute("""
                    UPDATE kitaplar 
                    SET kitap_adi = ?, yazar = ?, sayfa_sayisi = ?, durum = ? 
                    WHERE kitap_adi = ?
                """, (guncel_ad, guncel_yazar, guncel_sayfa, yeni_durum, hedef_kitap_adi))

                etkilenen_satir = cursor.rowcount
                conn.commit()
                conn.close()

                if etkilenen_satir > 0:
                    self.tabloyu_doldur()
                    self.bar_guncelle()

                    self.crud_form.lineEdit_2.clear()
                    self.crud_form.lineEdit_3.clear()
                    self.crud_form.lineEdit_4.clear()
                    self.crud_form.radioButton.setChecked(True)

                    QMessageBox.information(None, "Başarılı", "Kitap bilgileri başarıyla güncellendi.")
                else:
                    QMessageBox.warning(None, "Gizli Hata", f"'{hedef_kitap_adi}' isimli kitap bulunamadı!")

            except Exception as e:
                print(f"---- GÜNCELLEME HATASI DETAYI ----\n{e}\n--------------------------------")
                QMessageBox.critical(None, "Hata", f"Güncelleme hatası: {e}")
        else:
            QMessageBox.warning(None, "Uyarı", "Lütfen güncellemek istediğiniz kitabı tablodan seçin!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("faruk.ico"))
    sistem = UygulamaYonetimi()
    sys.exit(app.exec())