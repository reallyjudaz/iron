import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS ORIGINALE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
.stApp { background-color: #161719; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.contatore-targhetta { display: inline-block; background-color: #1f2124; color: #ff9100; padding: 5px 12px; border-radius: 5px; font-family: 'Special Elite'; font-weight: bold; border: 2px solid #ff9100; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; border: none !important; font-weight: bold !important; font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; }
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999; display: flex; justify-content: space-around; }
</style>
""", unsafe_allow_html=True)

# --- STATO NAVIGAZIONE ---
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

# --- CARICAMENTO DATI ---
df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
df.columns = df.columns.str.strip()

# --- HEADER FISSO ---
if os.path.exists("logo_custom.png"): st.image("logo_custom.png", use_container_width=True)
st.markdown("<h1 style='text-align:center; color:#ff9100; font-family:UnifrakturMaguntia;'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- AREA CONTENUTO (LISTA O DETTAGLIO) ---
if st.session_state.evento_selezionato is None:
    # --- VISUALIZZAZIONE LISTA ORIGINALE ---
    for i, row in df.iterrows():
        nome = str(row['Nome Evento / Raduno'])
        if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
        
        # BOX EVENTO
        st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            if st.button("PARTECIPERÒ!", key=f"btn_{i}"):
                st.session_state.voti[nome] += 1
        with col2:
            st.markdown(f"<div class='contatore-targhetta'>🔥 {st.session_state.voti[nome]}</div>", unsafe_allow_html=True)
        
        # BOTTONE DETTAGLIO NASCOSTO/INTEGRATO
        if st.button("Vedi Dettagli", key=f"info_{i}"):
            st.session_state.evento_selezionato = i
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- VISUALIZZAZIONE DETTAGLIO (Il rettangolo arancione) ---
    idx = st.session_state.evento_selezionato
    row = df.iloc[idx]
    st.markdown("<div class='event-box' style='border-color:#ff9100;'>", unsafe_allow_html=True)
    st.write(f"## {row['Nome Evento NOME'] if 'Nome Evento NOME' in row else row['Nome Evento / Raduno']}")
    if os.path.exists(str(row.get('Locandina', ''))): st.image(str(row['Locandina']), use_container_width=True)
    st.write(f"**Data:** {row['Data']} | **Luogo:** {row['Luogo']}")
    if st.button("⬅ TORNA ALLA LISTA"):
        st.session_state.evento_selezionato = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO ---
st.markdown("<div class='menu-fisso'>HOME | MC | ADMIN</div>", unsafe_allow_html=True)
