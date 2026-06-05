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
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; }

/* Logo & Titoli */
.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-bottom: 0px !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; margin-bottom: 20px !important; text-shadow: 2px 2px 4px #000; }

/* Box Eventi (STILE ORIGINALE) */
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.dettaglio-box { background-color: #1f2124; padding: 20px; border: 3px solid #ff9100; border-radius: 15px; color: white; margin-bottom: 20px; }

/* Bottone stile standard (senza pillole arancioni) */
div[data-testid="stButton"] button {
    background-color: #1f2124 !important;
    color: #ff9100 !important;
    border: 2px solid #ff9100 !important;
    border-radius: 10px !important;
    font-family: 'Special Elite', cursive !important;
    font-weight: bold !important;
    width: 100% !important;
    padding: 10px !important;
}

/* Menu */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# --- STATO ---
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None

# --- CARICAMENTO ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except: st.stop()

# --- LOGICA VISIVA ---
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

if st.session_state.evento_selezionato is None:
    # LISTA (Grafica originale)
    for i, row in df.iterrows():
        if st.button(f"🏴‍☠️ {row['Nome Evento / Raduno']}", key=f"btn_{i}"):
            st.session_state.evento_selezionato = i
            st.rerun()
else:
    # DETTAGLIO (Quadrato arancione)
    idx = st.session_state.evento_selezionato
    row = df.iloc[idx]
    st.markdown("<div class='dettaglio-box'>", unsafe_allow_html=True)
    st.write(f"## {row['Nome Evento / Raduno']}")
    if os.path.exists(str(row.get('Locandina', ''))): st.image(str(row['Locandina']), use_container_width=True)
    st.write(f"📅 **Data:** {row['Data']} | 📍 **Luogo:** {row['Luogo']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO (Ripristinato) ---
st.markdown("<div class='menu-fisso'>", unsafe_allow_html=True)
if st.button("HOME"): 
    st.session_state.evento_selezionato = None
    st.rerun()
st.button("MC")
st.button("ADMIN")
st.markdown("</div>", unsafe_allow_html=True)
