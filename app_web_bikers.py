# --- MENU FISSO CON POPOVER (Aggiungi Evento) ---
st.markdown("""
<style>
/* Stile per rendere il popover coerente con la tua grafica */
[data-testid="stPopover"] {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #1f2124;
    border-top: 3px solid #ff9100;
    z-index: 999999;
}
</style>
""", unsafe_allow_html=True)

# Creiamo un contenitore fisso per il menu
with st.container():
    st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True) # Spazio vuoto per non coprire gli ultimi elementi

# Inseriamo il popover nel menu fisso
with st.popover("➕ AGGIUNGI EVENTO", use_container_width=True):
    st.subheader("Nuovo Raduno")
    with st.form("form_aggiungi", clear_on_submit=True):
        nuovo_nome = st.text_input("Nome Evento")
        nuova_data = st.date_input("Data")
        nuovo_luogo = st.text_input("Luogo")
        nuove_note = st.text_area("Note")
        locandina = st.file_uploader("Carica Locandina (JPG/PNG)", type=['jpg', 'png'])
        
        if st.form_submit_button("Salva Evento"):
            # Qui creeremo la logica per salvare i dati nel file Excel
            st.success(f"Evento {nuovo_nome} aggiunto!")
            # Inseriremo qui il codice per aggiornare il dataframe
