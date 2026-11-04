"""Project 1 - My Family Birthday Countdown (Tkinter)."""
from datetime import datetime, date
from pathlib import Path
from tkinter import Tk, Canvas

# Mengambil file data dari folder yang sama dengan kode Python.
DATA_FILE = Path(__file__).with_name("birthday_data.txt")


def read_birthdays():
    """Membaca nama dan tanggal lahir anggota keluarga dari TXT."""
    birthdays = []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                name, birthday_text = line.split(",", 1)
                name = name.strip()
                birthday = datetime.strptime(birthday_text.strip(), "%d/%m/%y").date()
                if not name:
                    raise ValueError("Nama tidak boleh kosong")
                birthdays.append((name, birthday))
            except ValueError as exc:
                print(f"Baris {number} dilewati karena format tidak sesuai: {exc}")
    return birthdays


def next_birthday(birthday, today):
    """Menghitung tanggal ulang tahun berikutnya, berulang setiap tahun."""
    # Tanggal 29 Februari dirayakan 28 Februari pada tahun non-kabisat.
    def date_in_year(year):
        try:
            return date(year, birthday.month, birthday.day)
        except ValueError:
            return date(year, 2, 28)

    next_date = date_in_year(today.year)
    if next_date < today:
        next_date = date_in_year(today.year + 1)
    return next_date


# Membuat jendela utama dan canvas.
root = Tk()
root.title("My Family Birthday Countdown")
root.resizable(False, False)
canvas = Canvas(root, width=800, height=500, bg="#FFE5C2", highlightthickness=0)
canvas.pack()

# Menampilkan judul.
canvas.create_text(45, 45, anchor="w", fill="#162A64",
                   font=("Arial", 25, "bold", "underline"),
                   text="My Family Birthday Countdown")

# Menampilkan waktu yang terus diperbarui.
clock_text = canvas.create_text(770, 445, anchor="e", fill="#9B2431",
                                font=("Arial", 13, "bold"), text="")

# Daftar baris teks yang akan di-refresh secara berkala.
line_items = [canvas.create_text(45, 88 + 34 * i, anchor="w",
                                 fill="#146734", font=("Arial", 16, "bold"), text="")
              for i in range(8)]

birthdays = read_birthdays()


def update_display():
    """Memperbarui countdown dan jam setiap satu detik."""
    now = datetime.now()
    today = now.date()
    upcoming = []

    for name, birthday in birthdays:
        event_date = next_birthday(birthday, today)
        days_left = (event_date - today).days
        upcoming.append((days_left, name))

    upcoming.sort(key=lambda item: (item[0], item[1].casefold()))

    for i, item in enumerate(line_items):
        if i >= len(upcoming):
            canvas.itemconfigure(item, text="")
            continue
        days_left, name = upcoming[i]
        if days_left == 0:
            display = f"Today is {name}'s Birthday!"
        elif days_left == 1:
            display = f"It is 1 day until {name}'s Birthday"
        else:
            display = f"It is {days_left} days until {name}'s Birthday"
        canvas.itemconfigure(item, text=display,
                             fill="#D82D30" if days_left <= 7 else "#146734")

    if not birthdays:
        canvas.itemconfigure(line_items[0], text="No birthday data available.")

    canvas.itemconfigure(clock_text,
                         text=now.strftime("Date: %d/%m/%Y\nTime: %H:%M:%S"))
    root.after(1000, update_display)


update_display()
root.mainloop()
