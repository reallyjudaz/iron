import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #161719; }

/* Centratura totale */
.block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Logo container */
.logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

/* Titolo ridotto e centrato */
.titolo-biker {
    font-family: 'Impact', sans-serif !important;
    text-align: center;
    color: #ff9100 !important;
    font-size: 1.8rem !important; /* Ridotto */
    margin: 10px 0;
}

.dettaglio-box { 
    background-color: #1f2124; 
    padding: 15px; 
    margin-bottom: 15px; 
    border: 3px solid #ff9100; 
    border-radius: 10px; 
    color: white; 
    width: 100%;
}
h3 { color: #ff9100; font-size: 1.4rem !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Logo in un contenitore centrato
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("logo_custom.png", width=200) # Leggermente più piccolo
    st.markdown('</div>', unsafe_allow_html=True)

# Titolo compatto
st.markdown("<h1 class='titolo-biker'>IRON & RUBBER</h1>", unsafe_allow_html=True)

# Caricamento Dati
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento senza nome'))
        data = str(row.get('Data', 'N/D'))
        luogo = str(row.get('Luogo', 'N/D'))
        locandina = str(row.get('Locandina', ''))
        
        with st.container():
            st.markdown('<div class="dettaglio-box">', unsafe_allow_html=True)
            st.subheader(nome)
            st.write(f"📅 **{data}** | 📍 **{luogo}**")
            
            if locandina and os.path.exists(locandina):
                try:
                    st.image(locandina, use_container_width=True)
                except:
                    st.write("*(Errore immagine)*")
            else:
                st.write("*(Nessuna locandina)*")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Errore: {e}")
