# QUESTION 2

# Meminta pengguna memasukkan usia
age = int(input("Enter your age: "))

# Mengelompokkan usia berdasarkan kategori umur
if 13 <= age < 18:
    print("You belong to the Teenager category.")
elif age >= 18 and age <= 30:
    print("You belong to the Young Adult category.")
else:
    print("You belong to the Adult category.")
