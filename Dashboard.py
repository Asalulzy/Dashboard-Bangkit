import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk mengklasifikasikan musim berdasarkan suhu
def classify_season(temp):
    if temp < 0:
        return 'Gelombang Dingin'
    elif 0 <= temp < 10:
        return 'Musim Dingin'
    elif 10 <= temp < 20:
        return 'Musim Semi'
    elif 20 <= temp < 35:
        return 'Musim Panas'
    elif temp >= 35:
        return 'Gelombang Panas'
    else:
        return 'Tidak Diketahui'

# Load Data
data_path = 'https://raw.githubusercontent.com/Asalulzy/Dashboard-Bangkit/main/all_data.csv'
data = pd.read_csv(data_path)

# Menyaring kolom yang diperlukan
if 'TEMP' in data.columns and 'datetime' in data.columns:
    # Menambahkan kolom musim
    data['Season'] = data['TEMP'].apply(classify_season)

    # Mengonversi kolom 'datetime' menjadi tipe datetime
    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')

    # Streamlit Layout
    st.title('Dashboard Analisis Polutan Udara')

    # Sidebar untuk pemilihan filter musim
    st.sidebar.header('Filter Data')
    selected_season = st.sidebar.selectbox('Pilih Musim:', data['Season'].unique())

    # Filter data berdasarkan pilihan pengguna
    filtered_data = data[data['Season'] == selected_season]
    st.write(f"Menampilkan data untuk musim: **{selected_season}**")

    if not filtered_data.empty:
        # Line Plot untuk menunjukkan tren polutan udara
        st.header(f"Tren Polutan Udara untuk Musim {selected_season}")
        fig_line, ax_line = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=filtered_data, x='datetime', y='NO2', label='NO2', color='blue')
        sns.lineplot(data=filtered_data, x='datetime', y='SO2', label='SO2', color='green')
        sns.lineplot(data=filtered_data, x='datetime', y='PM10', label='PM10', color='red')
        sns.lineplot(data=filtered_data, x='datetime', y='O3', label='O3', color='purple')
        ax_line.set_title(f'Tren Polutan Udara di Musim {selected_season}')
        ax_line.set_xlabel('Tanggal')
        ax_line.set_ylabel('Konsentrasi (µg/m³)')
        plt.xticks(rotation=45)
        st.pyplot(fig_line)

        # Box Plot untuk menunjukkan distribusi konsentrasi senyawa udara
        st.header(f"Distribusi Konsentrasi Senyawa Udara di Musim {selected_season}")
        fig_box, ax_box = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=filtered_data[['NO2', 'SO2', 'PM10', 'O3']], ax=ax_box, palette='Set3')
        ax_box.set_title(f'Distribusi Konsentrasi Senyawa Udara di Musim {selected_season}')
        ax_box.set_ylabel('Konsentrasi (µg/m³)')
        st.pyplot(fig_box)

        # Bar Plot untuk membandingkan rata-rata konsentrasi senyawa udara
        st.header(f"Rata-rata Konsentrasi Senyawa Udara di Musim {selected_season}")
        mean_data = filtered_data[['NO2', 'SO2', 'PM10', 'O3']].mean()
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        sns.barplot(x=mean_data.index, y=mean_data.values, palette='viridis', ax=ax_bar)
        ax_bar.set_title(f'Rata-rata Konsentrasi Senyawa Udara di Musim {selected_season}')
        ax_bar.set_ylabel('Konsentrasi (µg/m³)')
        st.pyplot(fig_bar)

        # Menampilkan data tabel
        st.subheader('Tabel Data Terfilter')
        st.dataframe(filtered_data)

        # Menggunakan st.cache_data untuk caching
        @st.cache_data
        def convert_df(df):  # Memastikan tanda kurung "(" dan ":" ada
            return df.to_csv().encode('utf-8')

        csv = convert_df(filtered_data)
        st.download_button(
            label="Unduh data terfilter sebagai CSV",
            data=csv,
            file_name='data_filtered.csv',
            mime='text/csv',
        )
    else:
        st.warning("Tidak ada data untuk musim ini.")
else:
    st.error("Kolom 'TEMP' atau 'datetime' tidak ditemukan dalam data.")
