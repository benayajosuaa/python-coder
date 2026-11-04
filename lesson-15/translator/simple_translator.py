from pathlib import Path
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox

# Menentukan file tempat menyimpan kosakata
DATA_FILE = Path(__file__).with_name('translator_data.txt')

# Dictionary untuk menyimpan terjemahan Indonesia ke Inggris
translations = {}


def read_from_file():
    # Membaca kosakata yang sudah tersimpan dalam file TXT
    if not DATA_FILE.exists():
        DATA_FILE.write_text('Pinjam/Borrow\nMobil/Car\nRumah/House\nBuku/Book\nSekolah/School\n', encoding='utf-8')
    with DATA_FILE.open('r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if '/' not in line:
                continue
            word, translation = line.split('/', 1)
            if word.strip() and translation.strip():
                translations[word.strip().casefold()] = translation.strip()


def write_to_file(word, translation):
    # Menambahkan kosakata baru di baris berikutnya
    with DATA_FILE.open('a+', encoding='utf-8') as file:
        file.seek(0)
        contents = file.read()
        if contents and not contents.endswith('\n'):
            file.write('\n')
        file.write(f'{word}/{translation}\n')


def custom_askstring(title, prompt, bg_color='lightgreen'):
    # Membuka dialog input untuk pertanyaan dan jawaban
    dialog = Toplevel(root)
    dialog.title(title)
    dialog.geometry('480x170')
    dialog.configure(bg=bg_color)
    dialog.resizable(False, False)
    result = {'value': None}

    Label(dialog, text=prompt, bg=bg_color, font=('Arial', 12, 'bold'),
          wraplength=455).pack(pady=(15, 8))
    entry = Entry(dialog, font=('Arial', 13), width=35)
    entry.pack()
    entry.focus_set()

    def submit():
        result['value'] = entry.get().strip()
        dialog.destroy()

    Button(dialog, text='OK', command=submit, font=('Arial', 11)).pack(pady=10)
    entry.bind('<Return>', lambda event: submit())
    dialog.protocol('WM_DELETE_WINDOW', dialog.destroy)
    dialog.grab_set()
    root.wait_window(dialog)
    return result['value']


def main():
    global root
    root = Tk()
    root.withdraw()

    # Memuat dictionary sebelum memulai program
    read_from_file()

    # Mengulang pertanyaan sampai dialog ditutup atau dibiarkan kosong
    while True:
        word = custom_askstring('Simple Translator', 'Masukkan kata dalam bahasa Indonesia:')
        if not word:
            break

        key = word.casefold()
        if key in translations:
            messagebox.showinfo('Hasil Terjemahan', f'{word} dalam bahasa Inggris adalah {translations[key]}')
        else:
            answer = custom_askstring('Teach me', f'Aku belum tahu! Apa bahasa Inggris dari "{word}"?', 'lightblue')
            if answer:
                translations[key] = answer
                write_to_file(word, answer)
                messagebox.showinfo('Berhasil', f'Terima kasih! {word} = {answer} sudah disimpan.')

    root.destroy()


if __name__ == "__main__":
    main()
