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

# --- CSS SEMPLIFICATO (Solo per i colori) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
[data-testid="stSidebar"] { display: none; }
.arancione { color: #ff9100; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- STATO ---
if 'dettaglio_id' not in st.session_state: st.session_state.dettaglio_id = None

# --- CARICAMENTO ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
except:
    df = pd.DataFrame()

# --- INTERFACCIA ---
if not df.empty:
    if st.session_state.dettaglio_id is None:
        # PAGINA LISTA - USIAMO UN CONTENITORE PULITO
        for i, row in df.iterrows():
            with st.container(border=True):
                st.subheader(row['Nome Evento / Raduno'])
                st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
                
                if st.button("INFO DETTAGLIATE", key=f"btn_info_{i}"):
                    st.session_state.dettaglio_id = i
                    st.rerun()
                    
                # Voto
                label = f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}"
                if ha_gia_votato(i): st.button(label, key=f"btn_voto_{i}", disabled=True)
                elif st.button(label, key=f"btn_voto_{i}"):
                    df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    registra_voto(i)
                    st.rerun()
    
    else:
        # PAGINA DETTAGLIO - USIAMO UN CONTENITORE ARANCIONE
        i = st.session_state.dettaglio_id
        row = df.iloc[i]
        
        # Usiamo un contenitore con bordo per emulare il quadrato
        with st.container(border=True):
            st.markdown("<h2 style='color:#ff9100;'>DETTAGLI EVENTO</h2>", unsafe_allow_html=True)
            st.subheader(row['Nome Evento / Raduno'])
            st.write(f"📅 **Data:** {row['Data']}")
            st.write(f"📍 **Luogo:** {row['Luogo']}")
            st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
            
            img = str(row.get('Locandina', ''))
            if img and os.path.exists(img): 
                st.image(img, use_container_width=True)
            
            if st.button("⬅ TORNA ALLA LISTA"):
                st.session_state.dettaglio_id = None
                st.rerun()

# --- MENU FISSO ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 15px; border-top: 3px solid #ff9100; text-align: center; z-index: 9999;'>
    <span style='color:#ff9100; margin: 0 15px;'>HOME</span>
    <span style='color:#ff9100; margin: 0 15px;'>MC</span>
    <span style='color:#ff9100; margin: 0 15px;'>ADMIN</span>
</div>
""", unsafe_allow_html=True)
