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
.event-box { background-color: #1f2124; padding: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; margin-bottom: 10px; }
.dettaglio-box { background-color: #1f2124; padding: 25px; border: 3px solid #ff9100; border-radius: 15px; color: white; margin-bottom: 100px; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; width: 100%; border: none !important; }
</style>
""", unsafe_allow_html=True)

if 'dettaglio_id' not in st.session_state: st.session_state.dettaglio_id = None

# --- CARICAMENTO ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except:
    df = pd.DataFrame()

# --- LOGICA ---
if not df.empty:
    if st.session_state.dettaglio_id is None:
        # PAGINA LISTA
        for i, row in df.iterrows():
            st.markdown(f"<div class='event-box'>", unsafe_allow_html=True)
            # Solo il titolo come bottone per aprire
            if st.button(f"{row['Nome Evento / Raduno']}", key=f"t_{i}"):
                st.session_state.dettaglio_id = i
                st.rerun()
            st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
            
            # Voto
            label = f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}"
            if ha_gia_votato(i): st.button(label, key=f"b_{i}", disabled=True)
            elif st.button(label, key=f"b_{i}"):
                df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # PAGINA DETTAGLIO (Dentro il quadrato arancione)
        i = st.session_state.dettaglio_id
        row = df.iloc[i]
        
        st.markdown("<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.subheader(row['Nome Evento / Raduno'])
        st.write(f"📅 **Data:** {row['Data']}")
        st.write(f"📍 **Luogo:** {row['Luogo']}")
        st.markdown(f"<div style='color:white; margin-top:10px;'>{row.get('Dettagli / Note', '')}</div>", unsafe_allow_html=True)
        
        img = str(row.get('Locandina', ''))
        if img and os.path.exists(img): st.image(img, use_container_width=True)
        
        if st.button("BACK"):
            st.session_state.dettaglio_id = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO (Fuori da tutto) ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 20px; border-top: 3px solid #ff9100; display: flex; justify-content: space-around; z-index: 9999;'>
    <b style='color:#ff9100;'>HOME</b><b style='color:#ff9100;'>MC</b><b style='color:#ff9100;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
