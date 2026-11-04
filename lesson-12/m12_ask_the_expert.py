# MODULE 12 - ASK THE EXPERT ####

from tkinter import Tk, Toplevel, messagebox, font, Label, Entry, Button
from pathlib import Path

# Membuat dictionary kosong untuk menyimpan data negara
the_world = {}

# Menentukan lokasi file data negara
data_file = Path(__file__).with_name("m12_capital_data.txt")


# STEP 3 & 4
# Fungsi untuk membuat jendela input pengguna
def custom_askstring(title, prompt, dialog_size="450x150",
                     bg_color="lightblue", font_size=12,
                     font_weight="bold"):

    # Membuat jendela dialog baru
    dialog = Toplevel(root)
    dialog.title(title)
    dialog.configure(bg=bg_color)
    dialog.geometry(dialog_size)

    # Membuat jenis dan ukuran font
    custom_font = font.Font(size=font_size, weight=font_weight)

    # Menampilkan pertanyaan pada dialog
    label = Label(dialog, text=prompt, bg=bg_color)
    label.configure(font=custom_font)
    label.pack(pady=10)

    # Membuat kolom untuk memasukkan jawaban
    entry = Entry(dialog, font=custom_font)
    entry.pack()
    entry.focus_set()

    # Menyimpan hasil input sementara
    result = {"value": ""}

    # Fungsi ketika tombol OK ditekan
    def ok():
        result["value"] = entry.get()
        dialog.destroy()

    # Membuat tombol OK
    button = Button(
        dialog,
        text="OK",
        command=ok,
        bg=bg_color,
        font=custom_font
    )
    button.pack(pady=5)

    # Memungkinkan pengguna menekan Enter
    entry.bind("<Return>", lambda event: ok())

    # Menutup dialog ketika tombol X ditekan
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    # Menunggu hingga pengguna menutup dialog
    dialog.grab_set()
    root.wait_window(dialog)

    # Mengembalikan hasil input pengguna
    return result["value"]


# STEP 5
# Fungsi untuk membaca data negara dari file TXT
def read_from_file():

    # Membuka file yang berisi daftar negara dan ibu kota
    with open(data_file, "r", encoding="utf-8") as file:

        # Membaca setiap baris dalam file
        for line in file:

            # Menghapus spasi dan karakter baris baru
            line = line.strip()

            # Melewati baris yang kosong
            if not line:
                continue

            # Memisahkan negara dan ibu kota berdasarkan tanda /
            country, city = line.split("/", 1)

            # Menyimpan negara dan ibu kota ke dalam dictionary
            the_world[country.strip()] = city.strip()


# STEP 6
# Fungsi untuk menyimpan negara dan ibu kota baru
def write_to_file(country_name, city_name):

    # Membuka file dalam mode append untuk menambahkan data
    with open(data_file, "a", encoding="utf-8") as file:

        # Menambahkan negara dan ibu kota pada baris baru
        file.write("\n" + country_name + "/" + city_name)


def main():
    global root
    print("Ask the Expert - Capital Cities of the World")
    read_from_file()
    root = Tk()
    root.withdraw()

    # PROGRAM UTAMA
    # Menjalankan program secara berulang
    while True:

        # Meminta pengguna memasukkan nama negara
        query_country_input = custom_askstring(
            "Country",
            "Type the name of a country:",
            dialog_size="450x150",
            bg_color="lightgreen",
            font_size=14
        )

        # Memeriksa apakah pengguna memasukkan nama negara
        if query_country_input.strip():

            # Merapikan input pengguna
            query_country = query_country_input.strip()

            # Mencari negara tanpa membedakan huruf besar dan kecil
            matched_country = next(
                (
                    country for country in the_world
                    if country.casefold() == query_country.casefold()
                ),
                None
            )

            # Jika negara sudah terdaftar dalam dictionary
            if matched_country is not None:

                # Mengambil nama ibu kota dari dictionary
                result = the_world[matched_country]

                # Menampilkan jawaban ibu kota negara
                messagebox.showinfo(
                    "Answer",
                    "The capital city of " + matched_country
                    + " is " + result + "!"
                )

            # Jika negara belum terdaftar dalam dictionary
            else:

                # Meminta pengguna memasukkan nama ibu kota
                new_city = custom_askstring(
                    "Teach me",
                    "I don't know! What is the capital city of "
                    + query_country + "?",
                    dialog_size="550x150",
                    bg_color="lightblue",
                    font_size=12
                )

                # Memeriksa apakah nama ibu kota sudah diisi
                if new_city.strip():

                    # Menyimpan data baru ke dalam dictionary
                    the_world[query_country] = new_city.strip()

                    # Menyimpan data negara baru ke file TXT
                    write_to_file(query_country, new_city.strip())

                    # Memberikan informasi bahwa data berhasil disimpan
                    messagebox.showinfo(
                        "Success",
                        "Thank you! I have learned that the capital city of "
                        + query_country + " is " + new_city.strip() + "!"
                    )

        # Menghentikan program jika pengguna menutup dialog
        else:
            break


    # Menutup jendela utama setelah program selesai
    root.destroy()


if __name__ == "__main__":
    main()
