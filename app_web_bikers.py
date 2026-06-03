import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# CSS Migliorato
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }

/* Stile Rock per titolo */
.titolo-rock { font-family: 'Impact', sans-serif !important; text-align: center; color: #ff9100 !important; font-size: 2.2rem !important; margin: 10px 0; }

/* Menu Fisso in basso */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 999; }
.menu-btn { color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# 1. Logo (Centrato con colonne)
c1, c2, c3 = st.columns([1, 2, 1])
if os.path.exists("logo_custom.png"):
    with c2: st.image("logo_custom.png", use_container_width=True)

# 2. Titolo
st.markdown("<h1 class='titolo-rock'>IRON & RUBBER</h1>", unsafe_allow_html=True)

# 3. Lista Eventi
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    
    # Inizializza sessione per contatori
    if 'voti' not in st.session_state: st.session_state.voti = {}

    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
        
        st.subheader(nome)
        st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
        
        if os.path.exists(str(row.get('Locandina', ''))):
            st.image(str(row['Locandina']), use_container_width=True)
            
        if st.button(f"Parteciperò! ({st.session_state.voti[nome]})", key=f"btn_{i}"):
            st.session_state.voti[nome] += 1
            st.rerun()
        st.divider()

except Exception as e:
    st.error(f"Errore: {e}")

# 4. Menu Fisso
st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn'>🏠 HOME</a>
    <a href='#' class='menu-btn'>🏴‍☠️ MC</a>
    <a href='#' class='menu-btn'>🔑 ADMIN</a>
</div>
""", unsafe_allow_html=True)
