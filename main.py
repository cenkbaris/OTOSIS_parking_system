from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import tkinter as Tk
import cv2
import numpy as np
import pytesseract
import imutils
import veritabani
import customtkinter
from PIL import ImageTk, Image
from datetime import datetime, timedelta

customtkinter.set_default_color_theme("blue")

app =customtkinter.CTk()
app.title('otopark_sistemi')
app.geometry('1200x600')
app.resizable(False,False)

font1 =('Arial',18,'bold')
font2 =('Arial',12,'bold')
font3 =('Arial',25,'bold')

def ana_sayfa():
    ana_frame = customtkinter.CTkFrame(master=app,
                               width=950,
                               height=600,
                               corner_radius=10)
    ana_frame.place(relx=0.60, rely=0.5, anchor=CENTER) 
        
    def arac_plaka_oku_giris():
        pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\cenkb\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

        img = cv2.imread('plaka/3.jpeg')
        if img is None:
            print("Dosya okunamadı.")
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            filtre = cv2.bilateralFilter(gray, 7, 200, 200)
            kose = cv2.Canny(filtre, 40, 200)

            kontur, a = cv2.findContours(kose,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = imutils.grab_contours((kontur, a))
            cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:10]

            ekran = 0

            for i in cnt:
                eps = 0.018*cv2.arcLength(i, True)
                aprx = cv2.approxPolyDP(i, eps, True)
                if len(aprx) == 4:
                    ekran = aprx
                    break

            maske = np.zeros(gray.shape, np.uint8)
            yenimaske = cv2.drawContours(maske,[ekran],0,(255,255,255),-1)
            yazi = cv2.bitwise_and(img,img,mask=maske)

            (x, y) = np.where(maske == 255)
            (ustx, usty) = (np.min(x), np.min(y))
            (altx, alty) = (np.max(x), np.max(y))
            kirp = gray[ustx:altx + 1, usty:alty + 1]
           
            plaka_text = pytesseract.image_to_string(kirp, lang="eng")
            guncel_tarih = datetime.now().strftime("%Y-%m-%d")
            guncel_saat = datetime.now().strftime("%H:%M:%S")
            giris_plaka_entry.delete(0, 'end')
            giris_plaka_entry.insert(0, plaka_text)
            giris_tarih_entry.delete(0,'end')
            giris_tarih_entry.insert(0,guncel_tarih)
            giris_saat_entry.delete(0,'end')
            giris_saat_entry.insert(0,guncel_saat)

            cv2.imshow('Plaka Tanıma',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def arac_plaka_oku_cikis():
        pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\cenkb\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

        img = cv2.imread('plaka/3.jpeg')
        if img is None:
            print("Dosya okunamadı.")
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            filtre = cv2.bilateralFilter(gray, 7, 200, 200)
            kose = cv2.Canny(filtre, 40, 200)

            kontur, a = cv2.findContours(kose,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = imutils.grab_contours((kontur, a))
            cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:10]

            ekran = 0

            for i in cnt:
                eps = 0.018*cv2.arcLength(i, True)
                aprx = cv2.approxPolyDP(i, eps, True)
                if len(aprx) == 4:
                    ekran = aprx
                    break

            maske = np.zeros(gray.shape, np.uint8)
            yenimaske = cv2.drawContours(maske,[ekran],0,(255,255,255),-1)
            yazi = cv2.bitwise_and(img,img,mask=maske)

            (x, y) = np.where(maske == 255)
            (ustx, usty) = (np.min(x), np.min(y))
            (altx, alty) = (np.max(x), np.max(y))
            kirp = gray[ustx:altx + 1, usty:alty + 1]
           
            plaka_text = pytesseract.image_to_string(kirp, lang="eng")
            guncel_tarih = datetime.now().strftime("%Y-%m-%d")
            guncel_saat = datetime.now().strftime("%H:%M:%S")
            cikis_plaka_entry.delete(0, 'end')
            cikis_plaka_entry.insert(0, plaka_text)
            cikis_tarih_entry.delete(0,'end')
            cikis_tarih_entry.insert(0,guncel_tarih)
            cikis_saat_entry.delete(0,'end')
            cikis_saat_entry.insert(0,guncel_saat)
            fiyat_entry.delete(0,'end')
            fiyat_entry.insert(0,'200')

            cv2.imshow('Plaka Tanıma',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def giris_ekle():
        plaka = giris_plaka_entry.get()
        giris_th = giris_tarih_entry.get()
        giris_st = giris_saat_entry.get()
        giris_no = otopark_no_combo.get()

        if not (plaka and giris_th and giris_st):
            messagebox.showerror('HATA', 'Boş Alan Bırakmayınız.')
        else:
            kayit_varmi, kayit_id = veritabani.kontrol_et(plaka)     
            if kayit_varmi:
                messagebox.showerror('HATA','Plaka Zaten Kayıtlı.')
            else:
                veritabani.ekle_otopark_sistem(plaka, giris_th, giris_st, '', '', giris_no, '')
                messagebox.showinfo('Başarılı', 'Veriler Eklendi.')

            giris_plaka_entry.delete(0, END)
            giris_tarih_entry.delete(0, END)
            giris_saat_entry.delete(0, END)
    
    def cikis_ekle():
        plaka = cikis_plaka_entry.get()
        cikis_th = cikis_tarih_entry.get()
        cikis_st = cikis_saat_entry.get()
        fiyat = fiyat_entry.get()

        if not (plaka and cikis_th and cikis_st and fiyat):
            messagebox.showerror('HATA', 'Boş Alan Bırakmayınız.')
        else:
            kayit_varmi, kayit_id = veritabani.kontrol_et(plaka)

            if kayit_varmi:
                veritabani.guncelle_otopark_sistem(cikis_th, cikis_st, fiyat,plaka)
                messagebox.showinfo('Başarılı', 'Veriler Güncellendi')
            else:
                messagebox.showerror('HATA', 'Giriş yapılmadan çıkış yapılamaz!')
            
            cikis_plaka_entry.delete(0, END)
            cikis_tarih_entry.delete(0, END)
            cikis_saat_entry.delete(0, END)
            fiyat_entry.delete(0, '100')

    giris_kamera_buton = customtkinter.CTkButton(master=ana_frame,command=arac_plaka_oku_giris,font=font3,text='Giriş Kamerası',
                                        cursor='hand2',corner_radius=15,width=200,height=200)
    giris_kamera_buton.place(x=50,y=50)

    giris_plaka_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Plaka:')
    giris_plaka_label.place(x=550,y=100)

    giris_plaka_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    giris_plaka_entry.place(x=650,y=100)

    giris_tarih_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Giriş Tarihi:')
    giris_tarih_label.place(x=550,y=140)

    giris_tarih_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    giris_tarih_entry.place(x=650,y=140)

    giris_saat_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Giriş Saati:')
    giris_saat_label.place(x=550,y=180)

    giris_saat_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    giris_saat_entry.place(x=650,y=180)

    otopark_no_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='otopark no:')
    otopark_no_label.place(x=550,y=220)
    def degerler():
        veriler = [veri[0] for veri in veritabani.bos_otopark()]

        degerler1 = ["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5"]

        yeni_degerler = [deger for deger in degerler1 if deger not in veriler]
        return yeni_degerler

    degerler() 
    otopark_no_combo = customtkinter.CTkComboBox(master=ana_frame,border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150,values=degerler())
    otopark_no_combo.place(x=650,y=220)

    giris_kaydet_buton = customtkinter.CTkButton(master=ana_frame,font=font1,command=giris_ekle,
                                        text='Giriş Yap',fg_color='#05A312',
                                        hover_color='#00850B',cursor='hand2',corner_radius=15,width=60)
    giris_kaydet_buton.place(x=690,y=260)

    cikis_kamera_buton = customtkinter.CTkButton(master=ana_frame,command=arac_plaka_oku_cikis,font=font3,text='Çıkış Kamerası',
                                        cursor='hand2',corner_radius=15,width=200,height=200)
    cikis_kamera_buton.place(x=50,y=330)

    cikis_plaka_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Plaka:')
    cikis_plaka_label.place(x=550,y=380)

    cikis_plaka_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    cikis_plaka_entry.place(x=650,y=380)

    cikis_tarih_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Çıkıs Tarihi:')
    cikis_tarih_label.place(x=550,y=420)

    cikis_tarih_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    cikis_tarih_entry.place(x=650,y=420)

    cikis_saat_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Çıkış Saati:')
    cikis_saat_label.place(x=550,y=460)

    cikis_saat_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    cikis_saat_entry.place(x=650,y=460)

    fiyat_label = customtkinter.CTkLabel(master=ana_frame,font=font1,text='Fiyat :')
    fiyat_label.place(x=550,y=500)

    fiyat_entry = customtkinter.CTkEntry(master=ana_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    fiyat_entry.place(x=650,y=500)

    cikis_kaydet_buton = customtkinter.CTkButton(master=ana_frame,command=cikis_ekle,font=font1,
                                        text='Çıkış Yap',fg_color='#E40404',
                                        hover_color='dark red',cursor='hand2',corner_radius=15,width=60)
    cikis_kaydet_buton.place(x=690,y=540)
    
def liste():
    list_frame = customtkinter.CTkFrame(master=app,
                               width=950,
                               height=600,
                               corner_radius=10)
    list_frame.place(relx=0.60, rely=0.5, anchor=CENTER)

    def add_to_treeview():
        otopark_sistem=veritabani.getir_otopark_sistem()
        tree.delete(*tree.get_children())
        for musteri in otopark_sistem:
            tree.insert('', END, values=musteri)

    def temizle(*clicked):       
        if clicked:
            tree.selection_remove(tree.focus())
        id_entry.delete(0, END)
        plaka_entry.delete(0, END)
        giris_th_entry.delete(0, END)
        giris_st_entry.delete(0, END) 
        cikis_th_entry.delete(0, END)
        cikis_st_entry.delete(0, END)
        otopark_numara_entry.delete(0, END)
        fiyat_entry.delete(0, END)

    def verileri_goster(event):
        secilen_oge = tree.focus()
        if secilen_oge:
            row = tree.item(secilen_oge)['values']
            temizle()
            id_entry.insert(0,row[0])
            plaka_entry.insert(0, row[1])
            giris_th_entry.insert(0, row[2])
            giris_st_entry.insert(0, row[3]) 
            cikis_th_entry.insert(0, row[4])
            cikis_st_entry.insert(0, row[5])
            otopark_numara_entry.insert(0, row[6])
            fiyat_entry.insert(0, row[7])
        else:
            pass
            
    def sil():
        secilen_oge = tree.focus()
        if not secilen_oge:
            messagebox.showerror('Hata','Silinicek Bir Veri Seçin')
        else:
            id = id_entry.get()
            veritabani.sil_otopark_sistem(id)
            add_to_treeview()
            temizle()
            messagebox.showinfo('Başarılı','Veri Başarılıyla Silindi')

    def ekle():
        plaka = plaka_entry.get()
        giris_th = giris_th_entry.get()
        giris_st = giris_st_entry.get()
        cikis_th = cikis_th_entry.get()
        cikis_st = cikis_st_entry.get()
        otopark_no = otopark_numara_entry.get()
        fiyat = fiyat_entry.get()
        if not (plaka and giris_th and giris_st and cikis_th and cikis_st and otopark_no and fiyat):
            messagebox.showerror('HATA','Boş Alan Bırakmayınız.')
        else:
            veritabani.ekle_otopark_sistem(plaka,giris_th,giris_st,cikis_th,cikis_st,otopark_no,fiyat)
            add_to_treeview()
            messagebox.showinfo('Başarılı','Veriler Eklendi')
            id_entry.delete(0, END)
            plaka_entry.delete(0, END)
            giris_th_entry.delete(0, END)
            giris_st_entry.delete(0, END) 
            cikis_th_entry.delete(0, END)
            cikis_st_entry.delete(0, END)
            otopark_numara_entry.delete(0, END)
            fiyat_entry.delete(0, END) 
            
    
    #def id_gizle():
        #id_entry.configure(state='disabled')

    id_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='İd:',
                                        corner_radius=10)
    id_label.place(x=20, y=30)
    
    id_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    id_entry.place(x=130,y=30)

    plaka_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Plaka:',
                                        corner_radius=10)
    plaka_label.place(x=20, y=80)

    plaka_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    plaka_entry.place(x=130,y=80)

    giris_th_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Giriş Tarihi:',
                                        corner_radius=10)
    giris_th_label.place(x=20, y=130)

    giris_th_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    giris_th_entry.place(x=130,y=130)

    giris_st_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Giriş Saati:',
                                        corner_radius=10)
    giris_st_label.place(x=20, y=180)

    giris_st_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    giris_st_entry.place(x=130,y=180)

    cikis_th_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Çıkış Tarihi:',
                                        corner_radius=10)
    cikis_th_label.place(x=20, y=230)

    cikis_th_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    cikis_th_entry.place(x=130,y=230)

    cikis_st_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Çıkış Saati:',
                                        corner_radius=10)
    cikis_st_label.place(x=20, y=280)

    cikis_st_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    cikis_st_entry.place(x=130,y=280)
    
    otopark_numara_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Park No:',
                                        corner_radius=10)
    otopark_numara_label.place(x=20, y=330)

    otopark_numara_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    otopark_numara_entry.place(x=130,y=330)

    fiyat_label = customtkinter.CTkLabel(master=list_frame,font=font1,text='Fiyat:',
                                        corner_radius=10)
    fiyat_label.place(x=20, y=380)

    fiyat_entry = customtkinter.CTkEntry(master=list_frame,
                                        border_color='#0c9295',
                                        corner_radius=10,border_width=2,width=150)
    fiyat_entry.place(x=130,y=380)

    ekle_buton = customtkinter.CTkButton(master=list_frame,command=ekle,font=font2,
                                        text='Müşteri Ekle',fg_color='#05A312',
                                        hover_color='#00850B',cursor='hand2',corner_radius=15,width=160)
    ekle_buton.place(x=125,y=430)

    sil_buton = customtkinter.CTkButton(master=list_frame,command=sil,font=font2,
                                        text='Müşteri Sil',fg_color='#E40404',
                                        hover_color='#AE0000',cursor='hand2',corner_radius=15,width=160)
    sil_buton.place(x=125,y=470)

    temizle_buton = customtkinter.CTkButton(master=list_frame,command=lambda:temizle(True),font=font2,
                                        text='Kutuları Temizle',fg_color='#E40404',
                                        hover_color='#AE0000',cursor='hand2',corner_radius=15,width=160)
    temizle_buton.place(x=125,y=510)

    style = ttk.Style(list_frame)

    style.theme_use('clam')
    style.configure('treeview',font=font2,foreground='#fff',background='#000',fieldbackground='#313837')
    style.map('treeview',background=[('selected','#1A8F2D')])

    tree = ttk.Treeview(list_frame, columns=('id', 'plaka', 'giris_tarihi', 'giris_saati', 'cikis_tarihi', 'cikis_saati', 'otopark_numara', 'fiyat'), height=30)


    tree['columns'] = ('id','plaka','giris_tarihi','giris_saati','cikis_tarihi','cikis_saati','otopark_numara','fiyat')

    tree.column('#0', width=0, stretch=Tk.NO)
    tree.column('id', anchor=CENTER, width=60)
    tree.column('plaka', anchor=CENTER, width=110)
    tree.column('giris_tarihi', anchor=CENTER, width=110)
    tree.column('giris_saati', anchor=CENTER, width=110)
    tree.column('cikis_tarihi', anchor=CENTER, width=110)
    tree.column('cikis_saati', anchor=CENTER, width=110)
    tree.column('otopark_numara', anchor=CENTER, width=90)
    tree.column('fiyat', anchor=CENTER, width=80)

    tree.heading('id',text='id')
    tree.heading('plaka',text='plaka')
    tree.heading('giris_tarihi',text='giris_tarihi')
    tree.heading('giris_saati',text='giris_saati')
    tree.heading('cikis_tarihi',text='cikis_tarihi')
    tree.heading('cikis_saati',text='cikis_saati')
    tree.heading('otopark_numara',text='park_no')
    tree.heading('fiyat',text='fiyat')

    tree.place(x=390,y=30)

    tree.bind('<ButtonRelease>' ,verileri_goster)

    #id_gizle()
    add_to_treeview()

