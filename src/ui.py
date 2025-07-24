import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from src.calculations import interpolasi, hitung_z_score, tentukan_status, validasi_tinggi, hitung_usia_hari, hitung_usia_bulan
from src.data_manager import baca_data, simpan_histori, baca_histori

def buat_grafik(df_histori):
    """Membuat grafik Z-score menggunakan Plotly Express."""
    if not df_histori.empty:
        df_plot = df_histori.copy()
        df_plot['Tanggal'] = pd.to_datetime(df_plot['Tanggal'])
        
        fig = px.line(df_plot, x="Tanggal", y="Z-score", markers=True, 
                     title="Perkembangan Z-score Anak",
                     hover_data={"Usia (Hari)": True, "Usia (Bulan)": True, "Tinggi (cm)": True, "Status": True})
        
        fig.add_hline(y=2, line_dash="dot", line_color="green", 
                     annotation_text="Normal (+2)", annotation_position="top left")
        fig.add_hline(y=-2, line_dash="dash", line_color="orange", 
                     annotation_text="Batas Stunting (-2)", annotation_position="top left")
        fig.add_hline(y=-3, line_dash="dash", line_color="red", 
                     annotation_text="Stunting Berat (-3)", annotation_position="top left")
        
        fig.add_hrect(y0=-3, y1=-2, fillcolor="red", opacity=0.1, line_width=0)
        fig.add_hrect(y0=-2, y1=2, fillcolor="green", opacity=0.1, line_width=0)
        
        fig.update_layout(
            xaxis_title="Tanggal Pengukuran", 
            yaxis_title="Z-score", 
            showlegend=False,
            yaxis=dict(range=[-4, 4])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Interpretasi Z-score berdasarkan WHO:**
        - **Z > +2**: Tinggi (perlu pemantauan)
        - **+2 ≥ Z ≥ -2**: Normal
        - **-3 ≤ Z < -2**: Pendek/Stunting (perlu intervensi gizi)
        - **Z < -3**: Sangat Pendek/Severely Stunted (perlu intervensi medis segera)
        """)

def render_ui(profil):
    """Merender antarmuka pengguna Streamlit."""
    st.title("Kalkulator Stunting Anak")
    st.markdown("**Standar WHO - Pemantauan Pertumbuhan**")
    st.write("Aplikasi untuk memantau pertumbuhan tinggi/panjang badan anak usia 0-5 tahun")
    
    st.info("Data WHO: Length/Height-for-Age Z-scores (0-1856 hari)")
    
    tanggal_sekarang = datetime.now()
    st.success(f"Tanggal Pengukuran: {tanggal_sekarang.strftime('%d/%m/%Y %H:%M:%S')}")
    
    st.markdown("""
    <style>
    /* Light mode styles */
    .metric-container {
        background-color: var(--background-color, #f8f9fa);
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
        border-left: 4px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: var(--text-color, #333);
        transition: all 0.3s ease;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #007bff;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--secondary-text-color, #6c757d);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .status-normal { border-left-color: #28a745; }
    .status-normal .metric-value { color: #28a745; }
    .status-stunting { border-left-color: #ffc107; }
    .status-stunting .metric-value { color: #e67e22; }
    .status-severe { border-left-color: #dc3545; }
    .status-severe .metric-value { color: #dc3545; }
    
    .info-box {
        background-color: var(--background-color, #f8f9fa);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
        color: var(--text-color, #333);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .info-box h4 {
        color: var(--text-color, #333);
        margin-top: 0;
    }
    
    .info-box p {
        color: var(--text-color, #333);
        margin: 0.5rem 0;
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #262730;
            --text-color: #fafafa;
            --secondary-text-color: #a0a0a0;
        }
        
        .metric-container {
            background-color: #262730;
            border-color: rgba(255,255,255,0.1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .info-box {
            background-color: #262730;
            border-color: rgba(255,255,255,0.1);
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        
        .status-stunting .metric-value { 
            color: #f39c12;
        }
    }
    
    [data-testid="stAppViewContainer"][data-theme="dark"] .metric-container,
    .stApp[data-theme="dark"] .metric-container {
        background-color: #262730 !important;
        color: #fafafa !important;
        border-color: rgba(255,255,255,0.1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    [data-testid="stAppViewContainer"][data-theme="dark"] .info-box,
    .stApp[data-theme="dark"] .info-box {
        background-color: #262730 !important;
        color: #fafafa !important;
        border-color: rgba(255,255,255,0.1) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
    }
    
    [data-testid="stAppViewContainer"][data-theme="dark"] .info-box h4,
    [data-testid="stAppViewContainer"][data-theme="dark"] .info-box p,
    .stApp[data-theme="dark"] .info-box h4,
    .stApp[data-theme="dark"] .info-box p {
        color: #fafafa !important;
    }
    
    [data-testid="stAppViewContainer"][data-theme="dark"] .metric-label,
    .stApp[data-theme="dark"] .metric-label {
        color: #a0a0a0 !important;
    }
    
    [data-testid="stAppViewContainer"][data-theme="dark"] .status-stunting .metric-value,
    .stApp[data-theme="dark"] .status-stunting .metric-value {
        color: #f39c12 !important;
    }
    
    @media (max-width: 768px) {
        .metric-value { font-size: 1.8rem; }
        .metric-container { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    nama = profil["nama"]
    jenis_kelamin = profil["jenis_kelamin"]
    tanggal_lahir = profil["tanggal_lahir"]
    tanggal_lahir_dt = datetime.combine(tanggal_lahir, datetime.min.time())
    
    try:
        usia_hari = hitung_usia_hari(tanggal_lahir_dt, tanggal_sekarang)
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        return
    
    if usia_hari <= 0:
        st.error("Tanggal lahir tidak valid untuk pengukuran!")
        return
    
    usia_bulan = hitung_usia_bulan(usia_hari)
    
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin-top: 0; margin-bottom: 1rem;">Profil Anak</h4>
        <p style="margin: 0.5rem 0;"><strong>Nama:</strong> {nama}</p>
        <p style="margin: 0.5rem 0;"><strong>Jenis Kelamin:</strong> {jenis_kelamin}</p>
        <p style="margin: 0.5rem 0;"><strong>Tanggal Lahir:</strong> {tanggal_lahir.strftime('%d/%m/%Y')}</p>
        <p style="margin: 0.5rem 0;"><strong>Usia:</strong> {usia_hari} hari (~{usia_bulan:.1f} bulan)</p>
    </div>
    """, unsafe_allow_html=True)
    
    if usia_hari > 1856:
        st.error(f"Usia anak ({usia_hari} hari) melebihi rentang data referensi WHO (maksimum 1856 hari). Aplikasi ini untuk anak 0-5 tahun.")
        return

    with st.form("form_stunting"):
        st.subheader("Input Tinggi Badan")
        
        tinggi = st.number_input(
            "Tinggi/Panjang Badan (cm)", 
            min_value=30.0, 
            max_value=150.0, 
            value=70.0,
            step=0.1,
            help="Masukkan tinggi dalam cm (contoh: 75.5)"
        )
        
        submit_button = st.form_submit_button("Cek Status Pertumbuhan", use_container_width=True)

    if submit_button:
        try:
            valid_tinggi, pesan_validasi = validasi_tinggi(tinggi, usia_bulan)
            if not valid_tinggi:
                st.error(f"Error: {pesan_validasi}")
                return

            file_path = f"data/lhfa-{'girls' if jenis_kelamin == 'Perempuan' else 'boys'}-zscore-expanded-tables.xlsx"
            
            df = baca_data(file_path)
            L, M, S = interpolasi(usia_hari, df)
            z_score = hitung_z_score(tinggi, L, M, S)
            status, pesan = tentukan_status(z_score)
            
            success, message = simpan_histori(tanggal_sekarang, jenis_kelamin, usia_hari, usia_bulan, tinggi, z_score, status, nama, "WARGA")
            if not success:
                st.error(f"Error: {message}")
                return
                
            st.success(f"Berhasil: {message}")
            
            with st.container():
                st.subheader("Hasil Analisis Pertumbuhan")
                
                status_class = "status-severe" if z_score < -3 else "status-stunting" if z_score < -2 else "status-normal"
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-container {status_class}">
                        <div class="metric-label">Z-Score</div>
                        <div class="metric-value">{z_score:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-container {status_class}">
                        <div class="metric-label">Status Pertumbuhan</div>
                        <div class="metric-value" style="font-size: 1.4rem;">{status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Tinggi Badan</div>
                    <div class="metric-value">{tinggi} cm</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Detail Pengukuran"):
                    st.write(f"**Nama:** {nama}")
                    st.write(f"**Jenis Penginput:** WARGA")
                    st.write(f"**Tanggal Pengukuran:** {tanggal_sekarang.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Jenis Kelamin:** {jenis_kelamin}")
                    st.write(f"**Parameter WHO:** L={L:.4f}, M={M:.2f}, S={S:.4f}")
                
                if z_score < -2:
                    st.error(f"Perhatian: {pesan}")
                elif z_score > 2:
                    st.warning(f"Catatan: {pesan}")
                else:
                    st.success(f"Status: {pesan}")
        
        except FileNotFoundError as e:
            st.error(f"File tidak ditemukan: {str(e)}")
            st.info("Pastikan file Excel 'lhfa-boys-zscore-expanded-tables.xlsx' dan 'lhfa-girls-zscore-expanded-tables.xlsx' ada di folder data/.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")

    st.markdown("---")
    st.subheader("Histori dan Grafik Pertumbuhan")
    
    df_histori = baca_histori()
    if not df_histori.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Pengukuran", len(df_histori))
        
        with col2:
            z_scores = df_histori['Z-score'].astype(float)
            st.metric("Z-score Terakhir", f"{z_scores.iloc[-1]:.2f}")
        
        with col3:
            stunting_count = len(df_histori[df_histori['Z-score'].astype(float) < -2])
            st.metric("Riwayat Stunting", f"{stunting_count} kali")
        
        st.subheader("Data Histori Pengukuran")
        st.dataframe(df_histori, use_container_width=True)
        
        st.subheader("Grafik Perkembangan Z-score")
        buat_grafik(df_histori)
        
        if len(df_histori) >= 2:
            z_scores = df_histori['Z-score'].astype(float)
            trend = "naik" if z_scores.iloc[-1] > z_scores.iloc[-2] else "turun"
            if trend == "naik":
                st.info("Tren Positif: Z-score meningkat dari pengukuran sebelumnya.")
            else:
                st.warning("Perhatian: Z-score menurun dari pengukuran sebelumnya. Pantau nutrisi anak.")
    else:
        st.info("Belum ada data histori pengukuran. Silakan lakukan pengukuran pertama.")
        
    st.markdown("---")
    with st.expander("Informasi Penting"):
        st.markdown("""
        **Catatan Penting:**
        - Aplikasi ini menggunakan standar WHO Growth Charts (Length/Height-for-Age Z-scores, 0-1856 hari)
        - Data referensi diambil dari tabel WHO resmi untuk anak laki-laki dan perempuan
        - Konsultasikan hasil dengan tenaga kesehatan untuk diagnosis akurat
        - Pemantauan rutin penting untuk deteksi dini stunting
        - Data histori disimpan di sesi aplikasi dan akan hilang saat aplikasi ditutup
        - Sumber data: WHO Child Growth Standards (https://www.who.int/childgrowth/standards)
        """)