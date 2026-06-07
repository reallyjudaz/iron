import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- CSS CON ALLINEAMENTO A SINISTRA ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}

/* Forza l'allineamento a sinistra di tutto il contenuto */
.block-container { 
    padding-top: 0rem !important; 
    padding-bottom: 120px !important; 
    text-align: left !important; 
}

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: left !important; color: #ff9100 !important; font-size: 2.6rem !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: left !important; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }

/* Stile Expander allineato a sinistra */
.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; border-radius: 10px !important; color: white !important; text-align: left !important; }
.streamlit-expanderHeader { color: #ff9100 !important; font-weight: bold !important; font-size: 1.0rem !important; justify-content: flex-start !important; }

/* Bottoni */
div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; 
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI (Allineati a sinistra) ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=False, width=200) # Logo più piccolo e a sinistra

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        titolo_expander = f"{row['Data']} - {row['Nome Evento / Raduno']}"
        
        with st.expander(titolo_expander):
            st.write(f"📅 **Data:** {row['Data']}")
            st.write(f"📍 **Luogo:** {row['Luogo']}")
            st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

        conteggio = int(row.get('Partecipanti', 0))
        label = f"CI VADO 🔥 {conteggio}"
        if ha_gia_votato(i):
            st.button(label, key=f"btn_{i}", disabled=True)
        else:
            if st.button(label, key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = conteggio + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()

except Exception:
    st.error("Errore nel caricamento del file.")

# --- MENU FISSO ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #1f2124; border-top: 3px solid #ff9100; padding: 15px 0; display: flex; justify-content: center; z-index: 999999;'>
    <b style='color:#ff9100; font-family: Special Elite; font-size: 1.3rem; cursor: pointer;'>+ AGGIUNGI EVENTO</b>
</div>
""", unsafe_allow_html=True)
