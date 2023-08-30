import streamlit as st              
import base64

from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from PIL import Image

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
    options=["Parametri iniziali", "Sollecitazioni", "Visualizzazione"],
    icons=["pencil-fill", "calculator-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT  ---
if selected == "Parametri iniziali":
    sApplicazione = st.selectbox('Applicazione', ('Stradale', 'Ferroviario', 'Guado'))
    sTipologiaDiStruttura = st.selectbox('Tipologia di Struttura', ('Circolare', 'Ellittica', 'Tre raggi di Curvatura'))
    sTipologiaDimateriale = st.selectbox('Tipologia di materiale (fy)', ('Acciaio S235JR', 'Acciaio S275JR'))
    sOndulazione = st.selectbox('Ondulazione',('T100','T200','T350'))
    sSpessoreLamiera = st.selectbox('Spessore Lamiera', ('3 mm', '4 mm', '6 mm'))

if selected == "Sollecitazioni":
    st.header(f"Sollecitazioni")
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
            nLL = st.number_input('Live Load',value=0.0)
            nRicoprimentoTerreno = st.number_input('Ricoprimento Terreno (m)',value=0.0)
            nRicoprimentoAsfaltoCLS = st.number_input('Ricoprimento Asfalto/CLS (m)',value=0.0)
            nDensitaTerreno = st.number_input('Densità terreno (kN/m3)',value=0.0)
            nDensitaAsfaltoCLS = st.number_input('Densità Asfalto/CLS (kN/m3)',value=0.0)
             
        with col2:
            image = Image.open('fig2.png')
            st.image(image, caption='Diagramma dei fattori di riduzione legati alla Densità Proctor (DP)')
            sDL = st.selectbox('Compattazione terreno (%)', ('85', '90', '95'))
    
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
            
            nCarichiMorti = nRicoprimentoTerreno * nDensitaTerreno + nRicoprimentoAsfaltoCLS * nDensitaAsfaltoCLS
            st.write("Carichi morti {0} ".format( nCarichiMorti) )

# --- Visualizzazione dati ---
if selected == "Visualizzazione":
    st.header("Visualizzazione Dati")
    # st.markdown("<embed src="strutture autoportanti in acciaio corrugato.pdf" width="400" height="400">", unsafe_allow_html=True)
    pdf2view = "strutture autoportanti in acciaio corrugato.pdf"
    with open(pdf2view,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = "f'<embed src=”data:application/pdf;base64,{base64_pdf}” width=”700″ height=”1000″ type=”application/pdf”>’"
        
    st.markdown(pdf_display, unsafe_allow_html=True)