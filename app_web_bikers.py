import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI DATI ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- CARICAMENTO SICURO ---
# Creiamo il file solo se manca, altrimenti leggiamo quello esistente
FILE_EXCEL = "Lista_Eventi_Bikers_Judaz.xlsx"
if not os.path.exists(FILE_EXCEL):
    df_init = pd.DataFrame(columns=["Nome Evento / Raduno", "Data", "Luogo", "Dettagli / Note", "Locandina", "Partecipanti"])
    df_init.to_excel(FILE_EXCEL, index=False)

# --- CSS INTEGRATO ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 7rem !important; }

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -20px !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }

.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; border-radius: 10px !important; color: white !important; }
.streamlit-expanderHeader { color: #ff9100 !important; font-weight: bold !important; font-size: 1.0rem !important; }

div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important;
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; 
}

/* Scritte bianche nel form */
label, .stTextInput label, .stTextArea label, .stFileUploader label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- FORM AGGIUNGI EVENTO ---
with st.expander("➕ AGGIUNGI EVENTO"):
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nome Evento")
        d = st.text_input("Data")
        l = st.text_input("Luogo")
        i = st.text_area("Info")
        f = st.file_uploader("Locandina", type=['jpg', 'png'])
        if st.form_submit_button("SALVA"):
            if not os.path.exists("locandine"): os.makedirs("locandine")
            path = os.path.join("locandine", f.name) if f else ""
            if f:
                with open(path, "wb") as file: file.write(f.getbuffer())
            
            df = pd.read_excel(FILE_EXCEL)
            nuovo = pd.DataFrame([{"Nome Evento / Raduno": n, "Data": d, "Luogo": l, "Dettagli / Note": i, "Locandina": path, "Partecipanti": 0}])
            df = pd.concat([df, nuovo], ignore_index=True)
            df.to_excel(FILE_EXCEL, index=False)
            st.rerun()

# --- LISTA EVENTI E LOGICA ---
try:
    df = pd.read_excel(FILE_EXCEL)
    # Forza la colonna partecipanti a essere numerica per evitare azzeramenti
    df['Partecipanti'] = pd.to_numeric(df['Partecipanti'], errors='coerce').fillna(0).astype(int)

    for i, row in df.iterrows():
        with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
            st.write(f"📍 **Luogo:** {row['Luogo']}")
            st.write(f"📝 **Info:** {row.get('Dettagli / Note', 'Nessuna info')}")
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            
            # Modifica Protetta da Password
            pwd = st.text_input(f"Password per modificare {i}", type="password", key=f"p_{i}")
            if pwd == "Judaz2026":
                new_info = st.text_area(f"Modifica Info {i}", value=str(row.get('Dettagli / Note', '')), key=f"edit_{i}")
                if st.button("SALVA MODIFICHE", key=f"save_{i}"):
                    df.at[i, 'Dettagli / Note'] = new_info
                    df.to_excel(FILE_EXCEL, index=False)
                    st.rerun()

        # Bottone Partecipa
        conteggio = int(row['Partecipanti'])
        label = f"CI VADO 🔥 {conteggio}"
        if ha_gia_votato(i):
            st.button(label, key=f"btn_{i}", disabled=True)
        else:
            if st.button(label, key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = conteggio + 1
                df.to_excel(FILE_EXCEL, index=False)
                registra_voto(i)
                st.rerun()

except Exception as e:
    st.error(f"Errore caricamento: {e}")

# --- MENU FISSO ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999;'>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>HOME</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>MC</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
