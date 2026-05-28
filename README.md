# NutriAge — Simulasi Kebutuhan Nutrisi Makromolekul Berdasarkan Usia

Tugas Besar IF3211 Komputasi Domain Spesifik

---

## Deskripsi

NutriAge adalah aplikasi web interaktif berbasis Streamlit yang mensimulasikan kebutuhan nutrisi makromolekul (karbohidrat, protein, dan lipid) berdasarkan usia dan jenis kelamin. Aplikasi ini dikembangkan untuk mendukung konsep *healthy aging* — proses menua secara sehat dengan memperhatikan asupan nutrisi yang tepat pada setiap tahapan kehidupan.

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
├── modules/
│   ├── carbohydrate.py     # Modul perhitungan karbohidrat
│   ├── protein.py          # Modul perhitungan protein
│   └── lipid.py            # Modul perhitungan lipid
├── utils/
│   └── helpers.py          # Fungsi utilitas dan konstanta warna
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

---

## Referensi Data

Data kebutuhan nutrisi dalam aplikasi ini bersumber dari:

- **Angka Kecukupan Gizi (AKG)** yang ditetapkan oleh Kementerian Kesehatan Republik Indonesia
- **WHO Guidelines** untuk kebutuhan nutrisi berdasarkan kelompok usia
- Literatur ilmiah terkait nutrisi dan metabolisme makromolekul

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
