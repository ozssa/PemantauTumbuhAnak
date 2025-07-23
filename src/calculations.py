import math
import streamlit as st

def interpolasi(usia_hari, df):
    """Melakukan interpolasi linier untuk mendapatkan L, M, S berdasarkan usia."""
    if usia_hari < df['Day'].min():
        st.warning(f"Usia {usia_hari} hari terlalu muda. Menggunakan data usia minimum: {df['Day'].min()} hari.")
        return df.iloc[0]['L'], df.iloc[0]['M'], df.iloc[0]['S']
    
    if usia_hari > df['Day'].max():
        st.warning(f"Usia {usia_hari} hari melebihi data referensi. Menggunakan data usia maksimum: {df['Day'].max()} hari.")
        return df.iloc[-1]['L'], df.iloc[-1]['M'], df.iloc[-1]['S']
    
    df_bawah = df[df['Day'] <= usia_hari].iloc[-1]
    df_atas = df[df['Day'] >= usia_hari].iloc[0]
    
    if df_bawah['Day'] == df_atas['Day']:
        return df_bawah['L'], df_bawah['M'], df_bawah['S']
    
    proporsi = (usia_hari - df_bawah['Day']) / (df_atas['Day'] - df_bawah['Day'])
    L = df_bawah['L'] + proporsi * (df_atas['L'] - df_bawah['L'])
    M = df_bawah['M'] + proporsi * (df_atas['M'] - df_bawah['M'])
    S = df_bawah['S'] + proporsi * (df_atas['S'] - df_bawah['S'])
    
    return L, M, S

def hitung_z_score(tinggi, L, M, S):
    """Menghitung Z-score berdasarkan rumus WHO LMS."""
    try:
        if abs(L) < 1e-7:
            z_score = math.log(tinggi / M) / S
        else:
            z_score = ((tinggi / M) ** L - 1) / (L * S)
        return z_score
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        raise ValueError(f"Error menghitung Z-score: {str(e)}. Periksa nilai tinggi yang dimasukkan.")

def tentukan_status(z_score):
    """Menentukan status stunting berdasarkan Z-score WHO."""
    if z_score < -3:
        return "Sangat Pendek (Severely Stunted)", "Anak sangat pendek untuk usianya. Segera konsultasikan ke dokter atau puskesmas!"
    elif z_score < -2:
        return "Pendek (Stunted)", "Anak pendek untuk usianya. Perhatikan gizi dan konsultasikan ke puskesmas."
    elif z_score > 3:
        return "Sangat Tinggi", "Anak sangat tinggi untuk usianya. Konsultasikan ke dokter untuk pemeriksaan lebih lanjut."
    elif z_score > 2:
        return "Tinggi", "Anak tinggi untuk usianya. Pantau terus pertumbuhannya."
    else:
        return "Normal", "Tinggi anak sesuai untuk usianya. Pertahankan pola makan sehat!"

def validasi_tinggi(tinggi, usia_bulan):
    """Validasi tinggi berdasarkan usia untuk mencegah input yang tidak masuk akal."""
    if usia_bulan < 1:
        min_tinggi, max_tinggi = 40, 60
    elif usia_bulan < 12:
        min_tinggi, max_tinggi = 45, 85
    elif usia_bulan < 24:
        min_tinggi, max_tinggi = 65, 95
    elif usia_bulan < 36:
        min_tinggi, max_tinggi = 75, 105
    elif usia_bulan < 60:
        min_tinggi, max_tinggi = 85, 120
    else:
        min_tinggi, max_tinggi = 95, 140
    
    if tinggi < min_tinggi or tinggi > max_tinggi:
        return False, f"Tinggi {tinggi} cm tidak wajar untuk usia {usia_bulan:.1f} bulan. Rentang normal: {min_tinggi}-{max_tinggi} cm."
    return True, ""

def hitung_usia_hari(tanggal_lahir, tanggal_ukur):
    """Menghitung usia dalam hari dengan akurat."""
    if tanggal_lahir > tanggal_ukur:
        raise ValueError("Tanggal lahir tidak boleh setelah tanggal pengukuran.")
    selisih = tanggal_ukur - tanggal_lahir
    return selisih.days

def hitung_usia_bulan(usia_hari):
    """Konversi usia hari ke bulan menggunakan standar WHO (30.4375 hari per bulan)."""
    return usia_hari / 30.4375