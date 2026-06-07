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

# --- CSS ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-bottom: 6rem !important; }

/* Stile per l'expander */
.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; color: white !important; }
.streamlit-expanderHeader { color: #ff9100 !important; font-weight: bold !important; }

div[data-testid="stButton"] button {
    background-color: #ff9100 !important; color: black !important; 
    font-weight: bold !important; font-family: 'Special Elite', cursive !important; 
    border-radius: 5px !important; width: 100%;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png")

st.markdown("<h1 style='text-align:center; color:#ff9100;'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LISTA EVENTI CON TENDINA ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    for i, row in df.iterrows():
        # L'expander crea la "tendina" 
        with st.expander(f"📅 {row['Nome Evento / Raduno']}"):
            st.write(f"📍 {row['Luogo']}")
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
        
        # Il bottone sta FUORI dall'expander, così è sempre cliccabile [cite: 12, 13]
        label = f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}"
        if ha_gia_votato(i):
            st.button(label, key=f"btn_{i}", disabled=True)
        else:
            if st.button(label, key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()

except Exception as e:
    st.error(f"Errore: {e}")
