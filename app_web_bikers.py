import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- CSS (Mantiene il look della tua prima immagine) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
#MainMenu, header {visibility: hidden !important;}
.block-container { padding-bottom: 150px !important; }
.event-box { background-color: #1f2124; padding: 15px; margin-bottom: 15px; border: 2px solid #ff9100; border-radius: 10px; color: white; }
.dettaglio-box { background-color: #1f2124; padding: 20px; border: 3px solid #ff9100; border-radius: 15px; color: white; }
div[data-testid="stForm"] { border: none !important; background: transparent !important; }
</style>
""", unsafe_allow_html=True)

if 'dettaglio_id' not in st.session_state: st.session_state.dettaglio_id = None

try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()
except:
    df = pd.DataFrame()

if not df.empty:
    if st.session_state.dettaglio_id is None:
        # LISTA: Ogni box è un FORM (quindi cliccabile per intero)
        for i, row in df.iterrows():
            with st.form(key=f"form_{i}"):
                st.markdown(f"<div class='event-box'><h3>{row['Nome Evento / Raduno']}</h3><p>📅 {row['Data']} | 📍 {row['Luogo']}</p></div>", unsafe_allow_html=True)
                if st.form_submit_button("APRI EVENTO"):
                    st.session_state.dettaglio_id = i
                    st.rerun()
    else:
        # DETTAGLIO
        i = st.session_state.dettaglio_id
        row = df.iloc[i]
        st.markdown(f"<div class='dettaglio-box'>", unsafe_allow_html=True)
        st.subheader(row['Nome Evento / Raduno'])
        st.write(f"📅 **Data:** {row['Data']}")
        st.write(f"📍 **Luogo:** {row['Luogo']}")
        st.write(f"📝 **Note:** {row.get('Dettagli / Note', 'Nessuna nota.')}")
        
        img = str(row.get('Locandina', ''))
        if img and os.path.exists(img): st.image(img, use_container_width=True)
        
        if st.button("⬅ TORNA ALLA LISTA"):
            st.session_state.dettaglio_id = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- MENU FISSO (Posizionato in basso in modo assoluto) ---
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background: #1f2124; padding: 15px 0; border-top: 3px solid #ff9100; display: flex; justify-content: space-evenly; z-index: 9999;'>
    <b style='color:#ff9100;'>HOME</b><b style='color:#ff9100;'>MC</b><b style='color:#ff9100;'>ADMIN</b>
</div>
""", unsafe_allow_html=True)
