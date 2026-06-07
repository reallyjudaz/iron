import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- INIZIALIZZAZIONE STATO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'lista'

# --- FUNZIONI ---
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
.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}
.block-container { padding-bottom: 120px !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive; color: #ff9100; font-size: 2.6rem; }
div[data-testid="stButton"] button { background-color: #ff9100 !important; color: black !important; font-weight: bold !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- LOGICA PAGINE ---
if st.session_state.pagina == 'lista':
    # VISUALIZZAZIONE LISTA
    st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
    
    try:
        df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
        for i, row in df.iterrows():
            with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
                st.write(f"📍 {row['Luogo']}")
                st.write(f"📝 {row.get('Dettagli / Note', '')}")
                if os.path.exists(str(row.get('Locandina', ''))):
                    st.image(str(row['Locandina']), use_container_width=True)
            
            if st.button(f"CI VADO 🔥 {int(row.get('Partecipanti', 0))}", key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = int(row.get('Partecipanti', 0)) + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()
    except:
        st.error("Errore nel caricamento eventi.")

    # MENU FISSO (Tasto per passare ad Aggiungi)
    if st.button("➕ AGGIUNGI EVENTO", key="btn_aggiungi"):
        st.session_state.pagina = 'aggiungi'
        st.rerun()

elif st.session_state.pagina == 'aggiungi':
    # PAGINA AGGIUNGI EVENTO
    st.subheader("Nuovo Raduno")
    with st.form("form_evento"):
        nome = st.text_input("Nome Evento")
        data = st.date_input("Data")
        luogo = st.text_input("Luogo")
        note = st.text_area("Note / Dettagli")
        uploaded_file = st.file_uploader("Carica Locandina", type=['jpg', 'png'])
        
        submit = st.form_submit_button("Salva Evento")
        
        if submit:
            # Qui salveresti i dati nel file Excel
            st.success("Evento salvato!")
            if st.button("Torna alla lista"):
                st.session_state.pagina = 'lista'
                st.rerun()
