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

# --- CSS DEFINITIVO ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, header {visibility: hidden !important;}
/* Spazio extra sotto per evitare che il menu sia coperto */
.block-container { padding-top: 0rem !important; padding-bottom: 120px !important; }

.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
.dettaglio-box { background-color: #1f2124; padding: 20px; border: 3px solid #ff9100; border-radius: 15px; color: white; margin-bottom: 20px; }

div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    border-radius: 5px !important; border: none !important; width: 100%; height: 40px; 
}
</style>
""", unsafe_allow_html=True)

# --- LOGICA CARICAMENTO ---
if 'dettaglio_id' not in st.session_state: st.session_state.dettaglio_id = None

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    
    # --- INTERFACCIA ---
    if st.session_state.dettaglio_id is None:
        # LISTA EVENTI
        for i, row in df.iterrows():
            st.markdown(f"<div class='event-box'><h3>{row['Nome Evento / Raduno']}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p></div>", unsafe_allow_html=True)
            if st.button("VEDI DETTAGLI", key=f"btn_{i}"):
                st.session_state.dettaglio_id = i
                st.rerun()
    else:
        # DETTAGLIO
        i = st.session_state.dettaglio_id
        row = df.iloc[i]
        st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.subheader(row['Nome Evento / Raduno'])
        st.write(f"📅 **Data:** {row['Data']}")
        st.write(f"📍 **Luogo:** {row['Luogo']}")
        st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
        
        img = str(row.get('Locandina', ''))
        if img and os.path.exists(img): st.image(img, use_container_width=True)
        
        if st.button("⬅ TORNA ALLA LISTA"):
            st.session_state.dettaglio_id = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception:
    st.error("Errore: Assicurati che il file Excel esista e sia chiuso.")

# --- MENU FISSO (Posizionato in basso) ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 15px 0; border-top: 3px solid #ff9100; display: flex; justify-content: space-evenly; z-index: 999;'>
    <span style='color:#ff9100; font-weight:bold;'>HOME</span>
    <span style='color:#ff9100; font-weight:bold;'>MC</span>
    <span style='color:#ff9100; font-weight:bold;'>ADMIN</span>
</div>
""", unsafe_allow_html=True)
