import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS SICURO (Solo font e colori, niente forzature su elementi nativi) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; color: #ff9100 !important; text-align: center; font-size: 2.6rem; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; color: #ff9100 !important; text-align: center; font-size: 1.4rem; margin-bottom: 20px; }

/* Stile per i contenuti dentro l'expander */
.info-evento { color: white; font-family: 'Special Elite', cursive !important; }

div[data-testid="stButton"] button {
    background-color: #ff9100 !important; color: black !important; 
    font-weight: bold !important; font-family: 'Special Elite', cursive !important; 
    border-radius: 5px !important; width: 100%;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=200)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- FUNZIONI ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        # Qui usiamo l'expander standard. Non gli diamo CSS forzato, quindi non darà errore rosa.
        with st.expander(f"{row['Nome Evento / Raduno']}"):
            st.markdown(f"<div class='info-evento'>📍 Luogo: {row['Luogo']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-evento'>📝 Note: {row.get('Dettagli / Note', 'Nessuna nota.')}</div>", unsafe_allow_html=True)
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            
            conteggio = int(row.get('Partecipanti', 0))
            if ha_gia_votato(i):
                st.button(f"GIÀ PARTECIPATO 🔥 {conteggio}", key=f"btn_{i}", disabled=True)
            else:
                if st.button(f"CI VADO 🔥 {conteggio}", key=f"btn_{i}"):
                    df.at[i, 'Partecipanti'] = conteggio + 1
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    registra_voto(i)
                    st.rerun()

except Exception as e:
    st.error(f"Errore: {e}")
