import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import uuid

# --- CONFIGURAZIONE GOOGLE SHEETS ---
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_key.json', scope)
    client = gspread.authorize(creds)
    # app motoraduni
    sheet = client.open("app motoraduni").sheet1
    return sheet

sheet = get_google_sheet()

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.titolo-gotico { font-family: 'Georgia', serif; text-align: center; color: #ff9100; font-size: 2.6rem; }
.sottotitolo { font-family: 'Georgia', serif; text-align: center; color: #ff9100; font-size: 1.6rem; margin-bottom: 20px; }
.testo-normale { font-family: sans-serif; text-align: center; color: #ff9100; font-size: 1.2rem; font-weight: bold; margin-bottom: 20px; }
.stExpander { background-color: #1f2124; border: 2px solid #ff9100; border-radius: 10px; color: white; }
div[data-testid="stButton"] button { background-color: #ff9100; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- LETTURA DATI ---
df = pd.DataFrame(sheet.get_all_records())

# --- AGGIUNGI EVENTO ---
with st.expander("➕ AGGIUNGI EVENTO"):
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nome Evento"); d = st.text_input("Data (AAAA-MM-GG)"); l = st.text_input("Luogo"); i = st.text_area("Info")
        if st.form_submit_button("SALVA"):
            sheet.append_row([str(uuid.uuid4()), n, d, l, i, "", 0])
            st.rerun()

# --- PROSSIMI EVENTI ---
st.markdown("<p class='testo-normale'>PROSSIMI EVENTI</p>", unsafe_allow_html=True)

for idx, row in df.iterrows():
    event_id = row['ID']
    with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
        st.write(f"📍 {row['Luogo']} | 📝 {row['Dettagli / Note']}")
        
        # Bottone "Ci Vado" (Aggiorna colonna Partecipanti)
        if st.button(f"CI VADO 🔥 {row['Partecipanti']}", key=f"btn_{event_id}"):
            new_val = int(row['Partecipanti']) + 1
            sheet.update_cell(idx + 2, df.columns.get_loc('Partecipanti') + 1, new_val)
            st.rerun()
