import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI PER MEMORIA PERMANENTE ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- CSS E STILE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 7rem !important; }
.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.dettaglio-box { background-color: #1f2124; padding: 20px; border: 3px solid #ff9100; border-radius: 15px; color: white; margin-bottom: 20px; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- STATO ---
if 'dettaglio_id' not in st.session_state: st.session_state.dettaglio_id = None

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    if st.session_state.dettaglio_id is None:
        for i, row in df.iterrows():
            st.markdown(f"<div class='event-box'>", unsafe_allow_html=True)
            # Tasto che fa da titolo e apre i dettagli
            if st.button(f"INFO: {row['Nome Evento / Raduno']}", key=f"title_{i}"):
                st.session_state.dettaglio_id = i
                st.rerun()
            st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
            
            label = f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}"
            if ha_gia_votato(i): st.button(label, key=f"btn_{i}", disabled=True)
            elif st.button(label, key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # VISUALIZZAZIONE DETTAGLIO
        i = st.session_state.dettaglio_id
        row = df.iloc[i]
        st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.subheader(row['Nome Evento / Raduno'])
        st.write(f"**Data:** {row['Data']} | **Luogo:** {row['Luogo']}")
        st.write(f"**Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
        
        img = str(row.get('Locandina', ''))
        if img and os.path.exists(img): st.image(img, use_container_width=True)
        
        if st.button("BACK"):
            st.session_state.dettaglio_id = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Errore: {e}")

# --- MENU ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: space-around; padding: 15px; border-top: 3px solid #ff9100; z-index: 9999;'>
    <b style='color:#ff9100;'>HOME</b><b style='color:#ff9100;'>MC</b><b style='color:#ff9100;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
