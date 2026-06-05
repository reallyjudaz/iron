import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS E STILI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; align-items: center !important; }

.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; text-shadow: 2px 2px 4px #000; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-top: -5px !important; margin-bottom: 20px !important; }

.event-box { background-color: #1f2124; padding: 10px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.dettaglio-quadrato { background-color: #1f2124; padding: 20px; border: 3px solid #ff9100; border-radius: 15px; color: white; margin-bottom: 20px; }

div[data-testid="stButton"] button {
    background-color: #ff9100 !important; color: black !important; border: none !important;
    font-weight: bold !important; font-family: 'Special Elite', cursive !important;
    border-radius: 5px !important; height: 38px !important; width: 100%;
}

.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999; }
.menu-btn { font-family: 'Special Elite', cursive !important; color: #ff9100 !important; font-weight: bold; text-decoration: none; font-size: 1.2rem !important; cursor: pointer; background: none; border: none; }
</style>
""", unsafe_allow_html=True)

# --- STATO DELLA NAVIGAZIONE ---
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

# --- CARICAMENTO DATI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except:
    st.error("File eventi non trovato.")
    st.stop()

# --- HEADER FISSO ---
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LOGICA PAGINE ---
if st.session_state.evento_selezionato is None:
    # --- VISTA LISTA ---
    st.markdown("<p class='sottotitolo'>«Seleziona l'evento per i dettagli»</p>", unsafe_allow_html=True)
    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        if st.button(f"🏴‍☠️ {nome}", key=f"list_{i}"):
            st.session_state.evento_selezionato = i
            st.rerun()
else:
    # --- VISTA DETTAGLIO ---
    idx = st.session_state.evento_selezionato
    row = df.iloc[idx]
    
    st.markdown(f"<div class='dettaglio-quadrato'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#ff9100; font-family: sans-serif;'>{row['Nome Evento / Raduno']}</h2>", unsafe_allow_html=True)
    
    img_path = str(row.get('Locandina', ''))
    if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
        
    st.write(f"📅 **Data:** {row['Data']}")
    st.write(f"📍 **Luogo:** {row['Luogo']}")
    
    if st.button("⬅ TORNA ALLA LISTA"):
        st.session_state.evento_selezionato = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO ---
# Usiamo st.button per il tasto HOME così da poter gestire il reset dello stato
col_home, col_mc, col_admin = st.columns([1, 1, 1])
st.markdown("""
<div class='menu-fisso'>
""", unsafe_allow_html=True)

if st.button("HOME", key="nav_home"):
    st.session_state.evento_selezionato = None
    st.rerun()
st.markdown("<span>MC</span> <span>ADMIN</span> </div>", unsafe_allow_html=True)
