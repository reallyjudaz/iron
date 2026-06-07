# --- LOGICA (Sostituisci il blocco "LOGICA" precedente con questo) ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    if st.session_state.evento_aperto is None:
        # VISUALIZZAZIONE LISTA
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            conteggio = int(row.get('Partecipanti', 0))
            
            # Box interamente cliccabile senza tasto extra
            st.markdown(f"""
            <div class='event-box'>
                <h3>{nome}</h3>
                <p style='font-size:0.7rem;'>📅 {row['Data']} | 📍 {row['Luogo']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Bottone di selezione (che funge da "apri")
            if st.button(f"APRI {nome[:15]}...", key=f"apri_{i}"):
                st.session_state.evento_aperto = i
                st.rerun()

            label = f"CI VADO 🔥 {conteggio}"
            if ha_gia_votato(i): st.button(label, key=f"btn_{i}", disabled=True)
            else:
                if st.button(label, key=f"btn_{i}"):
                    df.at[i, 'Partecipanti'] = conteggio + 1
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    registra_voto(i)
                    st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            
    else:
        # VISUALIZZAZIONE DETTAGLIO (Tutto dentro il quadrato)
        idx = st.session_state.evento_aperto
        row = df.iloc[idx]
        
        st.markdown(f"""
        <div class='dettaglio-box'>
            <h3 style='color:#ff9100; font-size:1.2rem; margin-bottom:10px;'>{row['Nome Evento / Raduno']}</h3>
            <p style='font-size:0.9rem; margin-bottom:15px;'>📅 {row['Data']} | 📍 {row['Luogo']}</p>
        """, unsafe_allow_html=True)
        
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path): 
            st.image(img_path, use_container_width=True)
            
        if st.button("BACK"):
            st.session_state.evento_aperto = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error("Errore nel caricamento eventi.")
