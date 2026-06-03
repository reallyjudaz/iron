import streamlit as st
import pandas as pd
import os

# Configurazione pagina
st.set_page_config(page_title="Iron & Rubber", layout="centered")

# CSS aggiornato: centraggio logo e stile compatto
st.markdown("""
<style>
.stApp { background-color: #161719; }

/* Centra il logo e le immagini */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.dettaglio-box { 
    background-color: #1f2124; 
    padding: 15px; 
    margin-bottom: 15px; 
    border: 3px solid #ff9100; 
    border-radius: 10px; 
    color: white; 
}
h3 { color: #ff9100; font-size: 1.6rem !important; margin-bottom: 5px !important; }

/* Nasconde il menu di Streamlit e il footer */
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

st.markdown("<h1 style='text-align: center; color: white;'>Iron & Rubber</h1>", unsafe_allow_html=True)

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
            
            # Caricamento Locandina
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
