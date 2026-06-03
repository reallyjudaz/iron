import streamlit as st
import pandas as pd
import os

# Configurazione pagina
st.set_page_config(page_title="Iron & Rubber", layout="centered")

# CSS aggiornato: centraggio forzato e font "cattivo"
st.markdown("""
<style>
.stApp { background-color: #161719; }

/* Centra tutto nel contenitore principale */
.main .block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Centratura specifica per il logo */
div[data-testid="stImage"] {
    display: flex;
    justify-content: center !important;
}

/* Font Biker per il titolo */
.titolo-biker {
    font-family: 'Impact', sans-serif !important;
    text-align: center;
    color: #ff9100 !important;
    font-size: 2.5rem !important;
    margin-top: 10px;
    margin-bottom: 20px;
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
h3 { color: #ff9100; font-size: 1.6rem !important; margin-bottom: 5px !important; }

/* Nasconde il menu di Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Logo (Ingrandito e centrato)
if os.path.exists("logo_custom.png"):
    try:
        st.image("logo_custom.png", width=250)
    except:
        pass

# Titolo con font personalizzato
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
                    st.write("*(Locandina non visualizzabile)*")
            else:
                st.write("*(Nessuna locandina)*")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Errore di lettura: {e}")
