import streamlit as st
import pandas as pd
import os

# 1. Cambiato da 'centered' a 'wide'
st.set_page_config(page_title="Iron & Rubber", layout="wide")

# --- CSS (Ora forza l'allineamento a sinistra nel layout wide) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}

/* Forza il contenuto principale a sinistra e limita la larghezza */
.block-container { 
    max-width: 800px !important; 
    padding-left: 2rem !important;
    text-align: left !important;
    padding-bottom: 120px !important;
}

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive; color: #ff9100; font-size: 2.6rem; text-align: left; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive; color: #ff9100; font-size: 1.4rem; margin-bottom: 20px; text-align: left; }

div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; 
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=250)

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
        if st.button(f"CI VADO 🔥 {conteggio}", key=f"btn_{i}"):
            df.at[i, 'Partecipanti'] = conteggio + 1
            df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
            st.rerun()

except Exception:
    st.error("Errore caricamento file.")

# --- MENU FISSO (Allineato a sinistra) ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #1f2124; border-top: 3px solid #ff9100; padding: 15px 2rem; z-index: 999999;'>
    <b style='color:#ff9100; font-family: Special Elite; font-size: 1.3rem; cursor: pointer;'>+ AGGIUNGI EVENTO</b>
</div>
""", unsafe_allow_html=True)
