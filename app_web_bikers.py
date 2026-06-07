import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI PER MEMORIA PERMANENTE ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        voti = f.read().splitlines()
        return str(id_evento) in voti

# --- CSS E STILE ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important; }
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
.event-box h3 { color: #ff9100; font-family: sans-serif; font-size: 1.1rem; margin-bottom: 5px; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; border-radius: 5px !important; height: 38px !important; width: 100%; }
/* Stile expander */
.streamlit-expanderHeader { background-color: #2a2d32 !important; border: 1px solid #ff9100 !important; border-radius: 5px !important; color: #ff9100 !important; }
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=True)

st.markdown("<h1 style='text-align:center; color:#ff9100;'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LISTA EVENTI CON EXPANDER ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        
        # Usiamo l'expander per aprire/chiudere il dettaglio dentro il quadrato
        with st.expander(f"📌 {nome}"):
            st.write(f"📅 **Data:** {row['Data']}")
            st.write(f"📍 **Luogo:** {row['Luogo']}")
            st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

        # Logica Voto (fuori dall'expander)
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

except Exception as e:
    st.error("Carica il file Excel per iniziare.")

# --- MENU ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999;'>
    <b style='color:#ff9100;'>HOME</b><b style='color:#ff9100;'>MC</b><b style='color:#ff9100;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
