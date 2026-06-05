import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
/* CSS per forzare la riga compatta */
.riga-eventi { 
    display: flex !important; 
    flex-direction: row !important; 
    align-items: center !important; 
    gap: 5px !important; 
    width: 100% !important; 
}
/* Forza i bottoni a stare in riga */
.riga-eventi > div { flex: 1 !important; min-width: 0 !important; }

/* Stili specifici */
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
.contatore-box { background-color: #1f2124; color: #ff9100; border: 2px solid #ff9100; border-radius: 5px; padding: 7px; text-align: center; font-weight: bold; font-family: 'Special Elite'; font-size: 0.9rem; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; border: none !important; width: 100% !important; height: 35px !important; font-size: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)

if 'evento_selezionato' not in st.session_state: st.session_state.evento_selezionato = None
if 'voti' not in st.session_state: st.session_state.voti = {}

# --- HEADER (Mantieni il tuo originale) ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=True)
st.markdown("<h1 style='text-align:center; color:#ff9100; font-family:UnifrakturMaguntia;'>Iron & Rubber</h1>", unsafe_allow_html=True)

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    if st.session_state.evento_selezionato is None:
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
            
            st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
            
            # --- BLOCCO COMPATTO SENZA COLONNE STREAMLIT ---
            st.markdown("<div class='riga-eventi'>", unsafe_allow_html=True)
            
            # Usiamo dei form per gestire il click senza rompere il layout
            if st.button("INFO", key=f"info_{i}"):
                st.session_state.evento_selezionato = i
                st.rerun()
            if st.button("PARTECIPA", key=f"part_{i}"):
                st.session_state.voti[nome] += 1
                st.rerun()
            st.markdown(f"<div class='contatore-box'>🔥 {st.session_state.voti[nome]}</div>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    else:
        # DETTAGLIO
        idx = st.session_state.evento_selezionato
        row = df.iloc[idx]
        st.markdown(f"<div class='event-box'><h2>{row['Nome Evento / Raduno']}</h2>", unsafe_allow_html=True)
        st.write(f"📅 Data: {row['Data']} | 📍 Luogo: {row['Luogo']}")
        if st.button("⬅ TORNA"):
            st.session_state.evento_selezionato = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception:
    st.write("Carica il file Excel per iniziare.")

# Menu Fisso
st.markdown("<div class='menu-fisso' style='position:fixed; bottom:0; left:0; width:100%; background:#1f2124; display:flex; justify-content:space-around; padding:15px; border-top:3px solid #ff9100;'>HOME | MC | ADMIN</div>", unsafe_allow_html=True)
