import streamlit as st
import pandas as pd
import os

FILE_PATH = "data_siswa.csv"

# Fungsi untuk memuat data
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["NIS", "Nama", "Jenis Kelamin", "Matematika", "Indonesia", "IPA", "IPS"])

# Fungsi untuk menyimpan data
def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# Fungsi untuk menambahkan siswa
def add_student(*args):
    df = load_data()
    nis = args[0]
    if nis in df["NIS"].astype(str).values:
        st.warning("NIS sudah terdaftar!")
        return
    new_data = pd.DataFrame([args], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    st.success("Data siswa berhasil ditambahkan!")

# Fungsi untuk mengedit siswa
def update_student(nis, column, value):
    df = load_data()
    df.loc[df["NIS"] == nis, column] = value
    save_data(df)
    st.success(f"Data {column} berhasil diubah untuk NIS {nis}.")

# Fungsi untuk menghapus siswa
def delete_student(nis):
    df = load_data()
    df = df[df["NIS"] != nis]
    save_data(df)
    st.success("Data siswa berhasil dihapus!")

# Fungsi untuk mencari siswa
def search_student(keyword):
    df = load_data()
    return df[
        df.get("NIS", pd.Series(dtype=str)).astype(str).str.contains(keyword, na=False) |
        df.get("Nama", pd.Series(dtype=str)).astype(str).str.contains(keyword, case=False, na=False)
    ]

# Fungsi untuk menampilkan nilai maksimum dan minimum
def nilai_maks_min():
    df = load_data()

    if df.empty:
        st.info("Tidak ada data siswa.")
        return

    # Kolom nilai (dalam CSV kamu semuanya diawali dengan "Nilai_")
    nilai_cols = [col for col in df.columns if col.startswith("Nilai_")]

    if not nilai_cols:
        st.warning("Tidak ditemukan kolom nilai.")
        return

    st.subheader("📊 Nilai Tertinggi & Terendah Setiap Mata Pelajaran")
    for col in nilai_cols:
        st.markdown(f"**📝 {col.replace('Nilai_', '').replace('_', ' ')}**")
        st.write(f"- 🔼 Tertinggi: {df[col].max()}")
        st.write(f"- 🔽 Terendah : {df[col].min()}")

# UI Streamlit
st.title("📚 Aplikasi Data Siswa")

st.markdown("Selamat datang di aplikasi pengelolaan data siswa.")
st.info("Gunakan menu di sebelah kiri untuk menambah, melihat, atau mengelola data siswa,dan bisa klik pada bagian kolom untuk mengurutkan data.")
st.caption("Data disimpan secara lokal di file `data_siswa.csv`.")
st.caption("create by Sandi Winata I-2310247")
menu = st.sidebar.selectbox("Menu", ["Lihat Data", "Tambah Data", "Edit Data", "Hapus Data", "Cari Siswa", "Nilai Max/Min"])

# Menu Lihat
if menu == "Lihat Data":
    st.subheader("📋 Semua Data Siswa")
    st.dataframe(load_data())

# Menu Tambah
elif menu == "Tambah Data":
    st.subheader("➕ Tambah Data Siswa")
    nis = st.text_input("NIS")
    nama = st.text_input("Nama Lengkap")
    jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    tgl_lahir = st.date_input("Tanggal Lahir")
    kelas = st.selectbox("Kelas", ["X", "XI", "XII"])
    jurusan = st.text_input("Jurusan")
    alamat = st.text_area("Alamat")
    telepon = st.text_input("Nomor Telepon Wali")
    mat = st.number_input("Nilai Matematika", 0, 100)
    indo = st.number_input("Nilai Bahasa Indonesia", 0, 100)
    ipa = st.number_input("Nilai IPA", 0, 100)
    ips = st.number_input("Nilai IPS", 0, 100)
    if st.button("Simpan"):
        add_student(nis, nama, jk, str(tgl_lahir), kelas, jurusan, alamat, telepon, mat, indo, ipa, ips)

# Menu Edit
elif menu == "Edit Data":
    st.subheader("✏️ Edit Data Siswa")
    df = load_data()
    nis_list = df["NIS"].tolist()
    nis_edit = st.selectbox("Pilih NIS", nis_list)
    if nis_edit:
        selected_col = st.selectbox("Kolom yang diubah", ["Nama", "Jenis_Kelamin", "Matematika", "Bhs_Indonesia", "IPA", "IPS"])
        new_value = st.text_input("Nilai Baru") if selected_col in ["Nama", "Jenis_Kelamin"] else st.number_input("Nilai Baru", 0, 100)
        if st.button("Update"):
            update_student(nis_edit, selected_col, new_value)

# Menu Hapus
elif menu == "Hapus Data":
    st.subheader("🗑️ Hapus Data Siswa")
    nis = st.text_input("Masukkan NIS yang akan dihapus")
    if st.button("Hapus"):
        delete_student(nis)

# Menu Cari
elif menu == "Cari Siswa":
    st.subheader("🔍 Cari Siswa")
    keyword = st.text_input("Masukkan NIS atau Nama")
    if keyword:
        result = search_student(keyword)
        st.dataframe(result)

# Menu Nilai Max/Min
elif menu == "Nilai Max/Min":
    nilai_maks_min()

