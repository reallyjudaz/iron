import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS ORIGINALE (Quello che garantisce l'aspetto che volevi) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 1rem !important; padding-bottom: 6rem !important; }

/* Titoli */
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.2rem !important; margin-top: 0px !important; text-shadow: 2px 2px 4px #000; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.2rem !important; margin-bottom: 20px !important; }

/* Box Evento (Home) */
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
.contatore-targhetta { display: inline-block; background-color: #1f2124; color: #ff9100; padding: 5px 15px; border-radius: 5px; font-family: 'Special Elite', cursive; border: 2px solid #ff9100; }

/* Dettaglio (Rettangolo arancione) */
.dettaglio-box { background-color: #ff9100; padding: 20px; border-radius: 15px; color: black; font-weight: bold; }

/* Menu */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 9999; }
div[data-testid="stButton"] button { font-family: 'Special Elite', cursive !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# --- STATO ---
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

# --- HEADER FISSO ---
if os.path.exists("logo_custom.png"): st.image("logo_custom.png", use_container_width=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- CARICAMENTO DATI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except: st.stop()

# --- AREA VARIABILE ---
if st.session_state.evento_selezionato is None:
    # LISTA (Home)
    for i, row in df.iterrows():
        nome = str(row['Nome Evento / Raduno'])
        st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
        if st.button("DETTAGLI", key=f"btn_{i}"):
            st.session_state.evento_selezionato = i
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # DETTAGLIO (Rettangolo arancione)
    idx = st.session_state.evento_selezionato
    row = df.iloc[idx]
    st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
    st.write(f"## {row['Nome Evento / Raduno']}")
    if os.path.exists(str(row.get('Locandina', ''))): st.image(str(row['Locandina']), use_container_width=True)
    st.write(f"📅 **Data:** {row['Data']}")
    st.write(f"📍 **Luogo:** {row['Luogo']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO ---
st.markdown("<div class='menu-fisso'>", unsafe_allow_html=True)
if st.button("HOME"):
    st.session_state.evento_selezionato = None
    st.rerun()
st.button("MC")
st.button("ADMIN")
st.markdown("</div>", unsafe_allow_html=True)
