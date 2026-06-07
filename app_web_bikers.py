import streamlit as st
import pandas as pd
import os

# --- SETUP ---
st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f: f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f: return str(id_evento) in f.read().splitlines()

# --- CARICAMENTO DATI ---
if not os.path.exists("Lista_Eventi_Bikers_Judaz.xlsx"):
    pd.DataFrame(columns=["Nome Evento / Raduno", "Data", "Luogo", "Dettagli / Note", "Locandina", "Partecipanti"]).to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)

# --- UI ---
st.title("Iron & Rubber")

# 1. FORM AGGIUNGI (Sempre presente in alto)
with st.expander("➕ AGGIUNGI NUOVO EVENTO"):
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nome")
        d = st.text_input("Data")
        l = st.text_input("Luogo")
        i = st.text_area("Info")
        f = st.file_uploader("Locandina", type=['jpg', 'png'])
        if st.form_submit_button("SALVA"):
            if not os.path.exists("locandine"): os.makedirs("locandine")
            path = os.path.join("locandine", f.name) if f else ""
            if f:
                with open(path, "wb") as file: file.write(f.getbuffer())
            df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
            nuovo = pd.DataFrame([{"Nome Evento / Raduno": n, "Data": d, "Luogo": l, "Dettagli / Note": i, "Locandina": path, "Partecipanti": 0}])
            pd.concat([df, nuovo]).to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
            st.rerun()

# 2. LISTA EVENTI
df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
for idx, row in df.iterrows():
    with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
        st.write(f"📍 {row['Luogo']}")
        st.write(f"📝 {row.get('Dettagli / Note', 'Nessuna info')}")
        if os.path.exists(str(row.get('Locandina', ''))): st.image(row['Locandina'])
        
        # Area modifica protetta (dentro la tendina)
        with st.expander("🔑 Sblocca Modifica"):
            pwd = st.text_input("Password", type="password", key=f"pwd_{idx}")
            if pwd == "Judaz2026":
                new_info = st.text_area("Modifica Info", value=row.get('Dettagli / Note', ''), key=f"edit_{idx}")
                if st.button("SALVA MODIFICHE", key=f"save_{idx}"):
                    df.at[idx, 'Dettagli / Note'] = new_info
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    st.success("Salvato!")
                    st.rerun()

    # Voto
    if st.button(f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}", key=f"btn_{idx}", disabled=ha_gia_votato(idx)):
        df.at[idx, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
        df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
        registra_voto(idx)
        st.rerun()
