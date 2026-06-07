import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI PER MEMORIA PERMANENTE ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"):
        return False
    with open("voti_fatti.txt", "r") as f:
        voti = f.read().splitlines()
        return str(id_evento) in voti

# --- CSS E STILE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; }

.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; margin-bottom: 0px !important; text-shadow: 2px 2px 4px #000; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-top: -5px !important; margin-bottom: 20px !important; }

.event-box { background-color: #1f2124; padding: 10px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.event-box h3 { font-family: sans-serif !important; font-size: 1.0rem !important; margin-bottom: 5px !important; text-transform: uppercase; color: #ff9100; }
.event-box p { font-family: sans-serif !important; font-size: 0.8rem !important; margin-bottom: 10px !important; opacity: 0.9; }

div[data-testid="stButton"] button {
    background-color: #ff9100 !important; color: black !important; border: none !important; 
    font-weight: bold !important; font-family: 'Special Elite', cursive !important; 
    border-radius: 5px !important; height: 38px !important; width: 100%;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO E TITOLI ---
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# --- AGGIUNGI EVENTO (Modulo in cima) ---
with st.expander("➕ AGGIUNGI NUOVO EVENTO"):
    with st.form("form_aggiungi", clear_on_submit=True):
        new_nome = st.text_input("Nome Evento")
        new_data = st.text_input("Data (es. 15/07/2026)")
        new_luogo = st.text_input("Luogo")
        if st.form_submit_button("SALVA EVENTO"):
            st.success("Evento aggiunto! (Aggiorna il file Excel)")

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        try:
            conteggio = int(row.get('Partecipanti', 0))
        except:
            conteggio = 0
            
        # Trasformazione in Menu a Tendina (Expander)
        with st.expander(f"{nome}"):
            st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
            
            img_path = str(row.get('Locandina', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
                
            label = f"CI VADO 🔥 {conteggio}"
            
            if ha_gia_votato(i):
                st.button(label, key=f"btn_{i}", disabled=True)
            else:
                if st.button(label, key=f"btn_{i}"):
                    df.at[i, 'Partecipanti'] = conteggio + 1
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    registra_voto(i)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Errore: {e}. Assicurati che il file Excel sia chiuso.")

# --- MENU ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999;'>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>HOME</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>MC</a>
    <a href='#' style='font-family: Special Elite; color: #ff9100; font-weight: bold; text-decoration: none; font-size: 1.2rem;'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
