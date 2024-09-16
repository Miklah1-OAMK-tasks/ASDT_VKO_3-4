import tkinter as tk
import random
from PIL import Image, ImageTk
import pygame  # Äänien toistamiseen
import threading  # Säikeet

# Aloita pygame
pygame.mixer.init()

# Lataa osumaääni
osuma_aani = "aaniefektit/splat.wav"  # Äänen tiedostopolku

# Luo pääikkuna
root = tk.Tk()
root.title("Tomaatin heitto")
root.geometry("1400x1200")
root.configure(bg='white')

# Lataa kuvat
ernesti_img = ImageTk.PhotoImage(Image.open("kuvat/erne.png"))
kernesti_img = ImageTk.PhotoImage(Image.open("kuvat/kerne.png"))
maalitaulu_img = ImageTk.PhotoImage(Image.open("kuvat/maalitaulu.png"))
tomaatti_img = ImageTk.PhotoImage(Image.open("kuvat/tomaatti.png"))
osuma_img = ImageTk.PhotoImage(Image.open("kuvat/splat.png"))

# Canvas, johon kuvat sijoitetaan
canvas = tk.Canvas(root, width=1200, height=1000, bg='white', highlightthickness=0)
canvas.pack(pady=20)

# Sijoita maalitaulu keskelle
maalitaulu = canvas.create_image(600, 500, image=maalitaulu_img)

# Osumat tallentava sanakirja
osumat_sanakirja = {
    "ernesti_osumat": 0,
    "kernesti_osumat": 0,
    "yhteensa": 0
}

# Tulostaulu maalitaulun päälle
def luo_tulostaulu():
    global tulostaulu_text
    tulostaulu_text = tk.StringVar()
    tulostaulu_text.set(f"Kernesti: {osumat_sanakirja['kernesti_osumat']}  Ernesti: {osumat_sanakirja['ernesti_osumat']}")
    tulostaulu = tk.Label(root, textvariable=tulostaulu_text, bg='white', font=("Helvetica", 16, "bold"))
    tulostaulu.pack()

luo_tulostaulu()

# Luo satunnaiset sijainnit Ernestille ja Kernestille
ernesti = canvas.create_image(1100, random.randint(100, 900), image=ernesti_img)
kernesti = canvas.create_image(100, random.randint(100, 900), image=kernesti_img)

# Päivitä osumat sanakirjaan
def paivita_osumat(heittaja):
    if heittaja == "ernesti":
        osumat_sanakirja["ernesti_osumat"] += 1
    elif heittaja == "kernesti":
        osumat_sanakirja["kernesti_osumat"] += 1
    osumat_sanakirja["yhteensa"] += 1
    tulostaulu_text.set(f"Kernesti: {osumat_sanakirja['kernesti_osumat']}  Ernesti: {osumat_sanakirja['ernesti_osumat']}")
    print("Päivitetyt osumat:", osumat_sanakirja)

# Heittotoiminto (tomaatti lentää oikealta vasemmalle tai päinvastoin)
def heita_tomaatti(lahtopiste, suunta, heittaja):
    x, y = canvas.coords(lahtopiste)
    
    def animoi():
        nonlocal x
        x += 10 * suunta  # Liikutaan joko oikealle tai vasemmalle
        canvas.coords(tomaatti, x, y)
        
        # Tarkista osuuko tomaatti maalitauluun
        if (600 - 50 <= x <= 600 + 50) and (400 - 160 <= y <= 400 + 160):  # osuma-alue maalitaulun ympärillä
            canvas.delete(tomaatti)
            canvas.create_image(600, 500, image=osuma_img)  # Osumaefekti
            pygame.mixer.Sound(osuma_aani).play()  # Toista osumaääni
            paivita_osumat(heittaja)  # Päivitä osumatiedot sanakirjaan
        elif 0 < x < 1200:  # Tomaatti on yhä canvasin sisällä
            root.after(50, animoi)  # Animaatio jatkuu, kunnes osuma tai ulos ruudulta
        else:
            canvas.delete(tomaatti)  # Poista tomaatti, jos se ylittää canvasin reunat

    # Luo tomaatti ja animaatiotehtävä
    tomaatti = canvas.create_image(x, y, image=tomaatti_img)
    threading.Thread(target=animoi).start()  # Käynnistä animaatio erillisessä säikeessä

# Funktiot, jotka siirtävät Ernestin ja Kernestin satunnaisesti oikeaan tai vasempaan reunaan
def sijoita_ernesti():
    canvas.coords(ernesti, 1100, random.randint(100, 900))  # Oikea reuna

def sijoita_kernesti():
    canvas.coords(kernesti, 100, random.randint(100, 900))  # Vasen reuna

# Painike Ernesti heittää maalitauluun
def heita_ernestilla():
    heita_tomaatti(ernesti, -1, "ernesti")

# Painike Kernesti heittää maalitauluun
def heita_kernestilla():
    heita_tomaatti(kernesti, 1, "kernesti")

# Resetoi tulokset
def resetoi_tulokset():
    osumat_sanakirja["ernesti_osumat"] = 0
    osumat_sanakirja["kernesti_osumat"] = 0
    osumat_sanakirja["yhteensa"] = 0
    tulostaulu_text.set(f"Ernesti: {osumat_sanakirja['ernesti_osumat']}  Kernesti: {osumat_sanakirja['kernesti_osumat']}")

# Aseta painikkeet tyylillä ja tasaamalla leveydet
button_style = {
    "bg": "#4CAF50",  # Taustaväri
    "fg": "white",  # Tekstin väri
    "font": ("Helvetica", 14, "bold"),
    "activebackground": "#45a049",  # Painikkeen aktivoitu väri
    "activeforeground": "white",
    "padx": 20,  # Lisätään tyhjää tilaa sivuille
    "pady": 10,  # Lisätään tyhjää tilaa ylös ja alas
    "width": 10  # Asetetaan painikkeille vakio leveys
}

# Luo kehykset Ernestin ja Kernestin painikkeille
ernesti_frame = tk.Frame(root, bg='white')  # Kehys Ernestin painikkeille
ernesti_frame.pack(side=tk.RIGHT, padx=40, pady=20)

kernesti_frame = tk.Frame(root, bg='white')  # Kehys Kernestin painikkeille
kernesti_frame.pack(side=tk.LEFT, padx=40, pady=20)

# Heittopainikkeet
heita_ernesti_btn = tk.Button(root, text="Heitä Ernestiltä", command=heita_ernestilla, **button_style)
heita_ernesti_btn.pack(side=tk.RIGHT, padx=20, pady=20)

heita_kernesti_btn = tk.Button(root, text="Heitä Kernestiltä", command=heita_kernestilla, **button_style)
heita_kernesti_btn.pack(side=tk.LEFT, padx=20, pady=20)

# Lisää painikkeet, jotka sijoittavat Ernestin ja Kernestin satunnaisesti
sijoita_ernesti_btn = tk.Button(root, text="Sijoita Ernesti", command=sijoita_ernesti, **button_style)
sijoita_ernesti_btn.pack(side=tk.RIGHT, padx=20, pady=20)

sijoita_kernesti_btn = tk.Button(root, text="Sijoita Kernesti", command=sijoita_kernesti, **button_style)
sijoita_kernesti_btn.pack(side=tk.LEFT, padx=20, pady=20)

# Lisää reset-painike tulostaulun alle
resetoi_btn = tk.Button(root, text="Resetoi", command=resetoi_tulokset, **button_style)
resetoi_btn.pack(pady=20)

# Käynnistä ohjelma
root.mainloop()
