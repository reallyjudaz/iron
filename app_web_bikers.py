import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; display: none !important; }

.block-container { padding-top: 0.5rem !important; padding-bottom: 5rem !important; align-items: center !important; }

/* Logo Full Width */
.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; margin-bottom: 10px; }
div[data-testid="stImage"] { width: 100% !important; display: flex !important; justify-content: center !important; }

/* Scritta Principale - Ingrandita */
.titolo-gotico { 
    font-family: 'UnifrakturMaguntia', cursive !important; 
    text-align: center; 
    color: #ff9100 !important; 
    font-size: 3.2rem !important; /* Ingrandita */
    margin: 0 !important;
    text-shadow: 3px 3px 6px #000;
}

/* Sottotitolo Filosofico - Molto piccolo */
.sottotitolo {
    font-family: 'Arial', sans-serif !important;
    text-align: center;
    color: #aaaaaa !important;
    font-size: 0.9rem !important;
    font-style: italic;
    margin-bottom: 25px !important;
    letter-spacing: 1px;
}

.event-box { background-color: #1f2124; padding: 12px; margin-bottom: 15px; border: 3px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.event-box h3 { font-size: 1.2rem !important; margin-bottom: 5px !important; }
.event-box p { font-size: 0.9rem !important; }

.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 10px; border-top: 3px solid #ff9100; z-index: 9999; }
.menu-btn { color: #ff9100; font-weight: bold; text-decoration: none; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# Logo
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)

# Titolo e Sottotitolo
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>Non è la meta, è la strada a rivelare chi sei.</p>", unsafe_allow_html=True)

# Lista Eventi (Logica invariata)
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    if 'voti' not in st.session_state: st.session_state.voti = {}

    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
        
        st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        
        if st.button(f"Parteciperò! ({st.session_state.voti[nome]})", key=f"btn_{i}"):
            st.session_state.voti[nome] += 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
except Exception:
    pass

# Menu Fisso
st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn'>🏠 HOME</a>
    <a href='#' class='menu-btn'>🏴‍☠️ MC</a>
    <a href='#' class='menu-btn'>🔑 ADMIN</a>
</div>
""", unsafe_allow_html=True)
