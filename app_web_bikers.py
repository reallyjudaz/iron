import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

# --- CSS E STILE (Puro HTML/CSS per evitare errori Streamlit) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.event-card { 
    background-color: #1f2124; border: 2px solid #ff9100; 
    border-radius: 10px; padding: 15px; margin-bottom: 15px; 
    color: white; font-family: sans-serif;
}
.titolo-evento { color: #ff9100; font-size: 1.2rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#ff9100; text-align:center;'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- AGGIUNGI EVENTO ---
with st.expander("➕ AGGIUNGI NUOVO EVENTO"):
    with st.form("add_form"):
        n = st.text_input("Nome")
        if st.form_submit_button("SALVA"): st.success("Evento aggiunto!")

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    for i, row in df.iterrows():
        # Creiamo un contenitore semplice
        with st.container():
            st.markdown(f"<div class='event-card'><div class='titolo-evento'>{row['Nome Evento / Raduno']}</div>", unsafe_allow_html=True)
            st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
            
            # Bottone di voto standard (il più stabile in Streamlit)
            if st.button(f"CI VADO 🔥", key=f"voto_{i}"):
                registra_voto(i)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
except:
    st.error("Errore file.")
