# --- INTERFACCIA ---
if not df.empty:
    if st.session_state.evento_aperto is None:
        # LISTA EVENTI
        for i, row in df.iterrows():
            nome = str(row.get('Nome Evento / Raduno', 'Evento'))
            conteggio = int(row.get('Partecipanti', 0))
            
            # Box cliccabile (usiamo un form per catturare il click su tutto il box)
            with st.form(key=f"form_{i}"):
                st.markdown(f"<div style='text-align:center;'><h3>{nome}</h3><p>{row['Data']} - {row['Luogo']}</p></div>", unsafe_allow_html=True)
                if st.form_submit_button("APRI DETTAGLI"):
                    st.session_state.evento_aperto = i
                    st.rerun()

            # Tasto Voto (fuori dal form)
            label = f"CI VADO 🔥 {conteggio}"
            if ha_gia_votato(i): st.button(label, key=f"btn_{i}", disabled=True)
            elif st.button(label, key=f"btn_{i}"):
                df.at[i, 'Partecipanti'] = conteggio + 1
                df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                registra_voto(i)
                st.rerun()
            st.markdown("---", unsafe_allow_html=True)
            
    else:
        # DETTAGLIO COMPLETO (Tutto nel box arancione)
        idx = st.session_state.evento_aperto
        row = df.iloc[idx]
        
        st.markdown("<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.subheader(row['Nome Evento / Raduno'])
        st.write(f"📅 **Data:** {row['Data']}")
        st.write(f"📍 **Luogo:** {row['Luogo']}")
        
        # DESCRIZIONE IN BIANCO DENTRO IL BOX
        st.markdown(f"<div style='color:white; margin: 15px 0;'><strong>Note:</strong><br>{row.get('Dettagli / Note', 'Nessuna nota.')}</div>", unsafe_allow_html=True)
        
        # LOCANDINA
        img_path = str(row.get('Locandina', ''))
        if img_path and os.path.exists(img_path): 
            st.image(img_path, use_container_width=True)
            
        if st.button("BACK"):
            st.session_state.evento_aperto = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
