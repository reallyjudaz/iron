import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; align-items: center !important; }
.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; margin-bottom: 0px !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; margin-bottom: 0px !important; text-shadow: 2px 2px 4px #000; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-top: -5px !important; margin-bottom: 20px !important; }
.event-box { background-color: #1f2124; padding: 10px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; border: none !important; font-weight: bold !important; font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; }
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999; }
.menu-btn { font-family: 'Special Elite', cursive !important; color: #ff9100 !important; font-weight: bold; text-decoration: none; font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

if 'voti' not in st.session_state: st.session_state.voti = {}
# 'ha_votato' terrà traccia di quali eventi l'utente ha già confermato
if 'ha_votato' not in st.session_state: st.session_state.ha_votato = []

if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
        
        st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
        
        # Logica bottone univoco
        label = f"CI VADO 🔥 {st.session_state.voti[nome]}"
        
        # Se l'utente ha già votato questo evento (key univoca), disabilitiamo il bottone
        if i in st.session_state.ha_votato:
            st.button(label, key=f"btn_{i}", disabled=True)
        else:
            if st.button(label, key=f"btn_{i}"):
                st.session_state.voti[nome] += 1
                st.session_state.ha_votato.append(i) # Segna come votato
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
except Exception:
    pass

st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn'>HOME</a>
    <a href='#' class='menu-btn'>MC</a>
    <a href='#' class='menu-btn'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
