import streamlit as st
import pandas as pd
import os

# Configurazione mobile
st.set_page_config(page_title="Iron & Rubber", layout="centered")

# CSS "Blindato": nasconde tutto quello che disturba e centra in modo forzato
st.markdown("""
<style>
/* Sfondo nero */
.stApp { background-color: #161719; }

/* Forza il contenuto al centro e nasconde gli elementi di disturbo */
#MainMenu, footer, header, .viewerBadge_container__1QSob, .stDeployButton { visibility: hidden !important; display: none !important; }

/* Centratura logo e titoli */
.block-container { align-items: center !important; }

div[data-testid="stImage"] { 
    display: flex !important; 
    justify-content: center !important; 
    width: 100% !important; 
}

/* Titolo Stile Rock */
.titolo-rock {
    font-family: 'Impact', sans-serif !important;
    text-align: center;
    color: #ff9100 !important;
    font-size: 2.2rem !important;
    margin: 10px 0;
    text-transform: uppercase;
}

/* Box eventi */
.dettaglio-box { 
    background-color: #1f2124; 
    padding: 15px; 
    margin-bottom: 15px; 
    border: 3px solid #ff9100; 
    border-radius: 10px; 
    color: white; 
    width: 100%;
}
h3 { color: #ff9100; font-family: 'Impact', sans-serif !important; font-size: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)

# Logo Centrato
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", width=220)

# Titolo Rock
st.markdown("<h1 class='titolo-rock'>IRON & RUBBER</h1>", unsafe_allow_html=True)

# Dati
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    
    for index, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento senza nome'))
        data = str(row.get('Data', 'N/D'))
        luogo = str(row.get('Luogo', 'N/D'))
        locandina = str(row.get('Locandina', ''))
        
        st.markdown('<div class="dettaglio-box">', unsafe_allow_html=True)
        st.subheader(nome)
        st.write(f"📅 **{data}** | 📍 **{luogo}**")
        
        if locandina and os.path.exists(locandina):
            st.image(locandina, use_container_width=True)
        else:
            st.write("*(Nessuna locandina)*")
        st.markdown('</div>', unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Errore caricamento: {e}")
