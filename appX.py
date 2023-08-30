import streamlit as st              # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

# -------------- SETTINGS --------------

page_title = "Calcolo livello di compressione con metodo AISI"
page_icon = ":abacus:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Dati di calcolo", "Visualizzazione"],
    icons=["pencil-fill", "calculator-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT  ---
if selected == "Dati di calcolo":
    st.header(f"Inserimento dati")
    sTesto = """
    - Applicazioni stradali-autostradali in cui il ricoprimento minimo e 1/6 o 1/8 della luce della struttura (di norma
      si suggerisce di adottare a livello cautelativo e di prima approssimazione un cover minimo 1/6 della luce)
    - Applicazioni ferroviarie in cui il ricoprimento minimo adottato è pari a 1/4 la luce della struttura.
    """
    st.text(sTesto)
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nLuceMax = st.number_input('Luce massima (m)', value = 0.10, min_value=0.10, step=0.10, max_value=7.70)
            sDL = st.selectbox('% compattazione', ('85', '90', '95'))
             
        with col2:
            nLL = st.number_input('Live Load',value=0.0)

        submitted = st.form_submit_button("Conferma dati")
        if submitted:
            nk = 1
            if sDL == '85':
                nK = 0.86
            if sDL == '90':
                nK = 0.75
            if sDL == '90':
                nK = 0.65   

            st.success("Dati salvati")
            nPv = nK * (float(sDL) + nLL)
            st.write(nk)
            st.write(nPv)


# --- Visualizzazione dati ---
if selected == "Visualizzazione":
    st.header("Visualizzazione Dati")
    with st.form("Display_data"):
        submitted = st.form_submit_button("Display")
        if submitted:
            st.success("Dati visualizzati")