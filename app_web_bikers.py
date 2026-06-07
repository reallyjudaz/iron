import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI DI MEMORIA ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- CSS ESSENZIALE ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.event-box { background-color: #1f2124; padding: 20px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px; }
.dettaglio-box { background-color: #1f2124; padding: 25px; border: 3px solid #ff9100; border-radius: 15px; color: white; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; width: 100%; border: none !important; }
</style>
""", unsafe_allow_html=True)

# --- STATO E CARICAMENTO ---
if 'evento_aperto' not in st.session_state: st.session_state.evento_aperto = None

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except:
    df = pd.DataFrame()

# --- INTERFACCIA ---
if df.empty:
    st.error("Carica il file Excel!")
else:
    if st.session_state.evento_aperto is None:
        # LISTA: CLICCA SUL TASTO PER APRIRE
        for i, row in df.iterrows():
            st.markdown(f"<div class='event-box'><h3>{row['Nome Evento / Raduno']}</h3><p>{row['Data']}</p></div>", unsafe_allow_html=True)
            
            # Unico tasto per aprire
            if st.button("VEDI DETTAGLI", key=f"apri_{i}"):
                st.session_state.evento_aperto = i
                st.rerun()
            
            # Voto
            label = f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}"
            if ha_gia_votato(i): st.button(label, key=f"btn_{i}", disabled=True)
            elif st.button(label, key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()
    else:
        # DETTAGLIO
        idx = st.session_state.evento_aperto
        row = df.iloc[idx]
        
        st.markdown("<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.subheader(row['Nome Evento / Raduno'])
        st.write(f"📅 **Data:** {row['Data']}")
        st.write(f"📍 **Luogo:** {row['Luogo']}")
        st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
        
        # Locandina
        img = str(row.get('Locandina', ''))
        if img and os.path.exists(img): st.image(img, use_container_width=True)
            
        if st.button("BACK"):
            st.session_state.evento_aperto = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
