import streamlit as st
import pandas as pd
import os
import uuid

st.set_page_config(page_title="Iron & Rubber", layout="centered")

FILE_EXCEL = "Lista_Eventi_Bikers_Judaz.xlsx"

# --- FUNZIONI ---
def registra_voto(id_univoco):
    with open("voti_fatti.txt", "a") as f: f.write(f"{id_univoco}\n")
def ha_gia_votato(id_univoco):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f: return str(id_univoco) in f.read().splitlines()

# --- CARICAMENTO ---
if not os.path.exists(FILE_EXCEL):
    df = pd.DataFrame(columns=["ID", "Nome Evento / Raduno", "Data", "Luogo", "Dettagli / Note", "Locandina", "Partecipanti"])
    df.to_excel(FILE_EXCEL, index=False)
else:
    df = pd.read_excel(FILE_EXCEL)
    if 'ID' not in df.columns:
        df['ID'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_excel(FILE_EXCEL, index=False)

# --- CSS DEFINITIVO ---
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

div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button { 
    background-color: #ff9100 !important; 
    color: black !important; 
    font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important;
}

label { color: white !important; }
</style>
""", unsafe_allow_html=True)

if os.path.exists("logo_custom.png"): st.image("logo_custom.png", use_container_width=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- AGGIUNGI EVENTO ---
with st.expander("➕ AGGIUNGI EVENTO"):
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nome Evento"); d = st.text_input("Data (AAAA-MM-GG)"); l = st.text_input("Luogo"); i = st.text_area("Info")
        f = st.file_uploader("Locandina", type=['jpg', 'png'])
        if st.form_submit_button("SALVA"):
            if not os.path.exists("locandine"): os.makedirs("locandine")
            path = os.path.join("locandine", f.name) if f else ""
            if f:
                with open(path, "wb") as file: file.write(f.getbuffer())
            df = pd.read_excel(FILE_EXCEL)
            nuovo = pd.DataFrame([{"ID": str(uuid.uuid4()), "Nome Evento / Raduno": n, "Data": d, "Luogo": l, "Dettagli / Note": i, "Locandina": path, "Partecipanti": 0}])
            pd.concat([df, nuovo], ignore_index=True).to_excel(FILE_EXCEL, index=False)
            st.rerun()

# --- TITOLO SEZIONE ---
st.markdown("<p class='sottotitolo' style='margin-top: 30px;'>PROSSIMI EVENTI</p>", unsafe_allow_html=True)

# --- LISTA EVENTI ---
df = pd.read_excel(FILE_EXCEL)
df['Data_Date'] = pd.to_datetime(df['Data'], errors='coerce')
df = df.sort_values(by='Data_Date', ascending=True)

for idx, row in df.iterrows():
    event_id = str(row['ID'])
    with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
        st.write(f"📍 {row['Luogo']} | 📝 {row.get('Dettagli / Note', '')}")
        if os.path.exists(str(row.get('Locandina', ''))): st.image(row['Locandina'], use_container_width=True)
        
        pwd = st.text_input("Password Admin", type="password", key=f"p_{event_id}")
        if pwd == "Judaz2026":
            with st.form(f"mod_form_{event_id}"):
                new_n = st.text_input("Nome", value=row['Nome Evento / Raduno'])
                new_d = st.text_input("Data", value=row['Data'])
                new_l = st.text_input("Luogo", value=row['Luogo'])
                new_i = st.text_area("Info", value=row.get('Dettagli / Note', ''))
                new_f = st.file_uploader("Aggiorna Locandina", type=['jpg', 'png'])
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("SALVA"):
                    path = row['Locandina']
                    if new_f:
                        path = os.path.join("locandine", new_f.name)
                        with open(path, "wb") as file: file.write(new_f.getbuffer())
                    df.loc[df['ID'] == event_id, ['Nome Evento / Raduno', 'Data', 'Luogo', 'Dettagli / Note', 'Locandina']] = [new_n, new_d, new_l, new_i, path]
                    df.to_excel(FILE_EXCEL, index=False); st.rerun()
                if c2.form_submit_button("CANCELLA EVENTO"):
                    df = df[df['ID'] != event_id]
                    df.to_excel(FILE_EXCEL, index=False); st.rerun()

    if st.button(f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}", key=f"btn_{event_id}", disabled=ha_gia_votato(event_id)):
        df.loc[df['ID'] == event_id, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
        df.to_excel(FILE_EXCEL, index=False); registra_voto(event_id); st.rerun()

# --- MENU FISSO ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999;'>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>HOME</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>MC</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
