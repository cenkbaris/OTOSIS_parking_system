import sqlite3

def tabloyu_olustur():
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otopark_sistem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plaka TEXT,
            giris_tarih TEXT,
            giris_saati TEXT,
            cikis_tarihi TEXT,
            cikis_saati TEXT,
            otopark_numara TEXT,
            fiyat TEXT)''')
    con.commit()
    con.close()

def getir_otopark_sistem():
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM otopark_sistem')
    otopark_sistem = cursor.fetchall()
    con.close()
    return otopark_sistem

def kontrol_et(plaka):
    conn = sqlite3.connect("otopark_sistem.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM otopark_sistem WHERE plaka = ?", (plaka,))
    kayit = cursor.fetchone()
    conn.close()
    return (kayit is not None, kayit[0] if kayit else None)

def ekle_otopark_sistem(plaka,giris_tarih,giris_saati,cikis_tarihi,cikis_saati,otopark_numara,fiyat):
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()
    cursor.execute('INSERT INTO otopark_sistem (plaka,giris_tarih,giris_saati,cikis_tarihi,cikis_saati,otopark_numara,fiyat) VALUES (?,?,?,?,?,?,?)',
                   (plaka,giris_tarih,giris_saati,cikis_tarihi,cikis_saati,otopark_numara,fiyat))
    con.commit()
    con.close()

def bos_otopark():
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()
    cursor.execute('SELECT otopark_sistem.otopark_numara FROM otopark_sistem')
    veriler=cursor.fetchall()
    con.commit()
    con.close()
    return veriler

def cikis_yapanlari_sil():
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()
    cursor.execute('SELECT otopark_sistem.otopark_numara FROM otopark_sistem')
    veriler=cursor.fetchall()
    con.commit()
    con.close()
    return veriler

def sil_otopark_sistem(id):
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()
    cursor.execute('DELETE FROM otopark_sistem WHERE id = ?', (id,))
    con.commit()
    con.close()

def guncelle_otopark_sistem(cikis_th, cikis_st, fiyat, plaka):
    conn = sqlite3.connect("otopark_sistem.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE otopark_sistem SET cikis_tarihi=?, cikis_saati=?, otopark_numara='', fiyat=? WHERE plaka=?", 
                   (cikis_th, cikis_st, fiyat, plaka))
    conn.commit()
    conn.close()

def mevcut_id(id):
    con = sqlite3.connect('otopark_sistem.db')
    cursor = con.cursor()
    cursor.execute('SELECT COUNT(*) FROM otopark_sistem WHERE id = ?', (id,))
    sonuc = cursor.fetchone()
    con.close()
    return sonuc[0] > 0

tabloyu_olustur()
