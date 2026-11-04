"""Final Project 3 - Pig Pet: peliharaan interaktif menggunakan Tkinter."""
from tkinter import Tk, Canvas, NORMAL, HIDDEN

root = Tk()
root.title("Pig Pet")
root.resizable(False, False)
c = Canvas(root, width=400, height=400, bg="lightpink", highlightthickness=0)
c.pack()

# Membuat telinga, kepala, dan hiasan kupu-kupu pada babi.
c.create_polygon(80, 85, 80, 42, 133, 63, fill="lightcoral", outline="black")
c.create_polygon(320, 85, 320, 42, 267, 63, fill="lightcoral", outline="black")
c.create_oval(35, 20, 365, 350, fill="#FF7D85", outline="#FF7D85")
c.create_polygon(150, 328, 195, 348, 150, 370, fill="purple", outline="black")
c.create_polygon(250, 328, 205, 348, 250, 370, fill="purple", outline="black")
c.create_oval(189, 342, 211, 354, fill="black", outline="black")

# Membuat hidung babi dan mata sederhana.
c.create_rectangle(160, 112, 240, 153, fill="black", outline="black")
left_eye = c.create_oval(171, 123, 189, 141, fill="white", outline="white")
right_eye = c.create_oval(211, 123, 229, 141, fill="white", outline="white")

# Membuat mulut normal, senang, sedih, dan lidah.
mouth_normal = c.create_line(170, 259, 200, 275, 230, 259, smooth=True, width=2)
mouth_happy = c.create_line(160, 253, 200, 292, 240, 253, smooth=True, width=3, state=HIDDEN)
mouth_sad = c.create_line(170, 275, 200, 255, 230, 275, smooth=True, width=2, state=HIDDEN)
tongue = c.create_oval(185, 276, 215, 301, fill="red", outline="red", state=HIDDEN)
cheek_left = c.create_oval(91, 198, 132, 229, fill="pink", outline="pink", state=HIDDEN)
cheek_right = c.create_oval(268, 198, 309, 229, fill="pink", outline="pink", state=HIDDEN)

# Menyimpan status pet dan ID timer agar tidak saling bertabrakan.
inside = False
cheeky = False
sad_timer = None
cheeky_timer = None
eyes_closed = False


def set_face(face):
    # Menyembunyikan semua ekspresi, kemudian menampilkan yang dipilih.
    for item in (mouth_normal, mouth_happy, mouth_sad, tongue,
                 cheek_left, cheek_right):
        c.itemconfigure(item, state=HIDDEN)
    if face == "normal":
        c.itemconfigure(mouth_normal, state=NORMAL)
    elif face == "happy":
        for item in (mouth_happy, cheek_left, cheek_right):
            c.itemconfigure(item, state=NORMAL)
    elif face == "cheeky":
        for item in (mouth_happy, tongue, cheek_left, cheek_right):
            c.itemconfigure(item, state=NORMAL)
    elif face == "sad":
        c.itemconfigure(mouth_sad, state=NORMAL)


def toggle_eyes():
    # Mengubah warna mata untuk menciptakan efek berkedip.
    global eyes_closed
    eyes_closed = not eyes_closed
    color = "black" if eyes_closed else "white"
    c.itemconfigure(left_eye, fill=color, outline=color)
    c.itemconfigure(right_eye, fill=color, outline=color)


def blink():
    # Mata menutup sebentar lalu terbuka lagi setiap tiga detik.
    toggle_eyes()
    root.after(250, toggle_eyes)
    root.after(3000, blink)


def cancel_sad():
    global sad_timer
    if sad_timer is not None:
        root.after_cancel(sad_timer)
        sad_timer = None


def show_sad():
    global sad_timer
    sad_timer = None
    if not inside and not cheeky:
        set_face("sad")


def start_sad_timer():
    global sad_timer
    cancel_sad()
    sad_timer = root.after(4000, show_sad)


def on_motion(event):
    # Saat mouse berada di kanvas, pet tersenyum dan pipinya memerah.
    global inside
    inside = True
    cancel_sad()
    if not cheeky:
        set_face("happy")


def on_leave(event):
    # Saat mouse keluar, ekspresi normal dan hitungan sedih dimulai.
    global inside
    inside = False
    if not cheeky:
        set_face("normal")
    start_sad_timer()


def finish_cheeky():
    global cheeky, cheeky_timer
    cheeky_timer = None
    cheeky = False
    set_face("happy" if inside else "normal")
    if not inside:
        start_sad_timer()


def on_double_click(event):
    # Saat double-click, pet menjulurkan lidah selama satu detik.
    global cheeky, cheeky_timer, inside
    inside = True
    cancel_sad()
    if cheeky_timer is not None:
        root.after_cancel(cheeky_timer)
    cheeky = True
    set_face("cheeky")
    cheeky_timer = root.after(1000, finish_cheeky)


# Menghubungkan event mouse dengan reaksi peliharaan.
c.bind("<Motion>", on_motion)
c.bind("<Leave>", on_leave)
c.bind("<Double-Button-1>", on_double_click)
root.after(1000, blink)
start_sad_timer()
root.mainloop()
