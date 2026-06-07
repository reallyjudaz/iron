import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Iron & Rubber", layout="centered")

# --- FUNZIONI ---
def registra_voto(id_evento):
    with open("voti_fatti.txt", "a") as f:
        f.write(f"{id_evento}\n")

def ha_gia_votato(id_evento):
    if not os.path.exists("voti_fatti.txt"): return False
    with open("voti_fatti.txt", "r") as f:
        return str(id_evento) in f.read().splitlines()

# --- GESTIONE SESSIONE ADMIN ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# --- CSS (Stile pulito) ---
st.markdown("""
<style>
.stApp { background-color: #161719; }
.titolo-gotico { font-family: 'serif'; text-align: center; color: #ff9100; font-size: 2.6rem; }
</style>
""", unsafe_allow_html=True)

# --- MENU LATERALE (Sidebar: Il posto più sicuro) ---
with st.sidebar:
    st.markdown("## MENU")
    if st.button("🏠 HOME"): st.rerun()
    st.button("🏍️ MC")
    st.divider()
    
    # Login Admin nella sidebar
    if not st.session_state.admin_logged_in:
        if st.button("🔑 LOGIN ADMIN"):
            st.session_state.show_login = True
        if st.session_state.get("show_login", False):
            pwd = st.text_input("Password", type="password")
            if pwd == "Judaz2026":
                st.session_state.admin_logged_in = True
                st.rerun()
    else:
        st.success("Admin attivo")
        if st.button("🚪 LOGOUT ADMIN"):
            st.session_state.admin_logged_in = False
            st.rerun()

# --- PAGINA PRINCIPALE ---
if os.path.exists("logo_custom.png"):
    st.image("logo_custom.png", use_container_width=True)

st.markdown("<h1 class='titolo-gotico'>Iron & Rubber</h1>", unsafe_allow_html=True)

# --- LISTA EVENTI ---
try:
    df = pd.read_excel("Lista_Eventi_Bikers_Judaz.xlsx")
    df.columns = df.columns.str.strip()

    for i, row in df.iterrows():
        with st.expander(f"{row['Data']} - {row['Nome Evento / Raduno']}"):
            st.write(f"📍 {row['Luogo']}")
            
            if st.session_state.admin_logged_in:
                if st.button(f"🗑️ ELIMINA", key=f"del_{i}"):
                    df = df.drop(i)
                    df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
                    st.rerun()

        conteggio = int(row.get('Partecipanti', 0))
        if st.button(f"CI VADO 🔥 {conteggio}", key=f"btn_{i}", disabled=ha_gia_votato(i)):
            df.at[i, 'Partecipanti'] = conteggio + 1
            df.to_excel("Lista_Eventi_Bikers_Judaz.xlsx", index=False)
            registra_voto(i)
            st.rerun()

except Exception:
    st.error("Errore file.")
