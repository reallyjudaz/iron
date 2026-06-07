# --- MENU FISSO (Versione Semplificata e Stabile) ---
st.markdown("""
<style>
    .menu-fisso {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1f2124;
        border-top: 3px solid #ff9100;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        padding: 15px 0;
        z-index: 999999;
    }
    .menu-item {
        color: #ff9100 !important;
        font-family: 'Special Elite', cursive;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
    }
</style>

<div class="menu-fisso">
    <div class="menu-item">HOME</div>
    <div class="menu-item">MC</div>
    <div class="menu-item">ADMIN</div>
</div>
""", unsafe_allow_html=True)
