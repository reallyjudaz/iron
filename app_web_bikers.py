import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS SEMPLIFICATO ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 100px !important; }

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; color: #ff9100 !important; font-size: 2.6rem !important; }
.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; border-radius: 10px !important; color: white !important; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- CONTENUTO ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=200)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    for i, row in df.iterrows():
        with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
            st.write(f"📍 {row['Luogo']}")
            if os.path.exists(str(row.get('Locandina', ''))):
                st.image(str(row['Locandina']), use_container_width=True)
        
        if st.button(f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}", key=f"btn_{i}"):
            df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
            df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
            st.rerun()
except:
    st.error("Errore nel file Excel.")

# --- MENU IN BASSO (Metodo stabile senza errori) ---
st.markdown("---")
with st.container():
    # Usiamo un expander invece del popover per evitare l'errore in rosa
    with st.expander("➕ AGGIUNGI NUOVO EVENTO"):
        with st.form("form_nuovo", clear_on_submit=True):
            n = st.text_input("Nome Evento")
            d = st.date_input("Data")
            l = st.text_input("Luogo")
            if st.form_submit_button("SALVA EVENTO"):
                st.success(f"Evento {n} aggiunto!")
