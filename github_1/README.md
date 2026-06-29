# 📚 Dijital Kütüphane Otomasyon Sistemi (Desktop App)

Kişisel kütüphane envanterini ve okuma alışkanlıklarını dijital ortamda profesyonelce yönetmek amacıyla Nesne Yönelimli Programlama (OOP) prensipleri kullanılarak geliştirilmiş modern bir masaüstü uygulamasıdır. 

Bu proje, güçlü bir SQLite veritabanı altyapısını, PySide6 ile tasarlanmış dinamik ve esnek bir kullanıcı arayüzü ile birleştirerek uçtan uca (end-to-end) bir yazılım deneyimi sunar.

---

## ✨ Öne Çıkan Özellikler

* **Dinamik CRUD Operasyonları:** Veritabanı üzerinde anlık olarak kitap ekleme (Create), listeleme (Read), durum güncelleme (Update) ve silme (Delete) işlemleri.
* **Gerçek Zamanlı İlerleme Takibi (Progress Bar):** Kütüphanedeki "Okundu" ve "Okunmadı" durumundaki kitapların oranını hesaplayarak dinamik bir ilerleme çubuğu üzerinden görselleştirme.
* **Responsive (Esnek) Kullanıcı Arayüzü:** Qt Designer'ın Grid Layout mimarisi kullanılarak tasarlanan arayüz, her türlü monitör çözünürlüğünde (Full HD, 4K veya standart laptop ekranları) form bütünlüğünü korur ve tam ekran modunda kusursuz çalışır.
* **"Silent Failure" (Gizli Hata) Koruması:** Veritabanı güncellemelerinde kullanıcı hatalarını (örn: isim sonu boşluk bırakma) yakalayan `rowcount` kontrolleri ve `Try-Except` blokları ile donatılmış güvenli işlem yapısı.
* **Kullanıcı Dostu UX Deneyimi:** İşlem sonrası arayüz bileşenlerinin (TextBox, RadioButton vb.) otomatik sıfırlanması ve anlık bilgilendirme mesajları (QMessageBox).

---

## 🛠️ Kullanılan Teknolojiler ve Mimari

Bu proje geliştirilirken güncel kütüphaneler ve modüler kodlama yaklaşımı benimsenmiştir:

* **Programlama Dili:** Python 3
* **GUI Framework:** PySide6 (Qt for Python)
* **Arayüz Tasarım Aracı:** Qt Designer (`.ui` tabanlı dışarıdan okuma)
* **Veritabanı Yönetimi:** SQLite3 (Gömülü ilişkisel veritabanı)
* **Dağıtım ve Paketleme:** PyInstaller (Bağımsız `.exe` derlemesi)

### 🗄️ Veritabanı Şeması (`kutuphane.db`)
Proje, verileri güvenli bir şekilde saklamak için basit ancak etkili bir tablo yapısı kullanır:
| Sütun Adı | Veri Tipi | Açıklama |
| :--- | :--- | :--- |
| `kitap_adi` | TEXT | Kitabın tam adı (Birincil arama anahtarı) |
| `yazar` | TEXT | Yazarın adı ve soyadı |
| `sayfa_sayisi` | INTEGER | Kitabın toplam sayfa sayısı |
| `durum` | INTEGER | `1` (Okundu) veya `0` (Okunmadı) |

---

## 🚀 Kurulum ve Geliştirici Yönergeleri

Eğer kaynak kodlarını incelemek veya projeyi kendi ortamınızda geliştirmek isterseniz aşağıdaki adımları izleyebilirsiniz:

**1. Repoyu Klonlayın:**
```bash
git clone [https://github.com/KULLANICI_ADIN/dijital-kutuphane.git](https://github.com/farukksimsek/dijital-kutuphane.git)
cd dijital-kutuphane
2. Gerekli Kütüphaneleri Yükleyin:
Projeyi çalıştırmak için PySide6 paketine ihtiyacınız bulunmaktadır.

Bash
pip install PySide6
3. Uygulamayı Başlatın:

Bash
python main.py
(Not: Uygulamanın çalışması için splash.ui, anaekran.ui, crud.ui ve kitaplik.ui dosyalarının main.py ile aynı dizinde bulunduğundan emin olun.)

👨‍💻 Geliştirici Hakkında
Faruk Küçükşimşek
Niğde Ömer Halisdemir Üniversitesi
Bilgisayar ve Bilişim Bilimleri Fakültesi (BBBF) - Bilişim Sistemleri ve Teknolojileri

Portfolyo & İletişim: farukkucuksimsek.com

Bu proje, masaüstü yazılım geliştirme ve veritabanı entegrasyonu konularındaki yetkinliklerimi pratik etmek amacıyla açık kaynak olarak geliştirilmiştir.