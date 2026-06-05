import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS DEFINITIVO (Box cliccabili) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; cursor: pointer; }
.dettaglio-box { background-color: #ff9100; padding: 20px; border-radius: 15px; color: black; font-weight: bold; }
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 9999; }
/* Nasconde il bordo del bottone per renderlo invisibile */
div[data-testid="stButton"] button { border: none !important; background: none !important; text-align: left !important; padding: 0 !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except: st.stop()

# Logo e Header fissi
if os.path.exists("logo_custom.png"): st.image("logo_custom.png", use_container_width=True)
st.markdown("<h1 style='text-align:center; color:#ff9100;'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- NAVIGAZIONE ---
if st.session_state.evento_selezionato is None:
    # LISTA: Ogni box è un bottone unico
    for i, row in df.iterrows():
        nome = str(row['Nome Evento / Raduno'])
        # Questo bottone è invisibile ma copre l'intero contenuto
        if st.button(f"box_{i}", key=f"click_{i}"):
            st.session_state.evento_selezionato = i
            st.rerun()
            
        # Disegniamo il box (non come bottone, ma come visualizzazione)
        st.markdown(f"""
        <div class='event-box'>
            <h3>{nome}</h3>
            <p>📅 {row['Data']} | 📍 {row['Luogo']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # DETTAGLIO (Rettangolo arancione)
    idx = st.session_state.evento_selezionato
    row = df.iloc[idx]
    
    st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
    st.write(f"## {row['Nome Evento / Raduno']}")
    if os.path.exists(str(row.get('Locandina', ''))): 
        st.image(str(row['Locandina']), use_container_width=True)
    st.write(f"📅 **Data:** {row['Data']}")
    st.write(f"📍 **Luogo:** {row['Luogo']}")
    
    # Qui il contatore originale
    if st.button("PARTECIPERÒ!"): st.session_state.voti[nome] = st.session_state.voti.get(nome, 0) + 1
    st.write(f"🔥 {st.session_state.voti.get(nome, 0)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO ---
st.markdown("<div class='menu-fisso'>", unsafe_allow_html=True)
if st.button("HOME"):
    st.session_state.evento_selezionato = None
    st.rerun()
st.button("MC")
st.button("ADMIN")
st.markdown("</div>", unsafe_allow_html=True)
