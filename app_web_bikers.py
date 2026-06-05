import streamlit as st
import pandas as pd
import os

# Configurazione mobile-first
st.set_page_config(page_title="Iron & Rubber", layout="centered")

# CSS "Zero-Margin" e Font Gotico
st.markdown("""
<style>
/* Importa font stile gotico da Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');

.stApp { background-color: #161719; }

/* Elimina spazio in alto e icone */
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; display: none !important; }
.block-container { padding-top: 0rem !important; align-items: center !important; }

/* Logo in cima */
.logo-wrapper { margin-top: -20px !important; display: flex; justify-content: center; }

/* Titolo Gotico Rock */
.titolo-gotico { 
    font-family: 'UnifrakturMaguntia', cursive !important; 
    text-align: center; 
    color: #ff9100 !important; 
    font-size: 3.5rem !important; 
    margin-top: -10px !important;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px #000;
}

.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 20px; border: 3px solid #ff9100; border-radius: 12px; color: white; text-align: center; }

/* Menu Fisso in basso */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 9999; }
.menu-btn { color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# 1. Logo (senza margine)
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png", width=220)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Titolo Gotico
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# 3. Lista Eventi
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
        else:
            st.write("*(Nessuna locandina)*")
            
        if st.button(f"Parteciperò! ({st.session_state.voti[nome]})", key=f"btn_{i}"):
            st.session_state.voti[nome] += 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.write("Caricamento...")

# 4. Menu Fisso
st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn'>🏠 HOME</a>
    <a href='#' class='menu-btn'>🏴‍☠️ MC</a>
    <a href='#' class='menu-btn'>🔑 ADMIN</a>
</div>
""", unsafe_allow_html=True)
