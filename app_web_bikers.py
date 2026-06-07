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

# --- CSS OTTIMIZZATO MOBILE ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 7rem !important; }

.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.dettaglio-box { background-color: #1f2124; padding: 20px; border: 3px solid #ff9100; border-radius: 15px; color: white; text-align: center; }

/* Bottoni stile cellulare */
div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; 
    height: 45px !important; width: 100%; border: none !important;
}
/* Stile specifico tasto Apri Evento meno invasivo */
div[data-testid="stFormSubmitButton"] button { 
    background-color: #333 !important; color: #ff9100 !important; border: 1px solid #ff9100 !important; 
}
</style>
""", unsafe_allow_html=True)

# --- STATO E HEADER ---
if 'evento_aperto' not in st.session_state: st.session_state.evento_aperto = None

if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=True)

st.markdown("<h1 style='text-align:center; color:#ff9100; font-family:UnifrakturMaguntia;'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LOGICA ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    if st.session_state.evento_aperto is None:
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            conteggio = int(row.get('Partecipanti', 0))
            
            st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
            
            with st.form(key=f"form_{i}"):
                if st.form_submit_button("VEDI DETTAGLI"):
                    st.session_state.evento_aperto = i
                    st.rerun()

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
        idx = st.session_state.evento_aperto
        row = df.iloc[idx]
        st.markdown(f"<div class='dettaglio-box'><h2>{row['Nome Evento / Raduno']}</h2>", unsafe_allow_html=True)
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path): st.image(img_path, use_container_width=True)
        st.write(f"📅 Data: {row['Data']} | 📍 Luogo: {row['Luogo']}")
        
        if st.button("BACK"):
            st.session_state.evento_aperto = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception:
    st.error("Errore nel caricamento eventi.")

# --- MENU FISSO ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 20px 0; border-top: 3px solid #ff9100; display: flex; justify-content: space-around; z-index: 9999;'>
    <b style='color:#ff9100; font-family:Special Elite;'>HOME</b>
    <b style='color:#ff9100; font-family:Special Elite;'>MC</b>
    <b style='color:#ff9100; font-family:Special Elite;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