def otopark():
    oto_frame = customtkinter.CTkFrame(master=app,
                               width=950,
                               height=600,
                               corner_radius=10)
    oto_frame.place(relx=0.60, rely=0.5, anchor=CENTER)

    def gizle():
        a1_frame.place_forget()
        a2_frame.place_forget()
        a3_frame.place_forget()
        a4_frame.place_forget()
        a5_frame.place_forget()
        b1_frame.place_forget()
        b2_frame.place_forget()
        b3_frame.place_forget()
        b4_frame.place_forget()
        b5_frame.place_forget()

    def otopark_kontrol_et():
        otopark_numaralari = veritabani.cikis_yapanlari_sil()
        gizle()

        for otopark_numarasi in otopark_numaralari:
            otopark_numarasi = otopark_numarasi[0].strip()

            if otopark_numarasi == 'a1':
                a1_frame.place(x=130, y=20)
            elif otopark_numarasi == 'a2':
                a2_frame.place(x=290, y=20)
            elif otopark_numarasi == 'a3':
                a3_frame.place(x=450, y=20)
            elif otopark_numarasi == 'a4':
                a4_frame.place(x=610, y=20)
            elif otopark_numarasi == 'a5':
                a5_frame.place(x=770, y=20)
            elif otopark_numarasi == 'b1':
                b1_frame.place(x=130, y=385)
            elif otopark_numarasi == 'b2':
                b2_frame.place(x=290, y=385)
            elif otopark_numarasi == 'b3':
                b3_frame.place(x=450, y=385)
            elif otopark_numarasi == 'b4':
                b4_frame.place(x=610, y=385)
            elif otopark_numarasi == 'b5':
                b5_frame.place(x=770, y=385)
    

    park_frame1 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame1.place(x=80, y=-10)

    a1_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='A1')
    a1_label.place(x=160,y=30)

    a1_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(a1_frame, image=img)
    image_label.image = img
    image_label.pack()
    
    park_frame2 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame2.place(x=240, y=-10)

    a2_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='A2')
    a2_label.place(x=320,y=30)

    a2_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(a2_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame3 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame3.place(x=400, y=-10)

    a3_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='A3')
    a3_label.place(x=480,y=30)

    a3_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(a3_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame4 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame4.place(x=560, y=-10)

    a4_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='A4')
    a4_label.place(x=640,y=30)

    a4_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(a4_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame5 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame5.place(x=720, y=-10)

    a5_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='A5')
    a5_label.place(x=800,y=30)

    a5_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(a5_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame6 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame6.place(x=880, y=-10)
#alt line
    park_frame7 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame7.place(x=80, y=410)

    b1_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='B1')
    b1_label.place(x=160,y=540)

    b1_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    image = image.rotate(180)
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(b1_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame8 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame8.place(x=240, y=410)

    b2_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='B2')
    b2_label.place(x=320,y=540)

    b2_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    image = image.rotate(180)
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(b2_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame9 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame9.place(x=400, y=410)

    b3_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='B3')
    b3_label.place(x=480,y=540)

    b3_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    image = image.rotate(180)
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(b3_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame10 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame10.place(x=560, y=410)

    b4_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='B4')
    b4_label.place(x=640,y=540)

    b4_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    image = image.rotate(180)

    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(b4_frame, image=img)
    image_label.image = img
    image_label.pack()  

    park_frame11 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame11.place(x=720, y=410)

    b5_label = customtkinter.CTkLabel(master=oto_frame,font=font3,text='B5')
    b5_label.place(x=800,y=540)
    
    b5_frame = customtkinter.CTkFrame(master=oto_frame,width=80,height=200,corner_radius=20)
    image_path = 'araba.png'
    image = Image.open(image_path)
    image = image.resize((100, 250))
    image = image.rotate(180)
    img = ImageTk.PhotoImage(image)
    image_label = Tk.Label(b5_frame, image=img)
    image_label.image = img
    image_label.pack()

    park_frame12 = customtkinter.CTkFrame(master=oto_frame,width=20,height=200,corner_radius=20)
    park_frame12.place(x=880, y=410)

    park_frame_duvar = customtkinter.CTkFrame(master=oto_frame,width=50,height=700)
    park_frame_duvar.place(x=910, y=-10)

    otopark_kontrol_et()
