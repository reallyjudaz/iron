import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
/* Font Gotico per i titoli */
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');

.stApp { background-color: #161719; }

/* Nasconde elementi superflui */
#MainMenu, footer, header {visibility: hidden !important;}

.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; align-items: center !important; }

/* Logo */
.logo-wrapper { 
    display: flex !important; justify-content: center !important; width: 100vw !important; 
    margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; 
    margin-bottom: 0px !important; 
}
div[data-testid="stImage"] { width: 100% !important; display: flex !important; justify-content: center !important; }

/* Titolo Gotico */
.titolo-gotico { 
    font-family: 'UnifrakturMaguntia', cursive !important; 
    text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; 
    margin-top: -40px !important; margin-bottom: 0px !important;
    text-shadow: 2px 2px 4px #000;
}

/* Sottotitolo Gotico */
.sottotitolo {
    font-family: 'UnifrakturMaguntia', cursive !important;
    text-align: center; color: #ff9100 !important; font-size: 1.4rem !important;
    margin-top: -5px !important; margin-bottom: 20px !important;
}

/* Eventi */
.event-box { 
    background-color: #1f2124; padding: 8px; margin-bottom: 12px; 
    border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; 
    font-family: sans-serif !important; 
}
.event-box h3 { 
    font-family: sans-serif !important; font-size: 0.9rem !important; 
    margin-bottom: 3px !important; text-transform: uppercase; color: #ff9100;
}
.event-box p { 
    font-family: sans-serif !important; font-size: 0.75rem !important; 
    margin-bottom: 3px !important; opacity: 0.9; 
}

/* Menu Fisso Integrato - Gotico, arancione, distanziato */
.menu-fisso { 
    position: fixed; bottom: 0; left: 0; width: 100%; 
    background: #1f2124; display: flex; justify-content: flex-start; 
    gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999; 
}
.menu-btn { 
    font-family: 'UnifrakturMaguntia', cursive !important; 
    color: #ff9100 !important; 
    font-weight: bold; 
    text-decoration: none; 
    font-size: 1.4rem !important; 
}
</style>
""", unsafe_allow_html=True)

# Logo
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)

# Titolo e Sottotitolo
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# Lista Eventi
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

# Menu Fisso Integrato (Gotico e distanziato)
st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn'>HOME</a>
    <a href='#' class='menu-btn'>MC</a>
    <a href='#' class='menu-btn'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
