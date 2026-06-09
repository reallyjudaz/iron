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

# --- CSS DEFINITIVO (FORZATO) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.titolo-gotico { font-family: 'serif'; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; }
.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; color: white !important; }

/* Forza il testo nero dentro i bottoni di salvataggio e cancella */
div[data-testid="stFormSubmitButton"] button p { color: black !important; font-weight: bold !important; }
div[data-testid="stFormSubmitButton"] button { background-color: #ff9100 !important; color: black !important; }

/* Forza il testo nero dentro il bottone 'CI VADO' */
div[data-testid="stButton"] button p { color: black !important; font-weight: bold !important; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; }

label { color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- AGGIUNGI ---
with st.expander("➕ AGGIUNGI EVENTO"):
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nome Evento"); d = st.text_input("Data (es: 27 giugno 2026)"); l = st.text_input("Luogo"); i = st.text_area("Info")
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

# --- LISTA EVENTI ---
df = pd.read_excel(FILE_EXCEL)

# ORDINAMENTO: se la data non viene letta, la forziamo a una data lontanissima per metterla in fondo
df['Data_Ord'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce').fillna(pd.Timestamp('2099-12-31'))
df = df.sort_values(by='Data_Ord', ascending=True)

for idx, row in df.iterrows():
    event_id = str(row['ID'])
    with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
        st.write(f"📍 {row['Luogo']} | 📝 {row.get('Dettagli / Note', '')}")
        if os.path.exists(str(row.get('Locandina', ''))): st.image(row['Locandina'], use_container_width=True)
        
        if st.text_input("Password Admin", type="password", key=f"p_{event_id}") == "Judaz2026":
            with st.form(f"mod_form_{event_id}"):
                new_n = st.text_input("Nome", value=row['Nome Evento / Raduno'])
                new_d = st.text_input("Data", value=row['Data'])
                new_l = st.text_input("Luogo", value=row['Luogo'])
                new_i = st.text_area("Info", value=row.get('Dettagli / Note', ''))
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("SALVA"):
                    df.loc[df['ID'] == event_id, ['Nome Evento / Raduno', 'Data', 'Luogo', 'Dettagli / Note']] = [new_n, new_d, new_l, new_i]
                    df.to_excel(FILE_EXCEL, index=False); st.rerun()
                if c2.form_submit_button("CANCELLA EVENTO"):
                    df = df[df['ID'] != event_id]
                    df.to_excel(FILE_EXCEL, index=False); st.rerun()

    if st.button(f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}", key=f"btn_{event_id}"):
        df.loc[df['ID'] == event_id, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
        df.to_excel(FILE_EXCEL, index=False); registra_voto(event_id); st.rerun()
