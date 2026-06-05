import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

st.markdown("""
<style>
/* Font */
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important;}

.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; align-items: center !important; }

/* Logo & Titoli */
.logo-wrapper { display: flex !important; justify-content: center !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important; margin-bottom: 0px !important; }
.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -40px !important; margin-bottom: 0px !important; text-shadow: 2px 2px 4px #000; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-top: -5px !important; margin-bottom: 20px !important; }

/* Box Eventi */
.event-box { background-color: #1f2124; padding: 10px; margin-bottom: 12px; border: 2px solid #ff9100; border-radius: 10px; color: white; text-align: center; }
.event-box h3 { font-family: sans-serif !important; font-size: 1.0rem !important; margin-bottom: 5px !important; text-transform: uppercase; color: #ff9100; }
.event-box p { font-family: sans-serif !important; font-size: 0.8rem !important; margin-bottom: 10px !important; opacity: 0.9; }

/* Contatore Targhetta - Bordo stretto, font Special Elite */
.contatore-targhetta { 
    display: inline-block;
    background-color: #1f2124; 
    color: #ff9100; 
    padding: 5px 12px; 
    border-radius: 5px; 
    font-family: 'Special Elite', cursive; 
    font-weight: bold; 
    border: 2px solid #ff9100; 
    text-align: center;
    line-height: 25px;
}

/* Bottone */
div[data-testid="stButton"] button {
    background-color: #ff9100 !important;
    color: black !important;
    border: none !important;
    font-weight: bold !important;
    font-family: 'Special Elite', cursive !important;
    border-radius: 5px !important;
    height: 38px !important; /* Allineato all'altezza della targhetta */
    width: 100%;
}

/* Menu */
.menu-fisso { position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; display: flex; justify-content: flex-start; gap: 30px; padding: 15px 20px; border-top: 3px solid #ff9100; z-index: 9999; }
.menu-btn { font-family: 'Special Elite', cursive !important; color: #ff9100 !important; font-weight: bold; text-decoration: none; font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

# Logo
if os.path.exists("logo_custom.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo_custom.png")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)
st.markdown("<p class='sottotitolo'>«Non è la meta, è la strada a rivelare chi sei.»</p>", unsafe_allow_html=True)

# Lista Eventi
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
    if 'voti' not in st.session_state: st.session_state.voti = {}

    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        if nome not in st.session_state.voti: st.session_state.voti[nome] = 0
        
        st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
        
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        
        # Layout riga pulsante + targhetta
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            if st.button("PARTECIPERÒ!", key=f"btn_{i}"):
                st.session_state.voti[nome] += 1
                st.rerun()
        with col2:
            # La targhetta ora avvolge strettamente il contenuto
            st.markdown(f"<div class='contatore-targhetta'>🔥 {st.session_state.voti[nome]}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
except Exception:
    pass

# Menu
st.markdown("""
<div class='menu-fisso'>
    <a href='#' class='menu-btn'>HOME</a>
    <a href='#' class='menu-btn'>MC</a>
    <a href='#' class='menu-btn'>ADMIN</a>
</div>
""", unsafe_allow_html=True)
