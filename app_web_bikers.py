# --- CSS AGGIORNATO (Sostituisci questo blocco nel tuo codice) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp { background-color: #161719; }
#MainMenu, header {visibility: hidden !important;}

/* AUMENTATO il padding-bottom: questo crea lo spazio necessario in fondo alla pagina */
.block-container { padding-top: 0rem !important; padding-bottom: 150px !important; }

.titolo-gotico { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 2.6rem !important; margin-top: -20px !important; }
.sottotitolo { font-family: 'UnifrakturMaguntia', cursive !important; text-align: center; color: #ff9100 !important; font-size: 1.4rem !important; margin-bottom: 20px !important; }

.stExpander { background-color: #1f2124 !important; border: 2px solid #ff9100 !important; border-radius: 10px !important; color: white !important; }
.streamlit-expanderHeader { color: #ff9100 !important; font-weight: bold !important; font-size: 1.0rem !important; }

div[data-testid="stButton"] button { 
    background-color: #ff9100 !important; color: black !important; font-weight: bold !important; 
    font-family: 'Special Elite', cursive !important; border-radius: 5px !important; height: 38px !important; width: 100%; 
}
</style>
""", unsafe_allow_html=True)

# --- ... (Lascia invariato il resto del codice fino al menu) ... ---

# --- MENU FISSO (Sostituisci anche questo blocco alla fine) ---
# Ho impostato 'bottom: 0px' ma con uno spazio maggiore nel padding del container sopra
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 20px 0; border-top: 3px solid #ff9100; display: flex; justify-content: space-around; z-index: 100; box-shadow: 0px -5px 10px rgba(0,0,0,0.5);'>
    <b style='color:#ff9100; font-family: Special Elite;'>HOME</b>
    <b style='color:#ff9100; font-family: Special Elite;'>MC</b>
    <b style='color:#ff9100; font-family: Special Elite;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
