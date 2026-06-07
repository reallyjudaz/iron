import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS ORIGINALE E STABILE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}

/* Testo bianco per tutto */
.stApp, p, div, span, label { color: #ffffff !important; }

.block-container { 
    padding-top: 0rem !important; 
    margin-left: 0 !important;
    margin-right: auto !important;
    max-width: 800px !important;
}

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: left !important; color: #ff9100 !important; font-size: 2.6rem !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: left !important; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }

.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; border-radius: 10px !important; }
.streamlit-expanderHeader { color: #ffffff !important; font-weight: bold !important; justify-content: flex-start !important; }

div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; width: 100%; 
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=200)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- AGGIUNGI EVENTO (Primo Riquadro) ---
with st.expander("➕ AGGIUNGI NUOVO EVENTO"):
    with st.form("form_nuovo", clear_on_submit=True):
        n = st.text_input("Nome Evento")
        d = st.date_input("Data")
        l = st.text_input("Luogo")
        if st.form_submit_button("SALVA EVENTO"):
            st.success(f"Evento {n} aggiunto!")

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
            st.write(f"📍 **Luogo:** {row['Luogo']}")
            st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
            if os.path.exists(str(row.get('Locandina', ''))):
                st.image(str(row['Locandina']), use_container_width=True)

        conteggio = int(row.get('Partecipanti', 0))
        if st.button(f"CI VADO 🔥 {conteggio}", key=f"btn_{i}"):
            df.at[i, 'Partecipanti'] = conteggio + 1
            df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
            st.rerun()

except Exception:
    st.error("Errore nel file Excel.")
