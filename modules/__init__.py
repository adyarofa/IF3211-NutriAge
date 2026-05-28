# =============================================================================
# NutriAge - Modul Makromolekul
# =============================================================================
# File ini berfungsi untuk menginisialisasi package modules
# sehingga modul-modul dapat diimport dengan mudah

from .carbohydrate import calculate_carbohydrate_needs, get_carbohydrate_insight
from .protein import calculate_protein_needs, get_protein_insight
from .lipid import calculate_lipid_needs, get_lipid_insight
from .integration import run_simulation, generate_combined_data

__all__ = [
    'calculate_carbohydrate_needs',
    'get_carbohydrate_insight',
    'calculate_protein_needs',
    'get_protein_insight',
    'calculate_lipid_needs',
    'get_lipid_insight',
    'run_simulation',
    'generate_combined_data',
]
