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

# --- CSS PERSONALIZZATO PER L'EXPANDER ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, header {visibility: hidden !important;}
.block-container { padding-bottom: 100px !important; }

/* Rende l'expander trasparente e coerente con i tuoi box */
.stExpander { 
    background-color: #1f2124 !important; 
    border: 2px solid #ff9100 !important; 
    border-radius: 10px !important; 
}
.streamlit-expanderHeader { 
    color: #ff9100 !important; 
    font-weight: bold !important; 
    font-size: 1.1rem !important; 
}

/* Bottone VOTO stile originale */
div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    border-radius: 5px !important; border: none !important; width: 100%; height: 38px; 
}
</style>
""", unsafe_allow_html=True)

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        # L'expander diventa il tuo "box arancione" cliccabile
        with st.expander(f"{row['Nome Evento / Raduno']}"):
            st.write(f"📅 **Data:** {row['Data']}")
            st.write(f"📍 **Luogo:** {row['Luogo']}")
            st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

        # Bottone voto subito sotto
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
        st.markdown("<br>", unsafe_allow_html=True)

except Exception as e:
    st.error("Errore nel caricamento eventi.")

# --- MENU FISSO (Senza errori) ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 15px 0; border-top: 3px solid #ff9100; display: flex; justify-content: space-evenly; z-index: 9999;'>
    <b style='color:#ff9100;'>HOME</b><b style='color:#ff9100;'>MC</b><b style='color:#ff9100;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
