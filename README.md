# olahdata
Pengolahan Data Submission IDCamp

# Proyek Analisis Data: Air Quality

## Informasi Proyek
- **Nama:** Asep Obi
- **Email:** asepobi1@gmail.com
- **ID Dicoding:** asep_obi

## Menentukan Pertanyaan Bisnis

- Pertanyaan 1: What are the most significant pollutants affecting air quality?
- Pertanyaan 2: What is the trend of air quality index over the years?

## Struktur Direktori

- `base_dir`: `/workspaces/olahdata/PRSA_Data_20130301-20170228`
- `file_list`: Daftar file dalam direktori `base_dir`.

## Langkah-Langkah Analisis

1. **Memuat Data**
    - Menggunakan `os.listdir` untuk memperoleh daftar file CSV di direktori.
    - Memuat file CSV ke dalam DataFrames dan menyimpan dalam dictionary `dfs`.
    - Menghapus kolom `No` dari setiap DataFrame.

2. **Menampilkan DataFrame**
    - Menampilkan beberapa baris pertama dari setiap DataFrame yang dimuat untuk verifikasi.

3. **Menggabungkan Kolom Tanggal dan Waktu**
    - Menggabungkan kolom `year`, `month`, `day`, dan `hour` menjadi kolom `datetime`.

4. **Menghitung Duplikasi dan Jumlah Sampel**
    - Menghitung jumlah duplikasi dan total sampel untuk setiap DataFrame.
    - Menampilkan hasil dalam bentuk tabel.

5. **Tipe Data**
    - Mengumpulkan dan menampilkan tipe data untuk setiap kolom dalam setiap DataFrame.

6. **Menghitung Nilai Null**
    - Menghitung dan menampilkan jumlah nilai null untuk setiap kolom dalam setiap DataFrame.

7. **Mengisi Nilai Null dengan Median**
    - Menghitung nilai median untuk setiap kolom numerik dan mengisi nilai null dengan median tersebut.
    - Melakukan forward fill untuk kolom `wd`.

8. **Menghitung dan Menampilkan Nilai Mean dan Median**
    - Menghitung dan menampilkan nilai mean dan median untuk setiap kolom numerik.

9. **Menggabungkan Semua DataFrame**
    - Menggabungkan semua DataFrame menjadi satu DataFrame besar.
    - Menampilkan statistik deskriptif dari DataFrame gabungan.

10. **Kategorisasi Data**
    - Mengkategorikan data berdasarkan rentang AQI untuk berbagai polutan.

11. **Analisis Korelasi**
    - Menghitung dan menampilkan matriks korelasi untuk kolom numerik.
    - Menampilkan heatmap dari matriks korelasi.

## Jawaban Pertanyaan Bisnis

### Pertanyaan 1: What are the most significant pollutants affecting air quality?

- **Hasil Analisis Korelasi:**
  - PM2.5 dan PM10 memiliki korelasi tinggi (0.88).
  - PM2.5 berkorelasi positif dengan SO2 (0.48), NO2 (0.66), dan CO (0.77).
  - Ozon (O3) memiliki korelasi negatif dengan PM2.5 (-0.15), PM10 (-0.11), SO2 (-0.16), NO2 (-0.46), dan CO (-0.30).
  - Temperatur (TEMP) memiliki korelasi negatif dengan beberapa polutan.
  - Kecepatan angin (WSPM) berkorelasi negatif dengan beberapa polutan.

### Pertanyaan 2: What is the trend of air quality index over the years?

- **Hasil Analisis Tren Waktu:**
  - Menampilkan plot time series untuk PM2.5 dan PM10.
  - Menunjukkan pola peningkatan kualitas udara selama bertahun-tahun.

## Kesimpulan

**Kesimpulan Pertanyaan 1:**
- Tren indeks kualitas udara menunjukkan pola peningkatan kualitas udara selama bertahun-tahun. Ini menunjukkan bahwa upaya untuk mengurangi polusi dan meningkatkan kualitas udara telah efektif.

**Kesimpulan Pertanyaan 2:**
- Analisis korelasi mengungkapkan bahwa PM2.5 memiliki korelasi tertinggi dengan AQI, menunjukkan bahwa ini adalah polutan paling signifikan yang mempengaruhi kualitas udara. Mengontrol tingkat PM2.5 sangat penting untuk mempertahankan kualitas udara yang baik.

## Cara Menjalankan Proyek

1. Instalasi dependensi:
    ```bash
    pip install streamlit pandas numpy matplotlib seaborn scipy
    ```

2. Jalankan aplikasi Streamlit:
    ```bash
    streamlit run dashboard.py
    ```
