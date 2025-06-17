import streamlit as st
import pandas as pd
import os

FILE_PATH = "data_siswa.csv"

def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["NIS", "Nama", "Matematika", "Bahasa_Indonesia", "IPA", "IPS"])

def save_data(df):
    df.to_csv(FILE_PATH, index=False)

def add_student(nis, nama, mat, bindo, ipa, ips):
    df = load_data()
    if nis in df["NIS"].astype(str).values:
        st.warning("NIS sudah terdaftar!")
        return
    new_data = pd.DataFrame([[nis, nama, mat, bindo, ipa, ips]],
                            columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    st.success("Data siswa berhasil ditambahkan!")

def update_student(nis, column, value):
    df = load_data()
    df.loc[df["NIS"] == nis, column] = value
    save_data(df)
    st.success(f"Data {column} berhasil diubah untuk NIS {nis}.")

def delete_student(nis):
    df = load_data()
    df = df[df["NIS"] != nis]
    save_data(df)
    st.success("Data siswa berhasil dihapus!")

def search_student(keyword):
    df = load_data()
    return df[df["NIS"].astype(str).str.contains(keyword) | df["Nama"].str.contains(keyword, case=False)]

def nilai_maks_min():
    df = load_data()
    subjects = ["Matematika", "Bahasa_Indonesia", "IPA", "IPS"]
    st.subheader("📊 Nilai Tertinggi & Terendah")
    for subject in subjects:
        if not df.empty:
            st.write(f"**{subject}**")
            st.write(f"- Tertinggi: {df[subject].max()}")
            st.write(f"- Terendah : {df[subject].min()}")

# Streamlit UI
st.title("📚 Aplikasi Data Siswa (CRUD + Pencarian + Statistik)")
menu = st.sidebar.selectbox("Menu", ["Lihat Data", "Tambah Data", "Edit Data", "Hapus Data", "Cari Siswa", "Nilai Max/Min"])

if menu == "Lihat Data":
    st.subheader("📋 Semua Data Siswa")
    st.dataframe(load_data())

elif menu == "Tambah Data":
    st.subheader("➕ Tambah Data Siswa")
    nis = st.text_input("NIS")
    nama = st.text_input("Nama")
    mat = st.number_input("Matematika", 0, 100)
    bindo = st.number_input("Bahasa Indonesia", 0, 100)
    ipa = st.number_input("IPA", 0, 100)
    ips = st.number_input("IPS", 0, 100)
    if st.button("Simpan"):
        add_student(nis, nama, mat, bindo, ipa, ips)

elif menu == "Edit Data":
    st.subheader("✏️ Edit Data Siswa")
    df = load_data()
    nis_list = df["NIS"].tolist()
    nis_edit = st.selectbox("Pilih NIS", nis_list)
    if nis_edit:
        selected_col = st.selectbox("Kolom yang diubah", ["Nama", "Matematika", "Bahasa_Indonesia", "IPA", "IPS"])
        new_value = st.text_input("Nilai Baru") if selected_col == "Nama" else st.number_input("Nilai Baru", 0, 100)
        if st.button("Update"):
            update_student(nis_edit, selected_col, new_value)

elif menu == "Hapus Data":
    st.subheader("🗑️ Hapus Data Siswa")
    nis = st.text_input("Masukkan NIS yang akan dihapus")
    if st.button("Hapus"):
        delete_student(nis)

elif menu == "Cari Siswa":
    st.subheader("🔍 Cari Siswa")
    keyword = st.text_input("Masukkan NIS atau Nama")
    if keyword:
        result = search_student(keyword)
        st.dataframe(result)

elif menu == "Nilai Max/Min":
    nilai_maks_min()
