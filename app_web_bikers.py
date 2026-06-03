import streamlit as st
import pandas as pd
from PIL import Image
import os

# Configurazione pagina per mobile
st.set_page_config(page_title="Iron & Rubber", layout="centered")

# CSS per stile "cattivo" e compatto
st.markdown("""
<style>
.stApp { background-color: #161719; }
.dettaglio-box {
    background-color: #1f2124;
    padding: 10px;
    margin-bottom: 10px;
    border: 3px solid #ff9100;
    border-radius: 5px;
    color: white;
}
h3 { color: #ff9100; font-size: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# Titolo e Logo
st.image("logo_custom.png", width=150)
st.title("Iron & Rubber")

# Caricamento Dati
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    
# Sostituisci il blocco for nel tuo codice con questo:
    for index, row in df.iterrows():
        # Convertiamo il valore della locandina in stringa per sicurezza
        locandina_path = str(row['Locandina']) if pd.notna(row['Locandina']) else ""
        
        with st.container():
            st.markdown('<div class="dettaglio-box">', unsafe_allow_html=True)
            st.subheader(row['Nome Evento'])
            st.write(f"📅 {row['Data']} | 📍 {row['Luogo']}")
            
            # Controlliamo se il file esiste e se il percorso è valido
            if locandina_path and os.path.exists(locandina_path):
                st.image(locandina_path, use_container_width=True)
            else:
                st.write("*(Nessuna locandina disponibile)*")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Errore nel caricamento dati: {e}")
