import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.carbohydrate import calculate_carbohydrate_needs, get_carbohydrate_insight, generate_carbohydrate_data
from modules.protein import calculate_protein_needs, get_protein_insight, generate_protein_data
from modules.lipid import calculate_lipid_needs, get_lipid_insight, generate_lipid_data
from utils.helpers import (
    COLORS, MACRO_COLORS, get_age_category, format_number,
    calculate_total_calories, get_calorie_distribution,
    create_summary_dataframe, get_healthy_aging_tips
)

st.set_page_config(
    page_title="NutriAge",
    page_icon="public/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO     = img_b64("public/logo.png")
LOGO_NAME = img_b64("public/logo-name.png")

# ── Colour tokens ──────────────────────────────────────────────
C = {
    "karbo":   "#F99C01",
    "protein": "#FF006E",
    "lipid":   "#748C2C",
    "purple":  "#A07ED2",
    "bg":      "#F4F3EF",
    "surface": "#FFFFFF",
    "border":  "#E8E8E8",
    "text":    "#1A1A1A",
    "muted":   "#888888",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* ── reset streamlit chrome ── */
html, body {{ overflow-x: hidden; }}
html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarUserContent"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {{ display: none !important; width: 0 !important; }}
/* paksa scrollbar selalu ada di scroll container Streamlit */
[data-testid="stAppViewContainer"] {{ overflow-y: scroll !important; }}
.stApp {{ overflow-x: hidden; }}
.stApp > .main, [data-testid="stMain"] {{ margin-left: 0 !important; }}
/* min-height supaya semua page selalu cukup tinggi → scrollbar tidak muncul-hilang */
.block-container {{ padding: 2rem 3rem 4rem 3rem !important; max-width: 1400px !important; min-height: 110vh !important; }}

/* ── page background ── */
.stApp {{ background: {C["bg"]}; }}

/* ── navbar ── */
.navbar {{
    display: flex;
    align-items: center;
    background: {C["surface"]};
    border-radius: 16px;
    padding: 0 1.5rem;
    height: 64px;
    box-shadow: 0 2px 12px rgba(0,0,0,.06);
    margin-bottom: 2rem;
    gap: 2rem;
}}
.navbar-logo {{ height: 28px; }}
.navbar-links {{ display: flex; gap: 4px; margin-left: auto; }}
.nav-btn {{
    padding: .45rem 1.1rem;
    border-radius: 10px;
    font-size: .9rem;
    font-weight: 500;
    color: {C["muted"]};
    cursor: pointer;
    border: none;
    background: transparent;
    transition: .15s;
    text-decoration: none;
}}
.nav-btn:hover {{ background: #F0EDF8; color: {C["purple"]}; }}
.nav-btn.active {{ background: #F0EDF8; color: {C["purple"]}; font-weight: 700; }}

/* ── hero banner ── */
.hero {{
    background: linear-gradient(130deg, {C["purple"]} 0%, #C97BB2 55%, {C["protein"]} 100%);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    display: flex;
    align-items: center;
    gap: 2rem;
}}
.hero img {{ width: 72px; height: 72px; object-fit: contain; }}
.hero h1 {{ color: #fff; font-size: 2.4rem; font-weight: 800; margin: 0 0 .35rem; }}
.hero p  {{ color: rgba(255,255,255,.85); font-size: 1.05rem; margin: 0; }}

/* ── section title ── */
.sec {{ font-size: 1.1rem; font-weight: 700; color: {C["text"]}; margin: 2.5rem 0 1rem; }}

/* ── white card ── */
.card {{
    background: {C["surface"]};
    border-radius: 16px;
    padding: 1.75rem;
    box-shadow: 0 2px 12px rgba(0,0,0,.05);
    height: 100%;
}}

/* ── macro feature card ── */
.mcard {{
    background: {C["surface"]};
    border-radius: 16px;
    padding: 1.75rem 1.5rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,.05);
    border-top: 4px solid;
}}
.mcard-title {{ font-size: 1.25rem; font-weight: 700; margin-bottom: .5rem; }}
.mcard-desc  {{ font-size: .88rem; color: {C["muted"]}; line-height: 1.5; }}

/* ── metric result card ── */
.rcard {{
    background: {C["surface"]};
    border-radius: 16px;
    padding: 2rem 1.25rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,.05);
    border-top: 4px solid;
}}
.rcard-val {{ font-size: 3rem; font-weight: 800; line-height: 1; margin-bottom: .4rem; }}
.rcard-lbl {{ font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: {C["muted"]}; }}
.rcard-sub {{ font-size: .85rem; color: #BBB; margin-top: .3rem; }}

/* ── stat card ── */
.scard {{
    background: {C["surface"]};
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,.05);
    border: 1.5px solid {C["border"]};
}}
.scard-val {{ font-size: 1.8rem; font-weight: 800; color: {C["purple"]}; }}
.scard-lbl {{ font-size: .8rem; font-weight: 600; color: {C["muted"]}; text-transform: uppercase; letter-spacing: .06em; margin-top: .25rem; }}

/* ── insight card ── */
.icard {{
    background: {C["surface"]};
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,.05);
    border-left: 5px solid;
    font-size: .9rem;
    line-height: 1.65;
    color: #333;
}}

/* ── tip card ── */
.tcard {{
    background: {C["surface"]};
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,.04);
    font-size: .9rem;
    color: #444;
    line-height: 1.6;
    margin-bottom: .75rem;
    border-left: 4px solid {C["purple"]};
}}

/* ── steps list ── */
.steps {{ list-style: none; padding: 0; margin: 0; counter-reset: s; }}
.steps li {{
    counter-increment: s;
    display: flex; align-items: flex-start; gap: .9rem;
    padding: .75rem 0; border-bottom: 1px solid #F0F0F0;
    font-size: .92rem; color: #444;
}}
.steps li:last-child {{ border-bottom: none; }}
.steps li::before {{
    content: counter(s);
    display: flex; align-items: center; justify-content: center;
    min-width: 26px; height: 26px;
    border-radius: 50%; background: {C["purple"]}; color: #fff;
    font-size: .78rem; font-weight: 700; flex-shrink: 0; margin-top: 1px;
}}

/* ── feature pill ── */
.pill {{
    display: inline-block;
    background: #F0EDF8; color: {C["purple"]};
    font-size: .82rem; font-weight: 600;
    padding: .35rem 1rem; border-radius: 50px; margin: .2rem;
}}

/* ── divider ── */
.div {{ height: 1px; background: {C["border"]}; margin: 2rem 0; }}

/* ── swatch ── */
.swatch {{ display: flex; align-items: center; gap: .75rem; margin-bottom: .6rem; }}
.swatch-box {{ width: 30px; height: 30px; border-radius: 7px; flex-shrink: 0; }}
.swatch-hex {{ margin-left: auto; font-size: .78rem; color: #AAA; font-family: monospace !important; }}

/* ── colour palette ── */
.pal-row {{ display: flex; gap: .5rem; margin-bottom: .5rem; }}
.pal-chip {{
    flex: 1; height: 44px; border-radius: 8px;
    display: flex; align-items: flex-end; justify-content: center;
    padding-bottom: .3rem;
    font-size: .7rem; font-weight: 600; color: rgba(255,255,255,.85);
}}

/* ── semua tombol default (action buttons) ── */
.stButton > button {{
    background: linear-gradient(135deg, {C["purple"]} 0%, {C["protein"]} 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: .7rem 1.5rem !important;
    font-weight: 700 !important; font-size: .95rem !important;
    width: 100% !important; transition: opacity .2s !important;
    box-shadow: 0 2px 8px rgba(160,126,210,.25) !important;
}}
.stButton > button:hover {{ opacity: .85 !important; }}

/* ── nav tombol: kolom 3–6 di horizontal block pertama ── */
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(n+3) .stButton > button {{
    background: transparent !important;
    color: #888 !important;
    border: none !important; box-shadow: none !important;
    border-radius: 10px !important;
    padding: .45rem 1rem !important;
    font-size: .9rem !important; font-weight: 500 !important;
    width: 100% !important;
    transition: all .2s !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(n+3) .stButton > button:hover {{
    background: linear-gradient(135deg, {C["purple"]} 0%, {C["protein"]} 100%) !important;
    color: #fff !important;
    box-shadow: 0 3px 10px rgba(160,126,210,.35) !important;
    opacity: 1 !important;
}}

[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] > div,
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] > div {{
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
    font-size: .95rem !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: #EDEAF6; border-radius: 12px; padding: 4px; gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 9px; font-size: .9rem; font-weight: 500;
    padding: .45rem 1.1rem;
}}
.stTabs [aria-selected="true"] {{
    background: {C["surface"]} !important; font-weight: 700 !important;
}}

/* ── footer ── */
.footer {{
    text-align: center; padding: 2.5rem 1rem;
    color: #BBB; font-size: .82rem;
    border-top: 1px solid {C["border"]}; margin-top: 4rem;
}}
</style>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'


def md_to_html(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text.strip())
    lines = [
        f'&nbsp;&nbsp;• {l.strip()[2:]}' if l.strip().startswith('- ') else l.strip()
        for l in text.split('\n') if l.strip()
    ]
    return '<br>'.join(lines)


# ══════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

PAGES = ["Beranda", "Simulasi Nutrisi", "Analisis Data", "Tentang"]

# ══════════════════════════════════════════════════════════════
# NAVBAR — tombol Streamlit murni, tanpa overlay trick
# ══════════════════════════════════════════════════════════════
nb_logo_col, nb_spacer, nb_b1, nb_b2, nb_b3, nb_b4 = st.columns([2, 1.5, 1, 1.2, 1, 0.8])

with nb_logo_col:
    st.markdown(
        f'<div style="display:flex;align-items:center;padding:.75rem 0;">'
        f'<img src="data:image/png;base64,{LOGO_NAME}" style="height:26px;object-fit:contain;"/>'
        f'</div>',
        unsafe_allow_html=True
    )

for col, lbl in [(nb_b1, "Beranda"), (nb_b2, "Simulasi Nutrisi"),
                 (nb_b3, "Analisis Data"), (nb_b4, "Tentang")]:
    with col:
        if st.button(lbl, key=f"nav_{lbl}"):
            st.session_state.page = lbl
            st.rerun()

# highlight tombol aktif — nth-child: logo=1, spacer=2, nav=3,4,5,6
active_page = st.session_state.page
active_idx = {"Beranda": 3, "Simulasi Nutrisi": 4, "Analisis Data": 5, "Tentang": 6}[active_page]
st.markdown(f"""
<style>
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child({active_idx}) .stButton > button {{
    background: linear-gradient(135deg, {C["purple"]} 0%, {C["protein"]} 100%) !important;
    color: #fff !important;
    font-weight: 700 !important;
    box-shadow: 0 3px 10px rgba(160,126,210,.35) !important;
    opacity: 1 !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child({active_idx}) .stButton > button:hover {{
    opacity: .88 !important;
}}
</style>
""", unsafe_allow_html=True)

page = st.session_state.page


# ══════════════════════════════════════════════════════════════
# HERO helper
# ══════════════════════════════════════════════════════════════
def hero(title, subtitle, show_logo=True):
    logo_html = (
        f'<img src="data:image/png;base64,{LOGO}" '
        f'style="width:72px;height:72px;object-fit:contain;flex-shrink:0;"/>'
        if show_logo else ""
    )
    st.markdown(
        f'<div class="hero">{logo_html}'
        f'<div><h1>{title}</h1><p>{subtitle}</p></div></div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════
# BERANDA
# ══════════════════════════════════════════════════════════════
if page == "Beranda":
    hero("NutriAge", "Simulasi Kebutuhan Nutrisi Makromolekul Berdasarkan Usia")

    # row 1: deskripsi + cara pakai
    c1, c2 = st.columns([3, 2], gap="large")

    with c1:
        st.markdown('<p class="sec">Tentang NutriAge</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <p style="font-size:.95rem;line-height:1.75;color:#444;margin:0;">
            <strong>NutriAge</strong> adalah aplikasi simulasi interaktif untuk memahami
            kebutuhan nutrisi makromolekul berdasarkan usia dan jenis kelamin.
            Dikembangkan untuk mendukung <strong>Healthy Aging</strong> — proses menua
            secara sehat dengan asupan nutrisi yang tepat di setiap tahapan kehidupan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="sec" style="margin-top:1rem;">Makromolekul yang Dianalisis</p>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3, gap="medium")
        macros = [
            ("Karbohidrat", C["karbo"],   "Sumber energi utama tubuh"),
            ("Protein",     C["protein"], "Pembangun & pemulih jaringan"),
            ("Lipid",       C["lipid"],   "Cadangan energi & pelindung organ"),
        ]
        for col, (name, color, desc) in zip([m1, m2, m3], macros):
            with col:
                st.markdown(
                    f'<div class="mcard" style="border-color:{color};">'
                    f'<div class="mcard-title" style="color:{color};">{name}</div>'
                    f'<div class="mcard-desc">{desc}</div></div>',
                    unsafe_allow_html=True
                )

        st.markdown('<p class="sec" style="margin-top:1rem;">Fitur Utama</p>', unsafe_allow_html=True)
        pills = ["Kalkulasi personal", "Grafik interaktif", "Insight biologis",
                 "Tips healthy aging", "Analisis rentang usia"]
        st.markdown(
            "".join(f'<span class="pill">{p}</span>' for p in pills),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown('<p class="sec">Cara Penggunaan</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <ol class="steps">
                <li>Pilih menu <strong>Simulasi Nutrisi</strong></li>
                <li>Masukkan usia Anda</li>
                <li>Pilih jenis kelamin</li>
                <li>Klik tombol <strong>Hitung</strong></li>
                <li>Lihat hasil analisis nutrisi Anda</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="sec" style="margin-top:1rem;">Statistik</p>', unsafe_allow_html=True)
        s1, s2 = st.columns(2, gap="small")
        stats = [("1–100", "Rentang Usia"), ("3", "Makromolekul"),
                 ("7", "Kel. Usia"), ("AKG & WHO", "Referensi")]
        for i, (val, lbl) in enumerate(stats):
            with (s1 if i % 2 == 0 else s2):
                st.markdown(
                    f'<div class="scard" style="margin-bottom:.75rem;">'
                    f'<div class="scard-val">{val}</div>'
                    f'<div class="scard-lbl">{lbl}</div></div>',
                    unsafe_allow_html=True
                )


# ══════════════════════════════════════════════════════════════
# SIMULASI NUTRISI
# ══════════════════════════════════════════════════════════════
elif page == "Simulasi Nutrisi":
    hero("Simulasi Nutrisi", "Hitung kebutuhan makromolekul harian Anda", show_logo=False)

    st.markdown('<p class="sec">Data Diri</p>', unsafe_allow_html=True)

    fi1, fi2, fi3 = st.columns([1, 1, 1], gap="medium")
    with fi1:
        usia = st.number_input("Usia (tahun)", min_value=1, max_value=100, value=25, step=1)
    with fi2:
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    with fi3:
        st.markdown("<br>", unsafe_allow_html=True)
        hitung = st.button("Hitung Kebutuhan Nutrisi")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    if hitung or "hasil_karbo" in st.session_state:
        hk = calculate_carbohydrate_needs(usia, jenis_kelamin)
        hp = calculate_protein_needs(usia, jenis_kelamin)
        hl = calculate_lipid_needs(usia, jenis_kelamin)
        st.session_state.update(hasil_karbo=hk, hasil_protein=hp, hasil_lipid=hl,
                                usia=usia, jenis_kelamin=jenis_kelamin)

        cat = get_age_category(usia)
        total_kal = calculate_total_calories(hk["kebutuhan_gram"], hp["kebutuhan_gram"], hl["kebutuhan_gram"])
        total_g   = hk["kebutuhan_gram"] + hp["kebutuhan_gram"] + hl["kebutuhan_gram"]

        st.markdown(
            f'<p class="sec">Hasil untuk {jenis_kelamin}, {usia} tahun &nbsp;—&nbsp; '
            f'<span style="color:{C["purple"]}">{cat}</span></p>',
            unsafe_allow_html=True
        )

        rc1, rc2, rc3, rc4 = st.columns(4, gap="medium")
        rcards = [
            (hk["kebutuhan_gram"], "Karbohidrat", "gram",  f'{hk["kalori"]} kkal',  C["karbo"]),
            (hp["kebutuhan_gram"], "Protein",     "gram",  f'{hp["kalori"]} kkal',  C["protein"]),
            (hl["kebutuhan_gram"], "Lipid",        "gram",  f'{hl["kalori"]} kkal',  C["lipid"]),
            (int(total_kal),       "Total Kalori", "kkal",  f"{total_g}g makromolekul", C["purple"]),
        ]
        for col, (val, lbl, unit, sub, clr) in zip([rc1, rc2, rc3, rc4], rcards):
            with col:
                st.markdown(
                    f'<div class="rcard" style="border-color:{clr};">'
                    f'<div class="rcard-val" style="color:{clr};">{val}</div>'
                    f'<div class="rcard-lbl">{lbl} ({unit})</div>'
                    f'<div class="rcard-sub">{sub}</div></div>',
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # tabel + pie
        t1, t2 = st.columns([1, 1], gap="large")
        with t1:
            st.markdown('<p class="sec">Tabel Ringkasan</p>', unsafe_allow_html=True)
            df_sum = create_summary_dataframe(hk, hp, hl)
            st.dataframe(df_sum, hide_index=True, use_container_width=True)

        with t2:
            st.markdown('<p class="sec">Distribusi Kalori</p>', unsafe_allow_html=True)
            dist = get_calorie_distribution(hk["kebutuhan_gram"], hp["kebutuhan_gram"], hl["kebutuhan_gram"])
            fig_pie = go.Figure(go.Pie(
                labels=["Karbohidrat", "Protein", "Lipid"],
                values=[dist["Karbohidrat"], dist["Protein"], dist["Lipid"]],
                hole=.45,
                marker_colors=[C["karbo"], C["protein"], C["lipid"]],
                textinfo="label+percent",
                textfont=dict(family="Plus Jakarta Sans", size=13)
            ))
            fig_pie.update_layout(
                showlegend=False, height=300,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans")
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec">Grafik Kebutuhan Nutrisi Berdasarkan Usia</p>', unsafe_allow_html=True)

        df_k = generate_carbohydrate_data()
        df_p = generate_protein_data()
        df_l = generate_lipid_data()
        gk = df_k[df_k["Jenis Kelamin"] == jenis_kelamin]
        gp = df_p[df_p["Jenis Kelamin"] == jenis_kelamin]
        gl = df_l[df_l["Jenis Kelamin"] == jenis_kelamin]

        fig = go.Figure()
        for df_g, col_name, clr in [
            (gk, "Karbohidrat (g)", C["karbo"]),
            (gp, "Protein (g)",     C["protein"]),
            (gl, "Lipid (g)",       C["lipid"]),
        ]:
            fig.add_trace(go.Scatter(
                x=df_g["Usia"], y=df_g[col_name],
                mode="lines", name=col_name.replace(" (g)", ""),
                line=dict(color=clr, width=3)
            ))

        for yval, clr in [
            (hk["kebutuhan_gram"], C["karbo"]),
            (hp["kebutuhan_gram"], C["protein"]),
            (hl["kebutuhan_gram"], C["lipid"]),
        ]:
            fig.add_trace(go.Scatter(
                x=[usia], y=[yval], mode="markers", showlegend=False,
                marker=dict(color=clr, size=13, symbol="circle",
                            line=dict(color="white", width=2.5))
            ))

        fig.add_vline(x=usia, line_dash="dash", line_color=C["purple"], line_width=1.5,
                      annotation_text=f"Usia {usia}",
                      annotation_font=dict(color=C["purple"], size=12, family="Plus Jakarta Sans"))
        fig.update_layout(
            height=440, hovermode="x unified",
            xaxis_title="Usia (tahun)", yaxis_title="Kebutuhan (gram/hari)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#444"),
            xaxis=dict(showgrid=True, gridcolor="#EEEEEE", zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="#EEEEEE", zeroline=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec">Insight Biologis</p>', unsafe_allow_html=True)

        ic1, ic2, ic3 = st.columns(3, gap="medium")
        for col, text, clr in zip(
            [ic1, ic2, ic3],
            [get_carbohydrate_insight(usia, jenis_kelamin),
             get_protein_insight(usia, jenis_kelamin),
             get_lipid_insight(usia, jenis_kelamin)],
            [C["karbo"], C["protein"], C["lipid"]]
        ):
            with col:
                st.markdown(
                    f'<div class="icard" style="border-color:{clr};">{md_to_html(text)}</div>',
                    unsafe_allow_html=True
                )

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec">Tips Healthy Aging</p>', unsafe_allow_html=True)

        tips = get_healthy_aging_tips(usia)
        tc1, tc2, tc3 = st.columns(3, gap="medium")
        for i, tip in enumerate(tips):
            with [tc1, tc2, tc3][i % 3]:
                st.markdown(f'<div class="tcard">{tip}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ANALISIS DATA
# ══════════════════════════════════════════════════════════════
elif page == "Analisis Data":
    hero("Analisis Data", "Eksplorasi kebutuhan nutrisi berdasarkan usia dan jenis kelamin", show_logo=False)

    df_k = generate_carbohydrate_data()
    df_p = generate_protein_data()
    df_l = generate_lipid_data()

    st.markdown('<p class="sec">Filter Data</p>', unsafe_allow_html=True)
    af1, af2 = st.columns(2, gap="large")
    with af1:
        gender = st.selectbox("Jenis Kelamin", ["Semua", "Laki-laki", "Perempuan"])
    with af2:
        age_r = st.slider("Rentang Usia", 1, 100, (1, 100))

    def filt(df, gcol):
        d = df if gender == "Semua" else df[df["Jenis Kelamin"] == gender]
        return d[(d["Usia"] >= age_r[0]) & (d["Usia"] <= age_r[1])]

    fk, fp, fl = filt(df_k, "Karbohidrat (g)"), filt(df_p, "Protein (g)"), filt(df_l, "Lipid (g)")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    base_layout = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#444"),
        xaxis=dict(showgrid=True, gridcolor="#EEEEEE", zeroline=False, title="Usia (tahun)"),
        yaxis=dict(showgrid=True, gridcolor="#EEEEEE", zeroline=False, title="Kebutuhan (gram/hari)"),
        height=480, hovermode="x unified",
        legend=dict(orientation="h", y=-0.15),
        margin=dict(t=30, b=60, l=10, r=10)
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Grafik Gabungan", "Karbohidrat", "Protein", "Lipid"])

    with tab1:
        fig_all = go.Figure()
        for g in fk["Jenis Kelamin"].unique():
            ls = "solid" if g == "Laki-laki" else "dash"
            fig_all.add_trace(go.Scatter(x=fk[fk["Jenis Kelamin"]==g]["Usia"],
                y=fk[fk["Jenis Kelamin"]==g]["Karbohidrat (g)"],
                mode="lines", name=f"Karbohidrat ({g})",
                line=dict(color=C["karbo"], dash=ls, width=2.5)))
            fig_all.add_trace(go.Scatter(x=fp[fp["Jenis Kelamin"]==g]["Usia"],
                y=fp[fp["Jenis Kelamin"]==g]["Protein (g)"],
                mode="lines", name=f"Protein ({g})",
                line=dict(color=C["protein"], dash=ls, width=2.5)))
            fig_all.add_trace(go.Scatter(x=fl[fl["Jenis Kelamin"]==g]["Usia"],
                y=fl[fl["Jenis Kelamin"]==g]["Lipid (g)"],
                mode="lines", name=f"Lipid ({g})",
                line=dict(color=C["lipid"], dash=ls, width=2.5)))
        fig_all.update_layout(**base_layout)
        st.plotly_chart(fig_all, use_container_width=True)

    for tab, df_f, col_name, clr in [
        (tab2, fk, "Karbohidrat (g)", C["karbo"]),
        (tab3, fp, "Protein (g)",     C["protein"]),
        (tab4, fl, "Lipid (g)",       C["lipid"]),
    ]:
        with tab:
            fig_t = px.line(df_f, x="Usia", y=col_name, color="Jenis Kelamin",
                            color_discrete_map={"Laki-laki": clr, "Perempuan": hex_to_rgba(clr, 0.5)})
            fig_t.update_layout(**{**base_layout, "yaxis": {**base_layout["yaxis"], "title": col_name}})
            st.plotly_chart(fig_t, use_container_width=True)
            st.markdown('<p class="sec">Statistik</p>', unsafe_allow_html=True)
            st.dataframe(
                df_f.groupby("Jenis Kelamin")[col_name].describe().round(2),
                use_container_width=True
            )


# ══════════════════════════════════════════════════════════════
# TENTANG
# ══════════════════════════════════════════════════════════════
elif page == "Tentang":
    hero("Tentang NutriAge", "Informasi aplikasi, referensi ilmiah, dan teknologi")

    # ── Row 1: Deskripsi + Warna ──────────────────────────────
    r1a, r1b = st.columns([3, 2], gap="large")
    with r1a:
        st.markdown('<p class="sec">Deskripsi</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <p style="font-size:.95rem;line-height:1.75;color:#444;margin:0;">
            <strong>NutriAge</strong> adalah aplikasi simulasi berbasis web yang mensimulasikan
            kebutuhan nutrisi makromolekul (karbohidrat, lipid, dan protein) berdasarkan usia
            dan jenis kelamin. Dikembangkan sebagai alat edukasi komputasional untuk mendukung
            pemahaman tentang <em>Healthy Aging</em> — proses menua secara sehat dengan asupan
            nutrisi yang tepat di setiap tahapan kehidupan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r1b:
        st.markdown('<p class="sec">Warna Makromolekul</p>', unsafe_allow_html=True)
        macros_sw = "".join(
            f'<div class="swatch">'
            f'<div class="swatch-box" style="background:{c};"></div>'
            f'<span style="font-size:.9rem;">{n}</span>'
            f'<span class="swatch-hex">{c}</span></div>'
            for n, c in [("Karbohidrat", C["karbo"]),
                         ("Protein",     C["protein"]),
                         ("Lipid",       C["lipid"])]
        )
        st.markdown(f'<div class="card">{macros_sw}</div>', unsafe_allow_html=True)

    # ── Row 2: Tujuan + Referensi ─────────────────────────────
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    r2a, r2b = st.columns([3, 2], gap="large")

    with r2a:
        st.markdown('<p class="sec">Tujuan</p>', unsafe_allow_html=True)
        goals = [
            "Mensimulasikan kebutuhan nutrisi makromolekul berdasarkan usia dan jenis kelamin",
            "Memvisualisasikan perubahan kebutuhan nutrisi sepanjang rentang usia",
            "Meningkatkan kesadaran tentang pentingnya nutrisi yang tepat sesuai tahap kehidupan",
            "Mendukung gaya hidup sehat melalui edukasi berbasis data ilmiah",
        ]
        items = "".join(f"<li>{g}</li>" for g in goals)
        st.markdown(f'<div class="card"><ol class="steps">{items}</ol></div>', unsafe_allow_html=True)

    with r2b:
        st.markdown('<p class="sec">Referensi Ilmiah</p>', unsafe_allow_html=True)
        refs = [
            ("Kemenkes RI, 2019", "Peraturan Menteri Kesehatan No. 28 Tahun 2019 tentang Angka Kecukupan Gizi (AKG) untuk Masyarakat Indonesia."),
            ("WHO, 2003", "Diet, Nutrition and the Prevention of Chronic Diseases. WHO Technical Report Series, No. 916. Geneva: WHO."),
            ("Institute of Medicine, 2005", "Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Fatty Acids, Protein, and Amino Acids. National Academies Press."),
            ("Gropper & Smith, 2013", "Advanced Nutrition and Human Metabolism (6th ed.). Wadsworth, Cengage Learning."),
        ]
        ref_html = "".join(
            f'<div style="padding:.6rem 0;border-bottom:1px solid #F0F0F0;">'
            f'<span style="font-size:.8rem;font-weight:700;color:{C["purple"]};">[{r[0]}]</span><br>'
            f'<span style="font-size:.82rem;color:#555;line-height:1.5;">{r[1]}</span></div>'
            for r in refs
        )
        st.markdown(f'<div class="card">{ref_html}</div>', unsafe_allow_html=True)

    # ── Row 3: Teknologi ──────────────────────────────────────
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec">Teknologi</p>', unsafe_allow_html=True)
    tech_cols = st.columns(4, gap="small")
    for col, (name, role) in zip(tech_cols, [
        ("Streamlit", "Web Framework"), ("Plotly", "Visualisasi Interaktif"),
        ("Pandas & NumPy", "Pengolahan Data"), ("Python 3.9+", "Bahasa Pemrograman")
    ]):
        with col:
            st.markdown(
                f'<div class="scard">'
                f'<div style="font-size:.95rem;font-weight:700;color:#333;">{name}</div>'
                f'<div class="scard-lbl">{role}</div></div>',
                unsafe_allow_html=True
            )

    # ── Row 4: Tim ────────────────────────────────────────────
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec">Tim Pengembang</p>', unsafe_allow_html=True)
    team = [
        ("Samuel Chris Michael\nBagasta Simanjuntak", "18223011", "Lipid & Backend"),
        ("Audy Alicia Renatha\nTirayoh", "18223097", "Integrasi & UI/Styling"),
        ("Carlen Asadel Axelle", "18223017", "Karbohidrat & Form Input"),
        ("Allodya Qonita Arrofa", "18223054", "Protein & Output Page"),
    ]
    tm_cols = st.columns(4, gap="medium")
    for col, (name, nim, role) in zip(tm_cols, team):
        with col:
            st.markdown(
                f'<div class="scard" style="text-align:left;">'
                f'<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,{C["purple"]},{C["protein"]});'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:.9rem;font-weight:800;color:#fff;margin-bottom:.75rem;">'
                f'{name[0]}</div>'
                f'<div style="font-size:.88rem;font-weight:700;color:#333;line-height:1.4;">{name.replace(chr(10), "<br>")}</div>'
                f'<div style="font-size:.78rem;color:{C["purple"]};font-weight:600;margin:.25rem 0;">{nim}</div>'
                f'<div style="font-size:.78rem;color:#888;">{role}</div>'
                f'</div>',
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="footer">'
    f'<img src="data:image/png;base64,{LOGO_NAME}" '
    f'style="height:24px;object-fit:contain;opacity:.45;display:block;margin:0 auto .75rem;"/>'
    f'<p style="margin:0 0 .2rem;">Simulasi Kebutuhan Nutrisi Makromolekul Berdasarkan Usia</p>'
    f'<p style="margin:0;font-size:.75rem;color:#CCC;">'
    f'© 2026 NutriAge Team &nbsp;·&nbsp; AKG Indonesia & WHO Guidelines</p></div>',
    unsafe_allow_html=True
)
