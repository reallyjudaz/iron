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

# --- CSS INTEGRATO ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important; }
.block-container { padding-top: 0rem !important; padding-bottom: 7rem !important; }

/* Testi Bianchi nel Form */
label, .stFileUploader label { color: white !important; font-family: 'Special Elite', cursive !important; }

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -20px !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }

.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; border-radius: 10px !important; color: white !important; }
.streamlit-expanderHeader { color: #ff9100 !important; font-weight: bold !important; font-size: 1.0rem !important; }

div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important;
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; 
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- AGGIUNGI EVENTO ---
with st.expander("➕ AGGIUNGI NUOVO EVENTO"):
    with st.form("form_aggiungi", clear_on_submit=True):
        nuovo_nome = st.text_input("Nome Evento")
        nuova_data = st.text_input("Data (es. 12/06/2026)")
        nuovo_luogo = st.text_input("Luogo")
        file_locandina = st.file_uploader("Carica Locandina", type=['png', 'jpg', 'jpeg'])
        submit = st.form_submit_button("SALVA EVENTO")
        
        if submit:
            if not os.path.exists("locandine"): os.makedirs("locandine")
            path_salvataggio = ""
            if file_locandina is not None:
                path_salvataggio = os.path.join("locandine", file_locandina.name)
                with open(path_salvataggio, "wb") as f:
                    f.write(file_locandina.getbuffer())
            
            if os.path.exists("Lista_Eventi_Bikers_Judaz.xlsx"):
                df_base = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
                nuovo_rigo = pd.DataFrame([{
                    "Nome Evento / Raduno": nuovo_nome, 
                    "Data": nuova_data, 
                    "Luogo": nuovo_luogo, 
                    "Locandina": path_salvataggio,
                    "Partecipanti": 0
                }])
                df_nuovo = pd.concat([df_base, nuovo_rigo], ignore_index=True)
                df_nuovo.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                st.success("Evento aggiunto!")
                st.rerun()

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
            st.write(f"📍 **Luogo:** {row['Luogo']}")
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

except Exception as e:
    st.error(f"Errore caricamento file: {e}")

# --- MENU FISSO ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999;'>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>HOME</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>MC</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
