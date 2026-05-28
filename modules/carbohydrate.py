# =============================================================================
# NutriAge - Modul Karbohidrat
# =============================================================================
# Modul ini menghitung kebutuhan karbohidrat berdasarkan usia dan jenis kelamin
# Referensi: Angka Kecukupan Gizi (AKG) Indonesia & WHO Guidelines

import pandas as pd
import numpy as np

def calculate_carbohydrate_needs(usia: int, jenis_kelamin: str) -> dict:
    """
    Menghitung kebutuhan karbohidrat harian berdasarkan usia dan jenis kelamin.
    
    Parameters:
    -----------
    usia : int
        Usia pengguna dalam tahun
    jenis_kelamin : str
        'Laki-laki' atau 'Perempuan'
    
    Returns:
    --------
    dict : Dictionary berisi kebutuhan karbohidrat dan detail lainnya
    """
    
    # Tabel kebutuhan karbohidrat berdasarkan kelompok usia (gram/hari)
    # Sumber: Adaptasi dari AKG Indonesia dan WHO
    kebutuhan_tabel = {
        'Laki-laki': {
            (0, 5): 155,
            (6, 9): 220,
            (10, 12): 289,
            (13, 15): 340,
            (16, 18): 368,
            (19, 29): 375,
            (30, 49): 340,
            (50, 64): 309,
            (65, 80): 275,
            (81, 120): 252
        },
        'Perempuan': {
            (0, 5): 155,
            (6, 9): 220,
            (10, 12): 275,
            (13, 15): 300,
            (16, 18): 309,
            (19, 29): 309,
            (30, 49): 286,
            (50, 64): 252,
            (65, 80): 232,
            (81, 120): 210
        }
    }
    
    # Cari kebutuhan berdasarkan rentang usia
    tabel = kebutuhan_tabel.get(jenis_kelamin, kebutuhan_tabel['Laki-laki'])
    kebutuhan = 0
    
    for (usia_min, usia_max), nilai in tabel.items():
        if usia_min <= usia <= usia_max:
            kebutuhan = nilai
            break
    
    # Jika usia di luar rentang, gunakan nilai terdekat
    if kebutuhan == 0:
        if usia < 0:
            kebutuhan = 155
        else:
            kebutuhan = 210 if jenis_kelamin == 'Perempuan' else 252
    
    # Hitung kalori dari karbohidrat (1 gram = 4 kkal)
    kalori = kebutuhan * 4
    
    # Hitung persentase dari total kalori harian (asumsi 2000-2500 kkal)
    total_kalori_harian = 2500 if jenis_kelamin == 'Laki-laki' else 2000
    persentase = (kalori / total_kalori_harian) * 100
    
    return {
        'kebutuhan_gram': kebutuhan,
        'kalori': kalori,
        'persentase_kalori': round(persentase, 1),
        'usia': usia,
        'jenis_kelamin': jenis_kelamin,
        'satuan': 'gram/hari'
    }


def get_carbohydrate_insight(usia: int, jenis_kelamin: str) -> str:
    """
    Memberikan insight biologis tentang kebutuhan karbohidrat berdasarkan usia.
    
    Parameters:
    -----------
    usia : int
        Usia pengguna dalam tahun
    jenis_kelamin : str
        'Laki-laki' atau 'Perempuan'
    
    Returns:
    --------
    str : Insight biologis dalam bentuk teks
    """
    
    if usia <= 5:
        return """
        🍞 **Insight Karbohidrat - Masa Balita**
        
        Pada masa balita, karbohidrat sangat penting untuk:
        - Perkembangan otak yang optimal (otak menggunakan ~60% glukosa tubuh)
        - Sumber energi utama untuk aktivitas fisik dan pertumbuhan
        - Pembentukan jaringan tubuh baru
        
        Tips: Pilih karbohidrat kompleks seperti nasi, kentang, dan roti gandum.
        """
    
    elif usia <= 12:
        return """
        🍞 **Insight Karbohidrat - Masa Anak-anak**
        
        Pada masa anak-anak, kebutuhan karbohidrat meningkat karena:
        - Aktivitas fisik yang tinggi (bermain, belajar)
        - Pertumbuhan tinggi badan yang pesat
        - Kebutuhan energi untuk fungsi kognitif di sekolah
        
        Tips: Kombinasikan karbohidrat dengan protein untuk energi berkelanjutan.
        """
    
    elif usia <= 18:
        return """
        🍞 **Insight Karbohidrat - Masa Remaja**
        
        Masa remaja adalah puncak kebutuhan energi karena:
        - Growth spurt (percepatan pertumbuhan)
        - Perkembangan hormon dan massa otot
        - Aktivitas fisik dan mental yang intens
        
        Tips: Hindari karbohidrat olahan berlebihan, pilih whole grains.
        """
    
    elif usia <= 29:
        return """
        🍞 **Insight Karbohidrat - Dewasa Muda**
        
        Pada usia dewasa muda, karbohidrat berperan untuk:
        - Menjaga performa kerja dan produktivitas
        - Sumber energi untuk aktivitas fisik
        - Mendukung metabolisme yang masih optimal
        
        Tips: Seimbangkan asupan dengan aktivitas fisik untuk mencegah penumpukan lemak.
        """
    
    elif usia <= 49:
        return """
        🍞 **Insight Karbohidrat - Dewasa**
        
        Pada usia dewasa, perlu diperhatikan:
        - Metabolisme mulai melambat
        - Risiko resistensi insulin meningkat
        - Kebutuhan energi menurun seiring berkurangnya aktivitas
        
        Tips: Kurangi karbohidrat sederhana, tingkatkan serat dari sayuran.
        """
    
    elif usia <= 64:
        return """
        🍞 **Insight Karbohidrat - Pra-Lansia**
        
        Pada usia pra-lansia, penting untuk:
        - Menjaga kadar gula darah tetap stabil
        - Mencegah sindrom metabolik
        - Memilih karbohidrat dengan indeks glikemik rendah
        
        Tips: Pilih karbohidrat kompleks seperti oatmeal, quinoa, dan brown rice.
        """
    
    else:
        return """
        🍞 **Insight Karbohidrat - Lansia**
        
        Pada usia lansia, fokus pada:
        - Menjaga energi tanpa meningkatkan gula darah drastis
        - Karbohidrat tinggi serat untuk kesehatan pencernaan
        - Porsi lebih kecil tapi lebih sering
        
        Tips: Kombinasikan dengan protein untuk mencegah sarcopenia (kehilangan massa otot).
        """


def generate_carbohydrate_data() -> pd.DataFrame:
    """
    Membuat DataFrame simulasi kebutuhan karbohidrat untuk semua kelompok usia.
    Berguna untuk visualisasi grafik.
    
    Returns:
    --------
    pd.DataFrame : Data kebutuhan karbohidrat per usia
    """
    
    data = []
    
    for jk in ['Laki-laki', 'Perempuan']:
        for usia in range(1, 101):
            hasil = calculate_carbohydrate_needs(usia, jk)
            data.append({
                'Usia': usia,
                'Jenis Kelamin': jk,
                'Karbohidrat (g)': hasil['kebutuhan_gram'],
                'Kalori dari Karbohidrat': hasil['kalori']
            })
    
    return pd.DataFrame(data)
