import sqlite3

def veritabani_kur():
    conn = sqlite3.connect("kutuphane.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kitaplar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kitap_adi TEXT NOT NULL,
        yazar TEXT,
        sayfa_sayisi INTEGER,
        durum INTEGER DEFAULT 0 
    )
    """)

    conn.commit()
    conn.close()
    print("Veritabanı ve 'kitaplar' tablosu başarıyla oluşturuldu!")

if __name__ == "__main__":
    veritabani_kur()