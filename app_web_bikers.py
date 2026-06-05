import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS DEFINITIVO ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important; }
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; align-items: center !important; }

/* Logo & Titoli */
.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-bottom: 0px !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; margin-bottom: 0px !important; text-shadow: 2px 2px 4px #000; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-top: -5px !important; margin-bottom: 20px !important; }

/* Box Eventi */
.event-box { background-color: #1f2124; padding: 10px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.dettaglio-box { background-color: #ff9100; padding: 20px; border-radius: 15px; color: black; font-weight: bold; margin-bottom: 20px; text-align: center; }

/* Contatore */
.contatore-targhetta { background-color: #1f2124; color: #ff9100; padding: 5px 0; border-radius: 5px; font-family: 'Special Elite', cursive; font-weight: bold; border: 2px solid #ff9100; text-align: center; height: 38px; display: flex; align-items: center; justify-content: center; }

/* Bottoni */
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; border: none !important; font-weight: bold !important; font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; }

/* Menu */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# Stati
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

# Logo e Titolo
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# Caricamento Dati
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    # --- LOGICA: LISTA VS DETTAGLIO ---
    if st.session_state.evento_selezionato is None:
        st.markdown("<p class='sottotitolo'>«Seleziona l'evento per i dettagli»</p>", unsafe_allow_html=True)
        
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
            
            st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
            
            # --- RIGA CON 3 ELEMENTI ---
            c1, c2, c3 = st.columns([1, 1, 0.5])
            with c1:
                if st.button("DETTAGLI", key=f"dett_{i}"):
                    st.session_state.evento_selezionato = i
                    st.rerun()
            with c2:
                if st.button("PARTECIPA", key=f"part_{i}"):
                    st.session_state.voti[nome] += 1
                    st.rerun()
            with c3:
                st.markdown(f"<div class='contatore-targhetta'>🔥 {st.session_state.voti[nome]}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # --- VISTA DETTAGLIO ---
        idx = st.session_state.evento_selezionato
        row = df.iloc[idx]
        st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.write(f"<h2>{row['Nome Evento / Raduno']}</h2>", unsafe_allow_html=True)
        
        if os.path.exists(str(row.get('Locandina', ''))):
            st.image(str(row['Locandina']), use_container_width=True)
            
        st.write(f"📅 Data: {row['Data']} | 📍 Luogo: {row['Luogo']}")
        
        if st.button("⬅ TORNA ALLA LISTA"):
            st.session_state.evento_selezionato = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception:
    pass

# --- MENU FISSO ---
st.markdown("<div class='menu-fisso'>", unsafe_allow_html=True)
if st.button("HOME", key="nav_home"):
    st.session_state.evento_selezionato = None
    st.rerun()
st.button("MC", key="nav_mc")
st.button("ADMIN", key="nav_admin")
st.markdown("</div>", unsafe_allow_html=True)
