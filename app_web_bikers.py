# --- CSS RESET - PULITO E COMPATIBILE ---
st.markdown("""
<style>
/* Reset globale */
.stApp { background-color: #161719; }

/* Forza il colore degli Expander */
div[data-testid="stExpander"] {
    background-color: #1f2124 !important;
    border: 2px solid #ff9100 !important;
    border-radius: 10px !important;
}

/* Forza il testo dell'header dell'Expander */
div[data-testid="stExpander"] div[role="button"] p {
    color: #ff9100 !important;
    font-family: 'Special Elite', cursive !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
}

/* Nasconde elementi di sistema che causano errori */
#MainMenu, footer, header {visibility: hidden !important;}

/* Stile bottoni */
div[data-testid="stButton"] button {
    background-color: #ff9100 !important;
    color: black !important;
    font-weight: bold !important;
    font-family: 'Special Elite', cursive !important;
    border-radius: 5px !important;
}
</style>
""", unsafe_allow_html=True)
