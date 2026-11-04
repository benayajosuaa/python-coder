from tkinter import Tk, Canvas
from datetime import datetime
from pathlib import Path

# Fungsi untuk membaca daftar acara dari file teks
def get_events():
    list_events = []
    file_path = Path(__file__).with_name("m11_events.txt")

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            current_event = line.split(",")
            event_date = datetime.strptime(
                current_event[1].strip(), "%d/%m/%y"
            ).date()
            current_event[1] = event_date
            list_events.append(current_event)

    return list_events

# Fungsi untuk menghitung selisih hari antara dua tanggal
def days_between_dates(date1, date2):
    return (date1 - date2).days

def main():
    # Fungsi untuk memperbarui tanggal dan jam secara otomatis
    def update_clock():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")

        c.itemconfig(
            clock_text,
            text=f"Date: {current_date}\nTime: {current_time}"
        )

        # Memperbarui jam setiap satu detik
        root.after(1000, update_clock)

    # Membuat jendela utama aplikasi
    root = Tk()
    root.title("My Countdown Calendar")

    # Membuat tampilan kalender dengan latar belakang hijau
    c = Canvas(root, width=800, height=500, bg="green")
    c.pack()

    # Menampilkan judul kalender
    c.create_text(
        100, 50,
        anchor="w",
        fill="orange",
        font=("Arial", 28, "bold", "underline"),
        text="My Countdown Calendar"
    )

    # Mengambil daftar acara dari file teks
    events = get_events()

    # Mengambil tanggal hari ini
    today = datetime.now().date()

    # Mengatur posisi awal teks
    vertical_space = 100

    # Mengurutkan acara berdasarkan tanggal
    events.sort(key=lambda x: x[1])

    # Menghitung dan menampilkan sisa hari setiap acara
    for event in events:
        event_name = event[0]
        days_until = days_between_dates(event[1], today)

        display = f"It is {days_until} days until {event_name}"

        # Mengubah warna teks berdasarkan sisa hari
        if days_until <= 7:
            text_col = "red"
        else:
            text_col = "lightblue"

        # Menampilkan informasi acara pada kalender
        c.create_text(
            100, vertical_space,
            anchor="w",
            fill=text_col,
            font=("Arial", 28, "bold"),
            text=display
        )

        # Mengatur jarak antar acara
        vertical_space += 40

    # Membuat tampilan tanggal dan jam
    clock_text = c.create_text(
        750, 400,
        anchor="e",
        fill="white",
        font=("Arial", 18, "bold")
    )

    # Menjalankan pembaruan jam
    update_clock()

    # Menjalankan aplikasi
    root.mainloop()


if __name__ == "__main__":
    main()
