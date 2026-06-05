import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
/* CSS per forzare la riga */
.button-row { display: flex !important; align-items: center !important; gap: 10px !important; margin-top: 10px !important; }
.button-row > div { flex: 1 !important; } /* Ogni elemento prende spazio uguale */

/* Contatore stile targhetta */
.contatore-targhetta { background-color: #1f2124; color: #ff9100; border: 2px solid #ff9100; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; height: 38px; display: flex; align-items: center; justify-content: center; }

/* Bottoni compatti */
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; border: none !important; width: 100% !important; height: 38px !important; }

/* Il resto del tuo stile */
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
</style>
""", unsafe_allow_html=True)

# Logica di stato
if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    if st.session_state.evento_selezionato is None:
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            
            st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
            
            # --- RIGA FORZATA CON FLEXBOX ---
            st.markdown("<div class='button-row'>", unsafe_allow_html=True)
            
            # Colonna 1: INFO
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("INFO", key=f"inf_{i}"):
                    st.session_state.evento_selezionato = i
                    st.rerun()
            # Colonna 2: PARTECIPA
            with c2:
                if st.button("PARTECIPA", key=f"par_{i}"):
                    st.session_state.voti[nome] = st.session_state.voti.get(nome, 0) + 1
                    st.rerun()
            # Colonna 3: CONTATORE
            with c3:
                st.markdown(f"<div class='contatore-targhetta'>🔥 {st.session_state.voti.get(nome, 0)}</div>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True) # Chiude button-row e event-box
            
    else:
        # Dettaglio
        idx = st.session_state.evento_selezionato
        row = df.iloc[idx]
        st.write(f"## {row['Nome Evento / Raduno']}")
        if st.button("⬅ TORNA"):
            st.session_state.evento_selezionato = None
            st.rerun()
except:
    st.error("File non trovato o errore di lettura.")
