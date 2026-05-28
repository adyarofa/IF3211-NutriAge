# =============================================================================
# NutriAge - Utility Functions
# =============================================================================
# File ini berisi fungsi-fungsi utilitas untuk mendukung aplikasi

import pandas as pd
import numpy as np

# Definisi Warna Palette (Sesuai Ketentuan)
COLORS = {
    'ungu': '#A07ED2',
    'pink': '#FF006E',
    'orange_tua': '#FF470B',
    'orange': '#F99C01',
    'lime': '#D2D641',
    'olive': '#748C2C'
}

# Warna untuk masing-masing makromolekul
MACRO_COLORS = {
    'Karbohidrat': '#F99C01',  # Orange
    'Protein': '#FF006E',       # Pink
    'Lipid': '#748C2C'          # Olive Green
}


def get_age_category(usia: int) -> str:
    """
    Mengkategorikan usia ke dalam kelompok.
    
    Parameters:
    -----------
    usia : int
        Usia dalam tahun
    
    Returns:
    --------
    str : Kategori usia
    """
    if usia <= 5:
        return "Balita"
    elif usia <= 12:
        return "Anak-anak"
    elif usia <= 18:
        return "Remaja"
    elif usia <= 29:
        return "Dewasa Muda"
    elif usia <= 49:
        return "Dewasa"
    elif usia <= 64:
        return "Pra-Lansia"
    else:
        return "Lansia"


def format_number(value: float, decimal: int = 1) -> str:
    """
    Format angka dengan separator ribuan.
    
    Parameters:
    -----------
    value : float
        Angka yang akan diformat
    decimal : int
        Jumlah desimal
    
    Returns:
    --------
    str : Angka yang sudah diformat
    """
    return f"{value:,.{decimal}f}"


def calculate_total_calories(karbo: float, protein: float, lipid: float) -> float:
    """
    Menghitung total kalori dari makromolekul.
    
    Parameters:
    -----------
    karbo : float
        Karbohidrat dalam gram
    protein : float
        Protein dalam gram
    lipid : float
        Lipid dalam gram
    
    Returns:
    --------
    float : Total kalori
    """
    # 1g karbo = 4 kkal, 1g protein = 4 kkal, 1g lipid = 9 kkal
    return (karbo * 4) + (protein * 4) + (lipid * 9)


def get_calorie_distribution(karbo: float, protein: float, lipid: float) -> dict:
    """
    Menghitung distribusi kalori dari masing-masing makromolekul.
    
    Parameters:
    -----------
    karbo : float
        Karbohidrat dalam gram
    protein : float
        Protein dalam gram
    lipid : float
        Lipid dalam gram
    
    Returns:
    --------
    dict : Distribusi kalori dalam persentase
    """
    total = calculate_total_calories(karbo, protein, lipid)
    
    if total == 0:
        return {'Karbohidrat': 0, 'Protein': 0, 'Lipid': 0}
    
    return {
        'Karbohidrat': round((karbo * 4 / total) * 100, 1),
        'Protein': round((protein * 4 / total) * 100, 1),
        'Lipid': round((lipid * 9 / total) * 100, 1)
    }


def create_summary_dataframe(karbo_result: dict, protein_result: dict, lipid_result: dict) -> pd.DataFrame:
    """
    Membuat DataFrame ringkasan hasil simulasi.
    
    Parameters:
    -----------
    karbo_result : dict
        Hasil perhitungan karbohidrat
    protein_result : dict
        Hasil perhitungan protein
    lipid_result : dict
        Hasil perhitungan lipid
    
    Returns:
    --------
    pd.DataFrame : Ringkasan dalam bentuk tabel
    """
    
    total_kalori = calculate_total_calories(
        karbo_result['kebutuhan_gram'],
        protein_result['kebutuhan_gram'],
        lipid_result['kebutuhan_gram']
    )
    
    distribusi = get_calorie_distribution(
        karbo_result['kebutuhan_gram'],
        protein_result['kebutuhan_gram'],
        lipid_result['kebutuhan_gram']
    )
    
    data = {
        'Makromolekul': ['Karbohidrat', 'Protein', 'Lipid', 'TOTAL'],
        'Kebutuhan (gram)': [
            karbo_result['kebutuhan_gram'],
            protein_result['kebutuhan_gram'],
            lipid_result['kebutuhan_gram'],
            karbo_result['kebutuhan_gram'] + protein_result['kebutuhan_gram'] + lipid_result['kebutuhan_gram']
        ],
        'Kalori (kkal)': [
            karbo_result['kalori'],
            protein_result['kalori'],
            lipid_result['kalori'],
            total_kalori
        ],
        'Distribusi (%)': [
            distribusi['Karbohidrat'],
            distribusi['Protein'],
            distribusi['Lipid'],
            100.0
        ]
    }
    
    return pd.DataFrame(data)


def get_healthy_aging_tips(usia: int) -> list:
    """
    Memberikan tips healthy aging berdasarkan usia.
    
    Parameters:
    -----------
    usia : int
        Usia dalam tahun
    
    Returns:
    --------
    list : Daftar tips
    """
    
    tips_umum = [
        "Minum air putih minimal 8 gelas per hari",
        "Tidur cukup 7-9 jam setiap malam",
        "Olahraga teratur minimal 30 menit per hari"
    ]
    
    if usia <= 18:
        tips_spesifik = [
            "Pastikan asupan kalsium cukup untuk pertumbuhan tulang",
            "Hindari makanan cepat saji berlebihan",
            "Konsumsi buah dan sayur setiap hari"
        ]
    elif usia <= 49:
        tips_spesifik = [
            "Jaga berat badan ideal",
            "Kurangi konsumsi gula dan garam",
            "Kelola stress dengan baik"
        ]
    else:
        tips_spesifik = [
            "Perhatikan asupan protein untuk mencegah sarcopenia",
            "Rutin cek kesehatan (gula darah, kolesterol, tekanan darah)",
            "Jaga aktivitas sosial dan kesehatan mental"
        ]
    
    return tips_umum + tips_spesifik
