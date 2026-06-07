import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI DI MEMORIA ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; }
.logo-wrapper { display: flex !important; justify-content: center !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.dettaglio-box { background-color: #1f2124; padding: 25px; border: 3px solid #ff9100; border-radius: 15px; color: white; text-align: center; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- STATO ---
if 'evento_aperto' not in st.session_state: st.session_state.evento_aperto = None

# --- HEADER (FISSO) ---
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- LOGICA ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    if st.session_state.evento_aperto is None:
        # VISUALIZZAZIONE LISTA
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            conteggio = int(row.get('Partecipanti', 0))
            
            st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
            
            # Bottoni Info e Partecipa
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("INFO", key=f"info_{i}"):
                    st.session_state.evento_aperto = i
                    st.rerun()
            with c2:
                label = f"CI VADO 🔥 {conteggio}"
                if ha_gia_votato(i): st.button(label, key=f"btn_{i}", disabled=True)
                else:
                    if st.button(label, key=f"btn_{i}"):
                        df.at[i, 'Partecipanti'] = conteggio + 1
                        df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                        registra_voto(i)
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # VISUALIZZAZIONE DETTAGLIO
        idx = st.session_state.evento_aperto
        row = df.iloc[idx]
        st.markdown(f"<div class='dettaglio-box'><h2>{row['Nome Evento / Raduno']}</h2>", unsafe_allow_html=True)
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path): st.image(img_path, use_container_width=True)
        st.write(f"📅 Data: {row['Data']} | 📍 Luogo: {row['Luogo']}")
        if st.button("⬅ TORNA ALLA LISTA"):
            st.session_state.evento_aperto = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error("Carica il file Excel per iniziare.")

# --- MENU (FISSO IN BASSO) ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 15px; border-top: 3px solid #ff9100; display: flex; justify-content: space-around; z-index: 9999;'>
    <b style='color:#ff9100;'>HOME</b><b style='color:#ff9100;'>MC</b><b style='color:#ff9100;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
