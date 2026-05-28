from functools import lru_cache
from pathlib import Path
import json

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "nutriage_macro_model.joblib"
METADATA_PATH = ROOT_DIR / "models" / "nutriage_macro_model_metadata.json"
TARGET_COLUMNS = ["carbohydrate_g", "protein_g", "lipid_g"]
APP_GENDERS = ["Laki-laki", "Perempuan"]


def _normalize_gender(jenis_kelamin: str) -> str:
    gender = str(jenis_kelamin).strip().lower()
    if gender in {"laki-laki", "laki laki", "male", "m"}:
        return "Male"
    if gender in {"perempuan", "female", "f"}:
        return "Female"
    raise ValueError(f"Jenis kelamin tidak valid: {jenis_kelamin}")


@lru_cache(maxsize=1)
def load_nutriage_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model NutriAge tidak ditemukan: {MODEL_PATH}")

    import joblib

    model = joblib.load(MODEL_PATH)
    metadata = {}
    if METADATA_PATH.exists():
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            metadata = json.load(f)

    return model, metadata


def _macro_result(usia: int, jenis_kelamin: str, gram: float, calories_per_gram: int) -> dict:
    kebutuhan = round(max(float(gram), 0.0), 1)
    kalori = round(kebutuhan * calories_per_gram, 1)
    total_kalori_harian = 2500 if jenis_kelamin == "Laki-laki" else 2000

    return {
        "kebutuhan_gram": kebutuhan,
        "kalori": kalori,
        "persentase_kalori": round((kalori / total_kalori_harian) * 100, 1),
        "usia": usia,
        "jenis_kelamin": jenis_kelamin,
        "satuan": "gram/hari",
    }


def predict_macro_needs(usia: int, jenis_kelamin: str) -> dict:
    model, metadata = load_nutriage_model()
    gender_model = _normalize_gender(jenis_kelamin)
    usia_int = int(usia)

    input_df = pd.DataFrame([{"age": usia_int, "gender": gender_model}])
    prediction = model.predict(input_df)[0]
    target_columns = metadata.get("target_columns", TARGET_COLUMNS)
    values = dict(zip(target_columns, prediction))

    carbohydrate = _macro_result(
        usia_int, jenis_kelamin, values["carbohydrate_g"], calories_per_gram=4
    )
    protein = _macro_result(
        usia_int, jenis_kelamin, values["protein_g"], calories_per_gram=4
    )
    lipid = _macro_result(
        usia_int, jenis_kelamin, values["lipid_g"], calories_per_gram=9
    )
    lipid["lemak_jenuh_max"] = round(lipid["kebutuhan_gram"] * 0.10, 1)
    lipid["lemak_tak_jenuh"] = round(lipid["kebutuhan_gram"] * 0.90, 1)

    return {
        "karbohidrat": carbohydrate,
        "protein": protein,
        "lipid": lipid,
        "source": "Model ML",
        "metadata": metadata,
    }


def _fallback_macro_data(age_min: int, age_max: int, genders: list[str]):
    from modules.carbohydrate import generate_carbohydrate_data
    from modules.protein import generate_protein_data
    from modules.lipid import generate_lipid_data

    def filt(df: pd.DataFrame) -> pd.DataFrame:
        return df[
            (df["Usia"] >= age_min)
            & (df["Usia"] <= age_max)
            & (df["Jenis Kelamin"].isin(genders))
        ].reset_index(drop=True)

    return (
        filt(generate_carbohydrate_data()),
        filt(generate_protein_data()),
        filt(generate_lipid_data()),
        "Kalkulator fallback",
    )


def generate_model_macro_data(age_min: int = 1, age_max: int = 100, genders=None):
    age_min = max(1, int(age_min))
    age_max = min(100, int(age_max))
    selected_genders = APP_GENDERS if genders is None else list(genders)
    selected_genders = [g for g in selected_genders if g in APP_GENDERS]

    if age_min > age_max or not selected_genders:
        empty_k = pd.DataFrame(columns=["Usia", "Jenis Kelamin", "Karbohidrat (g)", "Kalori dari Karbohidrat"])
        empty_p = pd.DataFrame(columns=["Usia", "Jenis Kelamin", "Protein (g)", "Kalori dari Protein"])
        empty_l = pd.DataFrame(columns=["Usia", "Jenis Kelamin", "Lipid (g)", "Kalori dari Lipid"])
        return empty_k, empty_p, empty_l, "Model ML"

    try:
        model, metadata = load_nutriage_model()
        rows = [
            {"Usia": age, "Jenis Kelamin": gender, "age": age, "gender": _normalize_gender(gender)}
            for gender in selected_genders
            for age in range(age_min, age_max + 1)
        ]
        input_df = pd.DataFrame(rows)
        predictions = model.predict(input_df[["age", "gender"]])
        target_columns = metadata.get("target_columns", TARGET_COLUMNS)
        pred_df = pd.DataFrame(predictions, columns=target_columns)
        result_df = pd.concat(
            [input_df[["Usia", "Jenis Kelamin"]].reset_index(drop=True), pred_df],
            axis=1,
        )

        result_df[TARGET_COLUMNS] = result_df[TARGET_COLUMNS].clip(lower=0).round(1)

        carbohydrate_df = result_df[["Usia", "Jenis Kelamin", "carbohydrate_g"]].rename(
            columns={"carbohydrate_g": "Karbohidrat (g)"}
        )
        carbohydrate_df["Kalori dari Karbohidrat"] = (carbohydrate_df["Karbohidrat (g)"] * 4).round(1)

        protein_df = result_df[["Usia", "Jenis Kelamin", "protein_g"]].rename(
            columns={"protein_g": "Protein (g)"}
        )
        protein_df["Kalori dari Protein"] = (protein_df["Protein (g)"] * 4).round(1)

        lipid_df = result_df[["Usia", "Jenis Kelamin", "lipid_g"]].rename(
            columns={"lipid_g": "Lipid (g)"}
        )
        lipid_df["Kalori dari Lipid"] = (lipid_df["Lipid (g)"] * 9).round(1)

        return (
            carbohydrate_df.reset_index(drop=True),
            protein_df.reset_index(drop=True),
            lipid_df.reset_index(drop=True),
            "Model ML",
        )
    except Exception:
        return _fallback_macro_data(age_min, age_max, selected_genders)