def  mod():
    mod_degis_1 = customtkinter.StringVar(value="ac")
    mod_degis_2 = customtkinter.StringVar(value="kapat")

    def switch_event():
        if mod_degis_1.get() == 'ac' and mod_degis_2.get() == 'kapat':
            customtkinter.set_appearance_mode("System")
        if mod_degis_1.get() == 'kapat'and mod_degis_2.get() == 'kapat':
            customtkinter.set_appearance_mode("dark")

    mod_1 = customtkinter.CTkSwitch(master=frame,font=font2, text="Pencere Modu",command=switch_event,
                                variable=mod_degis_1,onvalue="ac",offvalue="kapat")
    mod_1.place(relx=0.2, rely=0.90)

frame = customtkinter.CTkFrame(master=app,
                               width=220,
                               height=600,
                               corner_radius=10)
frame.place(relx=0.1, rely=0.5, anchor=CENTER)

anasayfa_buton1 = customtkinter.CTkButton(command=ana_sayfa,font=font2,master=frame,
                                        text='Ana Sayfa',
                                        corner_radius=10)
anasayfa_buton1.place(relx=0.2, rely=0.12)

anasayfa_buton2 = customtkinter.CTkButton(command=liste,font=font2,master=frame,
                                        text='Liste',
                                        corner_radius=10)
anasayfa_buton2.place(relx=0.2, rely=0.20)

anasayfa_buton3 = customtkinter.CTkButton(command=otopark,font=font2,master=frame,
                                        text='Otopark',
                                        corner_radius=10)
anasayfa_buton3.place(relx=0.2, rely=0.28)


mod()
app.mainloop()

