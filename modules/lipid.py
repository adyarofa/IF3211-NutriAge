# =============================================================================
# NutriAge - Modul Lipid (Lemak)
# =============================================================================
# Modul ini menghitung kebutuhan lipid berdasarkan usia dan jenis kelamin
# Referensi: Angka Kecukupan Gizi (AKG) Indonesia & WHO Guidelines

import pandas as pd
import numpy as np

def calculate_lipid_needs(usia: int, jenis_kelamin: str) -> dict:
    """
    Menghitung kebutuhan lipid (lemak) harian berdasarkan usia dan jenis kelamin.
    
    Parameters:
    -----------
    usia : int
        Usia pengguna dalam tahun
    jenis_kelamin : str
        'Laki-laki' atau 'Perempuan'
    
    Returns:
    --------
    dict : Dictionary berisi kebutuhan lipid dan detail lainnya
    """
    
    # Tabel kebutuhan lipid berdasarkan kelompok usia (gram/hari)
    # Sumber: Adaptasi dari AKG Indonesia (20-35% total kalori)
    kebutuhan_tabel = {
        'Laki-laki': {
            (0, 5): 45,
            (6, 9): 50,
            (10, 12): 65,
            (13, 15): 80,
            (16, 18): 85,
            (19, 29): 75,
            (30, 49): 70,
            (50, 64): 60,
            (65, 80): 55,
            (81, 120): 50
        },
        'Perempuan': {
            (0, 5): 45,
            (6, 9): 50,
            (10, 12): 60,
            (13, 15): 70,
            (16, 18): 70,
            (19, 29): 65,
            (30, 49): 60,
            (50, 64): 50,
            (65, 80): 45,
            (81, 120): 42
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
            kebutuhan = 45
        else:
            kebutuhan = 42 if jenis_kelamin == 'Perempuan' else 50
    
    # Hitung kalori dari lipid (1 gram = 9 kkal)
    kalori = kebutuhan * 9
    
    # Hitung persentase dari total kalori harian
    total_kalori_harian = 2500 if jenis_kelamin == 'Laki-laki' else 2000
    persentase = (kalori / total_kalori_harian) * 100
    
    # Hitung rekomendasi jenis lemak
    saturated = round(kebutuhan * 0.10, 1)  # Max 10% saturated
    unsaturated = round(kebutuhan * 0.90, 1)  # 90% unsaturated
    
    return {
        'kebutuhan_gram': kebutuhan,
        'kalori': kalori,
        'persentase_kalori': round(persentase, 1),
        'lemak_jenuh_max': saturated,
        'lemak_tak_jenuh': unsaturated,
        'usia': usia,
        'jenis_kelamin': jenis_kelamin,
        'satuan': 'gram/hari'
    }


def get_lipid_insight(usia: int, jenis_kelamin: str) -> str:
    """
    Memberikan insight biologis tentang kebutuhan lipid berdasarkan usia.
    
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
        🥑 **Insight Lipid - Masa Balita**
        
        Lemak sangat penting pada masa balita untuk:
        - Perkembangan otak (otak terdiri dari ~60% lemak)
        - Penyerapan vitamin larut lemak (A, D, E, K)
        - Pembentukan membran sel dan myelin saraf
        
        Tips: Berikan lemak sehat dari ASI, alpukat, dan minyak zaitun.
        """
    
    elif usia <= 12:
        return """
        🥑 **Insight Lipid - Masa Anak-anak**
        
        Pada masa anak-anak, lemak berperan untuk:
        - Sumber energi cadangan untuk aktivitas
        - Perkembangan sistem saraf dan otak
        - Produksi hormon pertumbuhan
        
        Tips: Batasi lemak jenuh, perbanyak omega-3 dari ikan.
        """
    
    elif usia <= 18:
        return """
        🥑 **Insight Lipid - Masa Remaja**
        
        Remaja membutuhkan lemak sehat untuk:
        - Produksi hormon seksual
        - Perkembangan sistem reproduksi
        - Energi untuk aktivitas fisik intens
        
        Tips: Hindari trans fat dari makanan olahan dan fast food.
        """
    
    elif usia <= 29:
        return """
        🥑 **Insight Lipid - Dewasa Muda**
        
        Pada usia dewasa muda, perhatikan:
        - Keseimbangan omega-3 dan omega-6
        - Membatasi lemak jenuh untuk kesehatan jantung
        - Lemak sebagai sumber energi berkelanjutan
        
        Tips: Konsumsi ikan 2-3x seminggu untuk omega-3.
        """
    
    elif usia <= 49:
        return """
        🥑 **Insight Lipid - Dewasa**
        
        Pada usia dewasa, fokus pada:
        - Mencegah penumpukan kolesterol
        - Memilih lemak tak jenuh (MUFA, PUFA)
        - Menjaga profil lipid darah tetap sehat
        
        Tips: Ganti mentega dengan minyak zaitun atau canola.
        """
    
    elif usia <= 64:
        return """
        🥑 **Insight Lipid - Pra-Lansia**
        
        Pada usia pra-lansia, penting untuk:
        - Mencegah aterosklerosis (penyumbatan pembuluh darah)
        - Menjaga elastisitas pembuluh darah
        - Omega-3 untuk kesehatan jantung dan otak
        
        Tips: Rutin cek profil lipid dan batasi gorengan.
        """
    
    else:
        return """
        🥑 **Insight Lipid - Lansia**
        
        Pada usia lansia, lemak berperan untuk:
        - Menjaga fungsi kognitif (mencegah demensia)
        - Penyerapan vitamin larut lemak
        - Sumber energi yang mudah dicerna
        
        Tips: Pilih sumber lemak sehat seperti ikan, kacang, dan alpukat.
        """


def generate_lipid_data() -> pd.DataFrame:
    """
    Membuat DataFrame simulasi kebutuhan lipid untuk semua kelompok usia.
    Berguna untuk visualisasi grafik.
    
    Returns:
    --------
    pd.DataFrame : Data kebutuhan lipid per usia
    """
    
    data = []
    
    for jk in ['Laki-laki', 'Perempuan']:
        for usia in range(1, 101):
            hasil = calculate_lipid_needs(usia, jk)
            data.append({
                'Usia': usia,
                'Jenis Kelamin': jk,
                'Lipid (g)': hasil['kebutuhan_gram'],
                'Kalori dari Lipid': hasil['kalori']
            })
    
    return pd.DataFrame(data)
