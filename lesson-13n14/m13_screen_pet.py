from tkinter import HIDDEN, NORMAL, Tk, Canvas

# Membuat jendela utama dan kanvas
root = Tk()
root.title("Screen Pet")
c = Canvas(root, width=400, height=400, bg="dark blue", highlightthickness=0)
c.pack()
c.body_color = "SkyBlue1"

# Menggambar tubuh, mata, dan pupil
body = c.create_oval(35, 20, 365, 350, outline=c.body_color, fill=c.body_color)
eye_left = c.create_oval(130, 110, 160, 170, outline="black", fill="white")
eye_right = c.create_oval(230, 110, 260, 170, outline="black", fill="white")
pupil_left = c.create_oval(140, 145, 150, 155, outline="black", fill="black")
pupil_right = c.create_oval(240, 145, 250, 155, outline="black", fill="black")

# Membuat tiga ekspresi mulut
mouth_normal = c.create_line(170, 250, 200, 272, 230, 250, smooth=1, width=2, state=NORMAL)
mouth_happy = c.create_line(170, 250, 200, 282, 230, 250, smooth=1, width=2, state=HIDDEN)
mouth_sad = c.create_line(170, 250, 200, 232, 230, 250, smooth=1, width=2, state=HIDDEN)

# Membuat lidah dan pipi merah muda
tongue_main = c.create_rectangle(170, 250, 230, 290, outline="red", fill="red", state=HIDDEN)
tongue_tip = c.create_oval(170, 285, 230, 300, outline="red", fill="red", state=HIDDEN)
cheek_left = c.create_oval(70, 180, 120, 230, outline="pink", fill="pink", state=HIDDEN)
cheek_right = c.create_oval(280, 180, 330, 230, outline="pink", fill="pink", state=HIDDEN)

# Menyimpan status pet dan ID penjadwalan animasi
c.happy_level = 1
c.tongue_out = False
c.eyes_crossed = False
c.expression = "normal"
c.mouse_inside = False
idle_job = None
cheeky_job = None


def set_expression(expression):
    """Menampilkan satu ekspresi tanpa menumpuk gambar wajah."""
    c.expression = expression
    for item in (mouth_normal, mouth_happy, mouth_sad, cheek_left, cheek_right):
        c.itemconfigure(item, state=HIDDEN)
    if expression == "normal":
        c.itemconfigure(mouth_normal, state=NORMAL)
    elif expression == "happy":
        c.itemconfigure(mouth_happy, state=NORMAL)
        c.itemconfigure(cheek_left, state=NORMAL)
        c.itemconfigure(cheek_right, state=NORMAL)
    elif expression == "sad":
        c.itemconfigure(mouth_sad, state=NORMAL)
    elif expression == "cheeky":
        c.itemconfigure(cheek_left, state=NORMAL)
        c.itemconfigure(cheek_right, state=NORMAL)


def toggle_eyes():
    # Mengganti warna mata dan menyembunyikan/menampilkan pupil saat berkedip
    closed = c.itemcget(eye_left, "fill") == c.body_color
    color = "white" if closed else c.body_color
    pupil_state = NORMAL if closed else HIDDEN
    c.itemconfigure(eye_left, fill=color)
    c.itemconfigure(eye_right, fill=color)
    c.itemconfigure(pupil_left, state=pupil_state)
    c.itemconfigure(pupil_right, state=pupil_state)


def blink():
    # Mata tertutup 250 ms, lalu berkedip lagi setiap 3 detik
    toggle_eyes()
    root.after(250, toggle_eyes)
    root.after(3000, blink)


def toggle_tongue():
    # Lidah keluar dan masuk secara bergantian
    c.tongue_out = not c.tongue_out
    state = NORMAL if c.tongue_out else HIDDEN
    c.itemconfigure(tongue_main, state=state)
    c.itemconfigure(tongue_tip, state=state)


def toggle_pupils():
    # Memindahkan pupil ke tengah, lalu ke posisi semula
    if not c.eyes_crossed:
        c.move(pupil_left, 10, -5)
        c.move(pupil_right, -10, -5)
        c.eyes_crossed = True
    else:
        c.move(pupil_left, -10, 5)
        c.move(pupil_right, 10, 5)
        c.eyes_crossed = False


def reset_cheeky():
    # Mengembalikan lidah dan pupil ke keadaan awal
    global cheeky_job
    cheeky_job = None
    if c.tongue_out:
        toggle_tongue()
    if c.eyes_crossed:
        toggle_pupils()
    set_expression("happy" if c.mouse_inside else "normal")


def schedule_idle():
    # Mengulang hitungan 4 detik sejak interaksi terakhir
    global idle_job
    if idle_job is not None:
        root.after_cancel(idle_job)
    idle_job = root.after(4000, sad)


def sad():
    # Ekspresi sedih ketika tidak ada gerakan mouse selama 4 detik
    global idle_job
    idle_job = None
    if cheeky_job is None:
        c.happy_level = 0
        set_expression("sad")
    else:
        schedule_idle()


def show_happy(event):
    # Ketika kursor bergerak di area wajah, pet menjadi senang
    c.mouse_inside = True
    c.happy_level = 1
    schedule_idle()
    if cheeky_job is None and 20 <= event.x <= 350 and 20 <= event.y <= 350:
        set_expression("happy")


def hide_happy(event):
    # Ketika kursor keluar, ekspresi kembali normal
    c.mouse_inside = False
    if cheeky_job is None:
        set_expression("normal")
    schedule_idle()


def cheeky(event):
    # Double-click membuat lidah keluar dan mata menjadi juling selama 1 detik
    global cheeky_job
    if not (20 <= event.x <= 350 and 20 <= event.y <= 350):
        return
    c.mouse_inside = True
    c.happy_level = 1
    if cheeky_job is not None:
        root.after_cancel(cheeky_job)
    if not c.tongue_out:
        toggle_tongue()
    if not c.eyes_crossed:
        toggle_pupils()
    set_expression("cheeky")
    schedule_idle()
    cheeky_job = root.after(1000, reset_cheeky)


# Menghubungkan fungsi dengan mouse dan memulai animasi
c.bind("<Motion>", show_happy)
c.bind("<Leave>", hide_happy)
c.bind("<Double-Button-1>", cheeky)
root.after(1000, blink)
schedule_idle()
root.mainloop()
