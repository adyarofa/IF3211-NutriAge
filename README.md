# NutriAge — Simulasi Kebutuhan Nutrisi Makromolekul Berdasarkan Usia

Tugas Besar IF3211 Komputasi Domain Spesifik

---

## Deskripsi

NutriAge adalah aplikasi web interaktif berbasis Streamlit yang mensimulasikan kebutuhan nutrisi makromolekul (karbohidrat, protein, dan lipid) berdasarkan usia dan jenis kelamin. Aplikasi ini dikembangkan untuk mendukung konsep healthy aging — proses menua secara sehat dengan memperhatikan asupan nutrisi yang tepat pada setiap tahapan kehidupan.

---

## Fitur

- Kalkulasi kebutuhan karbohidrat, protein, dan lipid harian berdasarkan usia dan jenis kelamin
- Visualisasi distribusi kalori dalam bentuk pie chart
- Grafik kebutuhan nutrisi sepanjang rentang usia 1–100 tahun
- Insight biologis per makromolekul sesuai kelompok usia
- Tips healthy aging yang disesuaikan dengan usia pengguna
- Halaman analisis data dengan filter jenis kelamin dan rentang usia

---

## Struktur Proyek

```
IF3211-NutriAge/
├── app.py                  # Entry point aplikasi Streamlit
├── requirements.txt        # Dependensi Python
├── README.md               # Dokumentasi proyek
├── modules/
│   ├── __init__.py         # Ekspor semua modul
│   ├── carbohydrate.py     # Modul perhitungan karbohidrat
│   ├── protein.py          # Modul perhitungan protein
│   ├── lipid.py            # Modul perhitungan lipid
│   ├── ml_model.py         # Loading dan prediksi model ML
│   └── integration.py      # Pipeline terpadu & combined DataFrame
├── utils/
│   ├── __init__.py
│   └── helpers.py          # Fungsi utilitas dan konstanta warna
├── data/
│   └── __init__.py
├── models/
│   ├── nutriage_macro_model.joblib
│   └── nutriage_macro_model_metadata.json
└── public/
    ├── logo.png            # Logo ikon
    └── logo-name.png       # Logo dengan nama
```

---

## Instalasi dan Menjalankan Aplikasi

### Prasyarat

- Python 3.9 atau lebih baru
- pip atau conda

### Langkah Instalasi

1. Clone repositori

```bash
git clone https://github.com/adyarofa/IF3211-NutriAge.git
cd IF3211-NutriAge
```

2. Install dependensi

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`.

---

## Dependensi

| Package    | Versi Minimum | Kegunaan                        |
|------------|---------------|---------------------------------|
| streamlit  | 1.28.0        | Framework aplikasi web          |
| pandas     | 2.0.0         | Pengolahan data tabular          |
| numpy      | 1.24.0        | Komputasi numerik               |
| matplotlib | 3.7.0         | Visualisasi (pendukung)         |
| plotly     | 5.18.0        | Visualisasi interaktif          |
| scikit-learn | 1.3.0        | Machine learning (model loading)|
| joblib     | 1.3.0         | Serialisasi model               |

---

## Referensi Data

Data kebutuhan nutrisi dalam aplikasi ini bersumber dari:

- Angka Kecukupan Gizi (AKG) yang ditetapkan oleh Kementerian Kesehatan Republik Indonesia
- WHO Guidelines untuk kebutuhan nutrisi berdasarkan kelompok usia
- Literatur ilmiah terkait nutrisi dan metabolisme makromolekul

---

## Pipeline Komputasi

Aplikasi NutriAge menggunakan pipeline multi-tahap untuk menghasilkan prediksi kebutuhan nutrisi:

### 1. Input Data
- Usia pengguna (1–100 tahun)
- Jenis kelamin (Laki-laki / Perempuan)

### 2. Prediksi Model ML
- Model machine learning yang dilatih pada data AKG Indonesia dan WHO Guidelines
- Memprediksi kebutuhan karbohidrat, protein, dan lipid dalam gram/hari
- Fallback ke kalkulator berbasis rumus jika model tidak tersedia

### 3. Perhitungan Makromolekul
Setiap makromolekul dihitung melalui modul terpisah:

| Modul       | Input                  | Output                                    |
|-------------|------------------------|-------------------------------------------|
| carbohydrate.py | usia, jenis_kelamin | gram/hari, kkal/hari, kategori usia       |
| protein.py  | usia, jenis_kelamin | gram/hari, kkal/hari, kategori usia       |
| lipid.py    | usia, jenis_kelamin | gram/hari, kkal/hari, kategori usia       |

### 4. Agregasi Data
- Modul `integration.py` menggabungkan hasil ketiga makromolekul
- Menghasilkan DataFrame terpadu untuk visualisasi
- Menghitung total kalori dan distribusi persentase

### 5. Insight & Visualisasi
- Menghasilkan insight biologis berdasarkan kelompok usia
- Tips healthy aging yang disesuaikan
- Grafik interaktif menggunakan Plotly
- Tabel ringkasan hasil kalkulasi

### Diagram Alur

```
Input (usia, jenis_kelamin)
            |
            v
    [predict_macro_needs]
    (Model ML + Fallback)
            |
    +-------+-------+
    |       |       |
    v       v       v
  [Karbo] [Protein] [Lipid]
  Module  Module   Module
    |       |       |
    +-------+-------+
            |
            v
    [create_summary_dataframe]
    [get_calorie_distribution]
            |
            v
        Output
    (Tabel + Grafik)
```

---

## Kelompok Usia

| Kategori     | Rentang Usia |
|--------------|--------------|
| Balita       | 1–5 tahun    |
| Anak-anak    | 6–12 tahun   |
| Remaja       | 13–18 tahun  |
| Dewasa Muda  | 19–29 tahun  |
| Dewasa       | 30–49 tahun  |
| Pra-Lansia   | 50–64 tahun  |
| Lansia       | 65+ tahun    |

---

## Mata Kuliah

IF3211 — Komputasi Domain Spesifik

Institut Teknologi Bandung

---

## Tim Pengembang

| Nama                              | NIM      | Peran                      |
|-----------------------------------|----------|----------------------------|
| Samuel Chris Michael Bagasta Simanjuntak | 18223011 | Lipid & Backend            |
| Carlen Asadel Axelle              | 18223017 | Karbohidrat & Form Input    |
| Allodya Qonita Arrofa             | 18223054 | Protein & Output Page       |
| Audy Alicia Renatha Tirayoh       | 18223097 | Integrasi & UI/Styling     |

---

## Lisensi

Proyek ini dikembangkan sebagai tugas besar untuk mata kuliah IF3211 Komputasi Domain Spesifik di Institut Teknologi Bandung.