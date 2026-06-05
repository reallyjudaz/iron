import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS DEFINITIVO PER ALLINEAMENTO PULSANTI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 80px !important; }

/* Stili Box */
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-bottom: 0px !important; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
.contatore-targhetta { display: flex; align-items: center; justify-content: center; background-color: #1f2124; color: #ff9100; padding: 5px; border-radius: 5px; font-family: 'Special Elite', cursive; font-weight: bold; border: 2px solid #ff9100; height: 38px; }

/* Forza i bottoni a non sparpagliarsi */
div[data-testid="stButton"] { margin: 0px !important; }
div[data-testid="stButton"] button {
    background-color: #ff9100 !important; color: black !important; border: none !important;
    font-weight: bold !important; font-family: 'Special Elite', cursive !important;
    border-radius: 5px !important; height: 38px !important; width: 100%;
}
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 10px; border-top: 3px solid #ff9100; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except: st.stop()

# Logo
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- NAVIGAZIONE ---
if st.session_state.evento_selezionato is None:
    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        if st.button(f"🏴‍☠️ {nome}", key=f"list_{i}"):
            st.session_state.evento_selezionato = i
            st.rerun()
else:
    idx = st.session_state.evento_selezionato
    row = df.iloc[idx]
    
    st.markdown(f"<div class='event-box'>", unsafe_allow_html=True)
    st.markdown(f"<h2>{row['Nome Evento / Raduno']}</h2>", unsafe_allow_html=True)
    if os.path.exists(str(row.get('Locandina', ''))):
        st.image(str(row['Locandina']), use_container_width=True)
    st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
    
    # RIGA COMPATTA: Pulsante Partecipa + Contatore
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        if st.button("PARTECIPERÒ!"): st.session_state.voti[row['Nome Evento / Raduno']] = st.session_state.voti.get(row['Nome Evento / Raduno'], 0) + 1
    with col2:
        st.markdown(f"<div class='contatore-targhetta'>🔥 {st.session_state.voti.get(row['Nome Evento / Raduno'], 0)}</div>", unsafe_allow_html=True)
    
    # Pulsante Indietro separato
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅ TORNA ALLA LISTA"):
        st.session_state.evento_selezionato = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO IN BASSO ---
st.markdown("<div class='menu-fisso'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("HOME"):
        st.session_state.evento_selezionato = None
        st.rerun()
with c2: st.button("MC")
with c3: st.button("ADMIN")
st.markdown("</div>", unsafe_allow_html=True)
