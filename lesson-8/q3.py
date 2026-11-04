# QUESTION 3

# Fungsi untuk menghitung luas segitiga
def calculate_triangle_area(base, height):
    # Menghitung luas segitiga menggunakan alas dan tinggi
    area = (base * height) / 2
    return area

# Fungsi utama program
def main():
    # Menampilkan judul program
    print("Triangle Area Calculation Program")
    print("---------------------------------")

    # Meminta pengguna memasukkan nilai alas dan tinggi segitiga
    base = float(input("Enter the length of the base: "))
    height = float(input("Enter the height: "))

    # Memanggil fungsi untuk menghitung luas segitiga
    area = calculate_triangle_area(base, height)

    # Menampilkan hasil perhitungan luas segitiga
    print("The area of the triangle is", area)

# Menjalankan fungsi utama
main()
