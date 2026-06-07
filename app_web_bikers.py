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

# --- CSS MINIMO (Solo estetica, non tocca la struttura) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.titolo-gotico { font-family: 'serif'; color: #ff9100; text-align: center; font-size: 2.6rem; }
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=200)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        # EXPANDER NATIVO: non stiamo forzando CSS qui, quindi non darà errori
        with st.expander(f"📅 {row['Nome Evento / Raduno']}"):
            st.write(f"📍 Luogo: {row['Luogo']}")
            st.write(f"📝 Note: {row.get('Dettagli / Note', 'Nessuna nota.')}")
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            
            # Bottone voto dentro la tendina
            conteggio = int(row.get('Partecipanti', 0))
            if ha_gia_votato(i):
                st.button(f"GIÀ PARTECIPATO 🔥 {conteggio}", key=f"btn_{i}", disabled=True)
            else:
                if st.button(f"CI VADO 🔥 {conteggio}", key=f"btn_{i}"):
                    df.at[i, 'Partecipanti'] = conteggio + 1
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    registra_voto(i)
                    st.rerun()

except Exception as e:
    st.error(f"Errore: {e}")
