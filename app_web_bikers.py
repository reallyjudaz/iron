# Lista Eventi
    for i, row in df.iterrows():
        nome = str(row.get('Nome Evento / Raduno', 'Evento'))
        
        # Legge il numero esistente nel file (converte in intero per sicurezza)
        try:
            conteggio = int(row.get('Partecipanti', 0))
        except:
            conteggio = 0
            
        st.markdown(f"<div class='event-box'><h3>{nome}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p>", unsafe_allow_html=True)
        
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        
        # Logica bottone: CI VADO + Fiammella + Numero
        label = f"CI VADO 🔥 {conteggio}"
        
        # Controllo univocità nella sessione
        if 'ha_votato' not in st.session_state: st.session_state.ha_votato = []
        
        if i in st.session_state.ha_votato:
            st.button(label, key=f"btn_{i}", disabled=True)
        else:
            if st.button(label, key=f"btn_{i}"):
                # Incrementa nel dataframe
                df.at[i, 'Partecipanti'] = conteggio + 1
                # Salva subito nel file Excel
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                # Segna come votato
                st.session_state.ha_votato.append(i)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
