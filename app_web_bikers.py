# --- CSS CORRETTO PER MANTENERE IL LOOK DI "PRIMA.JPG" ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, footer, header {visibility: hidden !important; height: 0 !important;}

/* Forza il colore degli expander per tornare al nero/arancione */
.stExpander { 
    background-color: #1f2124 !important; 
    border: 2px solid #ff9100 !important; 
    border-radius: 10px !important; 
    margin-bottom: 15px !important;
}

/* Forza il testo dell'expander a essere visibile */
.streamlit-expanderHeader { 
    color: #ff9100 !important; 
    font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important;
}

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; }

/* Bottoni */
div[data-testid="stButton"] button {
    background-color: #ff9100 !important; color: black !important; 
    font-weight: bold !important; font-family: 'Special Elite', cursive !important; 
    border-radius: 5px !important; height: 38px !important; width: 100%;
}
</style>
""", unsafe_allow_html=True)
