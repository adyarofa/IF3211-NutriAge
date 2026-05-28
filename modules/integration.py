import pandas as pd

from .carbohydrate import calculate_carbohydrate_needs, generate_carbohydrate_data
from .protein import calculate_protein_needs, generate_protein_data
from .lipid import calculate_lipid_needs, generate_lipid_data


def run_simulation(usia: int, jenis_kelamin: str) -> dict:
    """
    Pipeline terpadu: jalankan simulasi ketiga makromolekul sekaligus.

    Returns dict dengan keys: 'karbohidrat', 'protein', 'lipid'
    Masing-masing berisi hasil dari modul yang bersangkutan.
    """
    return {
        "karbohidrat": calculate_carbohydrate_needs(usia, jenis_kelamin),
        "protein":     calculate_protein_needs(usia, jenis_kelamin),
        "lipid":       calculate_lipid_needs(usia, jenis_kelamin),
    }


def generate_combined_data() -> pd.DataFrame:
    """
    Gabungkan dataset ketiga makromolekul jadi satu DataFrame utuh.

    Kolom: Usia, Jenis Kelamin, Karbohidrat (g), Protein (g), Lipid (g),
           Kalori Karbohidrat, Kalori Protein, Kalori Lipid, Total Kalori (kkal)
    """
    df_k = generate_carbohydrate_data()
    df_p = generate_protein_data()
    df_l = generate_lipid_data()

    df = df_k.merge(df_p, on=["Usia", "Jenis Kelamin"])
    df = df.merge(df_l, on=["Usia", "Jenis Kelamin"])

    df["Total Kalori (kkal)"] = (
        df["Kalori dari Karbohidrat"]
        + df["Kalori dari Protein"]
        + df["Kalori dari Lipid"]
    )

    return df
