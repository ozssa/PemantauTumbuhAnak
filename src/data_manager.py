import pandas as pd
import os
import streamlit as st

def baca_data(file_path):
    """Membaca file Excel WHO dan mengembalikan DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} tidak ditemukan di folder data.")
    
    try:
        df = pd.read_excel(file_path)
        # Validasi kolom yang diperlukan
        required_columns = ['Day', 'L', 'M', 'S']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Kolom '{col}' tidak ditemukan dalam file Excel.")
        
        # Pastikan data terurut berdasarkan Day
        df = df.sort_values('Day').reset_index(drop=True)
        return df
    except Exception as e:
        raise Exception(f"Error membaca file Excel: {str(e)}")

def simpan_histori(tanggal, jenis_kelamin, usia_hari, usia_bulan, tinggi, z_score, status, nama="Agus", jenis_penginput="WARGA"):
    """Menyimpan data pengukuran ke session state."""
    tanggal_str = tanggal.strftime('%Y-%m-%d')
    
    # Inisialisasi session state untuk histori jika belum ada
    if 'histori' not in st.session_state:
        st.session_state.histori = pd.DataFrame(columns=["Nama", "JenisPenginput", "Tanggal", "Jenis Kelamin", "Usia (Hari)", "Usia (Bulan)", "Tinggi (cm)", "Z-score", "Status"])
    
    # Cek apakah sudah ada pengukuran untuk tanggal yang sama
    if 'histori' in st.session_state and not st.session_state.histori.empty:
        if tanggal_str in st.session_state.histori['Tanggal'].values:
            return False, "Pengukuran untuk hari ini sudah dilakukan. Hanya satu pengukuran per hari yang diizinkan."
    
    # Data baru
    data = {
        "Nama": [nama],
        "JenisPenginput": [jenis_penginput],
        "Tanggal": [tanggal_str],
        "Jenis Kelamin": [jenis_kelamin],
        "Usia (Hari)": [usia_hari],
        "Usia (Bulan)": [round(usia_bulan, 1)],
        "Tinggi (cm)": [tinggi],
        "Z-score": [round(z_score, 2)],
        "Status": [status]
    }
    df_new = pd.DataFrame(data)
    
    # Gabungkan data baru dengan histori di session state
    st.session_state.histori = pd.concat([st.session_state.histori, df_new], ignore_index=True)
    
    return True, "Data berhasil disimpan!"

def baca_histori():
    """Membaca histori pengukuran dari session state."""
    if 'histori' in st.session_state and not st.session_state.histori.empty:
        df = st.session_state.histori.copy()
        df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce').dt.strftime('%Y-%m-%d')
        df = df.sort_values('Tanggal')
        columns = ["Nama", "JenisPenginput", "Tanggal", "Jenis Kelamin", "Usia (Hari)", "Usia (Bulan)", "Tinggi (cm)", "Z-score", "Status"]
        df = df[columns]
        return df
    return pd.DataFrame(columns=["Nama", "JenisPenginput", "Tanggal", "Jenis Kelamin", "Usia (Hari)", "Usia (Bulan)", "Tinggi (cm)", "Z-score", "Status"])