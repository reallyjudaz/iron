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
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; }

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-bottom: 0px !important; text-shadow: 2px 2px 4px #000; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; cursor: pointer; }
.event-box h3 { font-family: 'Special Elite', cursive; color: #ff9100; margin: 0; }
.dettaglio-box { background-color: #1f2124; padding: 20px; border: 2px solid #ff9100; border-radius: 10px; color: white; }

/* Menu */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999; }
.menu-btn { font-family: 'Special Elite', cursive !important; color: #ff9100 !important; font-weight: bold; text-decoration: none; font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

# --- INIZIALIZZAZIONE STATO ---
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

# --- CARICAMENTO DATI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except:
    st.error("Errore: File eventi non trovato.")
    st.stop()

# --- LOGICA NAVIGAZIONE ---
if st.session_state.evento_selezionato is None:
    # --- VISTA LISTA ---
    st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ff9100;'>Seleziona un evento per i dettagli:</p>", unsafe_allow_html=True)
    
    for i, row in df.iterrows():
        nome = str(row['Nome Evento / Raduno'])
        if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
        
        # Cliccando su questo pulsante, apri il dettaglio
        if st.button(f"🏴‍☠️ {nome}", key=f"btn_open_{i}"):
            st.session_state.evento_selezionato = nome
            st.rerun()

else:
    # --- VISTA DETTAGLIO ---
    nome_evento = st.session_state.evento_selezionato
    evento = df[df['Nome Evento / Raduno'] == nome_evento].iloc[0]
    
    st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
    st.markdown(f"<h1>{nome_evento}</h1>", unsafe_allow_html=True)
    
    img_path = str(evento.get('Locandina', ''))
    if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
        
    st.write(f"📅 **Data:** {evento['Data']}")
    st.write(f"📍 **Luogo:** {evento['Luogo']}")
    
    # Pulsante partecipazione
    if st.button("PARTECIPERÒ! 🔥"):
        st.session_state.voti[nome_evento] += 1
        st.rerun()
    st.write(f"Partecipanti attuali: {st.session_state.voti[nome_evento]}")
    
    # Bottone Ritorno
    if st.button("⬅ INDIETRO"):
        st.session_state.evento_selezionato = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO ---
st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn' onclick='window.location.reload()'>HOME</a>
    <a href='#' class='menu-btn'>MC</a>
    <a href='#' class='menu-btn'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
