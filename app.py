# app.py
import streamlit as st
from src.ui import render_ui
from datetime import date

def main():
    # Data profil tetap
    profil = {
        "nama": "Agus",
        "jenis_kelamin": "Laki-laki",
        "tanggal_lahir": date(2022, 1, 22)
    }
    
    # Konfigurasi halaman
    st.set_page_config(page_title="Kalkulator Stunting Anak", page_icon="🧒", layout="wide")
    
    # Render antarmuka pengguna
    render_ui(profil)

if __name__ == "__main__":
    main()