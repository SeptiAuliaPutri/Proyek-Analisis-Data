import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset
script_dir = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(f"{script_dir}/data_clean.csv")

# Mengelompokkan data berdasarkan tahun dan menghitung rata-rata, minimum, maksimum untuk NO2, SO2, PM2.5
NO2_pollution = data.groupby('year')[['NO2']].agg(['mean', 'min', 'max'])
SO2_pollution = data.groupby('year')[['SO2']].agg(['mean', 'min', 'max'])
PM25_pollution = data.groupby('year')[['PM2.5']].agg(['mean', 'min', 'max'])

# Menghitung total polusi dari NO2, SO2, dan PM2.5 setiap tahunnya
yearly_pollution = data.groupby('year')[['NO2', 'SO2', 'PM2.5']].mean()
yearly_pollution['total_pollution'] = yearly_pollution[['NO2', 'SO2', 'PM2.5']].apply(lambda x: x.sum(), axis=1)
sorted_yearly_pollution = yearly_pollution.sort_values(by='total_pollution', ascending=False)

# Fungsi untuk memplot grafik
def plot_pollution_trends(pollution_data):
    plt.figure(figsize=(18, 6))
    for i, (pollutant, values) in enumerate(pollution_data.items(), start=1):
        plt.subplot(1, 3, i)
        plt.plot(values.index, values, color='brown')
        plt.title(f'Rata-rata {pollutant} Pollution per Tahun')
        plt.xlabel('Tahun')
        plt.ylabel('Konsentrasi (μg/m³)')
        plt.xticks(values.index)
        plt.grid(axis='y')
    st.pyplot(plt)

def plot_total_pollution():
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_yearly_pollution.index, sorted_yearly_pollution['total_pollution'], color='beige')
    plt.title('Total Polusi per Tahun (NO2, SO2, PM2.5)')
    plt.xlabel('Tahun')
    plt.ylabel('Total Polusi (μg/m³)')
    plt.xticks(sorted_yearly_pollution.index)
    plt.grid(axis='y')
    st.pyplot(plt)

def plot_pie_chart(year):
    average_pollution = yearly_pollution.loc[year].drop('total_pollution')
    plt.figure(figsize=(8, 8))
    plt.pie(average_pollution, labels=average_pollution.index, autopct='%1.1f%%', startangle=140, colors=['beige', 'lightblue', 'pink'])
    plt.title(f'Proporsi Rata-rata Polusi di Tahun {year}')
    plt.axis('equal')
    st.pyplot(plt)

def plot_correlation(monthly_avg):
    correlation_matrix = monthly_avg[['TEMP', 'NO2', 'SO2', 'PM2.5']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True, square=True)
    plt.title('Korelasi antara Suhu dan Polutan')
    st.pyplot(plt)

# Streamlit interface
st.title("ANALISIS KUALITAS UDARA DI TAINAN")

# Sidebar untuk memilih tahun
st.sidebar.header("Pilih Tahun untuk Analisis")
year = st.sidebar.selectbox("Tahun", yearly_pollution.index)

# Tab untuk analisis
tab1, tab2 = st.tabs(["Analisis Polusi", "Pengaruh Lingkungan terhadap Polutan"])

# Tab Analisis Polusi
with tab1:
    st.header("Tingkat Total Polusi Tertinggi")
    plot_total_pollution()

    # Menampilkan grafik tren polusi
    pollution_data = {
        'NO2': NO2_pollution['NO2']['mean'],
        'SO2': SO2_pollution['SO2']['mean'],
        'PM2.5': PM25_pollution['PM2.5']['mean']
    }
    
    st.header(f"Tren Rata-rata Polutan")
    plot_pollution_trends(pollution_data)

    # Menampilkan diagram pie
    st.header(f"Proporsi Polusi di Tahun {year}")
    plot_pie_chart(year)

# Tab Pengaruh Lingkungan terhadap Polutan
with tab2:
    st.header("Pengaruh Lingkungan terhadap Polutan")
    
    # Pilihan jenis polutan
    pollutant_choice = st.selectbox("Pilih Jenis Polutan", ["NO2", "SO2", "PM2.5"])

    # Menghitung rata-rata bulanan
    monthly_avg = data.groupby('month').agg({
        'TEMP': 'mean',
        'NO2': 'mean',
        'SO2': 'mean',
        'PM2.5': 'mean'
    }).reset_index()

    # Menampilkan plot spesifik untuk polutan yang dipilih
    st.subheader(f"Pengaruh Suhu terhadap {pollutant_choice}")
    plt.figure(figsize=(8, 6))
    plt.scatter(monthly_avg['TEMP'], monthly_avg[pollutant_choice], alpha=0.6)
    plt.title(f'Suhu vs {pollutant_choice}')
    plt.xlabel('Suhu (°C)')
    plt.ylabel(f'Konsentrasi {pollutant_choice} (μg/m³)')
    plt.grid()
    st.pyplot(plt)

    # Menampilkan korelasi
    st.subheader("Korelasi antara Suhu dan Polutan")
    plot_correlation(monthly_avg)
