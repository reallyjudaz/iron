import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #161719; }
.dettaglio-box { background-color: #1f2124; padding: 10px; margin-bottom: 10px; border: 3px solid #ff9100; border-radius: 5px; color: white; }
h3 { color: #ff9100; font-size: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# Controlla se il logo esiste, altrimenti salta
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=150)
st.title("Iron & Rubber")

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        # Usiamo il nome colonna esatto che hai trovato tu!
        nome = str(row.get('Nome Evento / Raduno', 'Evento senza nome'))
        data = str(row.get('Data', 'N/D'))
        luogo = str(row.get('Luogo', 'N/D'))
        locandina = str(row.get('Locandina', ''))
        
        with st.container():
            st.markdown('<div class="dettaglio-box">', unsafe_allow_html=True)
            st.subheader(nome)
            st.write(f"📅 {data} | 📍 {luogo}")
            
            if locandina and os.path.exists(locandina):
                st.image(locandina, use_container_width=True)
            else:
                st.write("*(Nessuna locandina disponibile)*")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Errore nel caricamento: {e}")
