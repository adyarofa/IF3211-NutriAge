# =============================================================================
# NutriAge - Modul Protein
# =============================================================================
# Modul ini menghitung kebutuhan protein berdasarkan usia dan jenis kelamin
# Referensi: Angka Kecukupan Gizi (AKG) Indonesia & WHO Guidelines

import pandas as pd
import numpy as np

def calculate_protein_needs(usia: int, jenis_kelamin: str) -> dict:
    """
    Menghitung kebutuhan protein harian berdasarkan usia dan jenis kelamin.
    
    Parameters:
    -----------
    usia : int
        Usia pengguna dalam tahun
    jenis_kelamin : str
        'Laki-laki' atau 'Perempuan'
    
    Returns:
    --------
    dict : Dictionary berisi kebutuhan protein dan detail lainnya
    """
    
    # Tabel kebutuhan protein berdasarkan kelompok usia (gram/hari)
    # Sumber: Adaptasi dari AKG Indonesia dan WHO (0.8-1.2 g/kg BB)
    kebutuhan_tabel = {
        'Laki-laki': {
            (0, 5): 20,
            (6, 9): 35,
            (10, 12): 50,
            (13, 15): 70,
            (16, 18): 75,
            (19, 29): 65,
            (30, 49): 65,
            (50, 64): 65,
            (65, 80): 64,
            (81, 120): 62
        },
        'Perempuan': {
            (0, 5): 20,
            (6, 9): 35,
            (10, 12): 55,
            (13, 15): 65,
            (16, 18): 65,
            (19, 29): 60,
            (30, 49): 57,
            (50, 64): 56,
            (65, 80): 56,
            (81, 120): 54
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
            kebutuhan = 20
        else:
            kebutuhan = 54 if jenis_kelamin == 'Perempuan' else 62
    
    # Hitung kalori dari protein (1 gram = 4 kkal)
    kalori = kebutuhan * 4
    
    # Hitung persentase dari total kalori harian
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


def get_protein_insight(usia: int, jenis_kelamin: str) -> str:
    """
    Memberikan insight biologis tentang kebutuhan protein berdasarkan usia.
    
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
        🥩 **Insight Protein - Masa Balita**
        
        Protein pada masa balita sangat krusial untuk:
        - Pembentukan jaringan tubuh baru (otot, organ, kulit)
        - Sintesis enzim dan hormon pertumbuhan
        - Perkembangan sistem imun yang kuat
        
        Tips: Berikan protein dari berbagai sumber (hewani dan nabati).
        """
    
    elif usia <= 12:
        return """
        🥩 **Insight Protein - Masa Anak-anak**
        
        Pada masa anak-anak, protein mendukung:
        - Pertumbuhan tinggi badan optimal
        - Perkembangan otot dan tulang
        - Fungsi kognitif dan konsentrasi belajar
        
        Tips: Kombinasikan telur, ikan, tempe, dan tahu dalam menu harian.
        """
    
    elif usia <= 18:
        return """
        🥩 **Insight Protein - Masa Remaja**
        
        Remaja membutuhkan protein tinggi karena:
        - Pembentukan massa otot yang pesat
        - Perubahan hormonal signifikan
        - Mendukung aktivitas fisik dan olahraga
        
        Tips: Konsumsi protein setiap makan utama untuk distribusi optimal.
        """
    
    elif usia <= 29:
        return """
        🥩 **Insight Protein - Dewasa Muda**
        
        Pada usia dewasa muda, protein berperan untuk:
        - Mempertahankan massa otot
        - Mendukung metabolisme yang aktif
        - Repair jaringan setelah aktivitas fisik
        
        Tips: 1.0-1.2 g/kg BB untuk yang aktif berolahraga.
        """
    
    elif usia <= 49:
        return """
        🥩 **Insight Protein - Dewasa**
        
        Pada usia dewasa, perhatikan:
        - Menjaga massa otot dari degradasi
        - Protein berkualitas tinggi (complete amino acids)
        - Distribusi protein merata sepanjang hari
        
        Tips: Pilih lean protein seperti ikan, ayam tanpa kulit, dan legumes.
        """
    
    elif usia <= 64:
        return """
        🥩 **Insight Protein - Pra-Lansia**
        
        Pada usia pra-lansia, fokus pada:
        - Mencegah sarcopenia (kehilangan massa otot)
        - Menjaga kekuatan dan mobilitas
        - Protein dengan leucine tinggi (telur, dairy, daging)
        
        Tips: Tingkatkan asupan protein 15-20% dari rekomendasi dewasa.
        """
    
    else:
        return """
        🥩 **Insight Protein - Lansia**
        
        Pada usia lansia, protein sangat penting untuk:
        - Mencegah frailty syndrome (kelemahan)
        - Menjaga massa otot dan kekuatan tulang
        - Mendukung sistem imun yang melemah
        
        Tips: Konsumsi protein 1.0-1.2 g/kg BB dengan tekstur mudah dicerna.
        """


def generate_protein_data() -> pd.DataFrame:
    """
    Membuat DataFrame simulasi kebutuhan protein untuk semua kelompok usia.
    Berguna untuk visualisasi grafik.
    
    Returns:
    --------
    pd.DataFrame : Data kebutuhan protein per usia
    """
    
    data = []
    
    for jk in ['Laki-laki', 'Perempuan']:
        for usia in range(1, 101):
            hasil = calculate_protein_needs(usia, jk)
            data.append({
                'Usia': usia,
                'Jenis Kelamin': jk,
                'Protein (g)': hasil['kebutuhan_gram'],
                'Kalori dari Protein': hasil['kalori']
            })
    
    return pd.DataFrame(data)
