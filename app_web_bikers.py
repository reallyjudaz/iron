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

# --- CARICAMENTO SICURO ---
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
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; }
.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; color: white !important; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; width: 100%; }
label, .stTextInput label, .stTextArea label, .stFileUploader label { color: white !important; }
</style>
""", unsafe_allow_html=True)

if os.path.exists("logo_custom.png"): st.image("logo_custom.png", use_container_width=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- AGGIUNGI EVENTO ---
with st.expander("➕ AGGIUNGI EVENTO"):
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nome Evento")
        d = st.text_input("Data (AAAA-MM-GG)")
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
            pd.concat([df, nuovo], ignore_index=True).to_excel(FILE_EXCEL, index=False)
            st.rerun()

# --- LISTA E MODIFICA/ELIMINA ---
df = pd.read_excel(FILE_EXCEL)
df['Data_Date'] = pd.to_datetime(df['Data'], errors='coerce')
df = df.sort_values(by='Data_Date', ascending=True)

for idx, row in df.iterrows():
    # Usiamo l'indice originale per non perdere i riferimenti
    original_idx = idx 
    with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
        st.write(f"📍 **Luogo:** {row['Luogo']}")
        st.write(f"📝 **Info:** {row.get('Dettagli / Note', 'Nessuna info')}")
        if os.path.exists(str(row.get('Locandina', ''))): st.image(row['Locandina'], use_container_width=True)
        
        pwd = st.text_input(f"Password Admin", type="password", key=f"p_{idx}")
        if pwd == "Judaz2026":
            with st.form(f"mod_form_{idx}"):
                new_n = st.text_input("Nome", value=row['Nome Evento / Raduno'])
                new_d = st.text_input("Data", value=row['Data'])
                new_l = st.text_input("Luogo", value=row['Luogo'])
                new_i = st.text_area("Info", value=row.get('Dettagli / Note', ''))
                new_f = st.file_uploader("Cambia Locandina", type=['jpg', 'png'])
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("SALVA MODIFICHE"):
                    df.at[original_idx, 'Nome Evento / Raduno'] = new_n
                    df.at[original_idx, 'Data'] = new_d
                    df.at[original_idx, 'Luogo'] = new_l
                    df.at[original_idx, 'Dettagli / Note'] = new_i
                    if new_f:
                        path = os.path.join("locandine", new_f.name)
                        with open(path, "wb") as file: file.write(new_f.getbuffer())
                        df.at[original_idx, 'Locandina'] = path
                    df.to_excel(FILE_EXCEL, index=False)
                    st.rerun()
                
                if col2.form_submit_button("❌ ELIMINA EVENTO"):
                    df = df.drop(original_idx)
                    df.to_excel(FILE_EXCEL, index=False)
                    st.rerun()

    if st.button(f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}", key=f"btn_{idx}", disabled=ha_gia_votato(idx)):
        df.at[original_idx, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
        df.to_excel(FILE_EXCEL, index=False)
        registra_voto(idx)
        st.rerun()
