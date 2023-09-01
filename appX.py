import streamlit as st              
import base64
import pickle
import streamlit_authenticator as stauth  
import utils as utl
import math

from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from PIL import Image
from pathlib import Path


# -------------- SETTINGS --------------

page_title = "Calcolo livello di compressione con metodo AISI"
page_icon = "🧮"  #:abacus:
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
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

# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller"] # abc / def
usernames = ["pparker", "rmiller"]
authentication_status = False

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "AISI compute", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Benvenuto {name}")
    # if st.sidebar.button("reset password", type="primary"):
    #     st.write('Premuto reset')
    
    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Sollecitazioni", "Visualizzazione"],
        icons=["pencil-fill", "calculator-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )
    # --- INPUT  ---
    # if selected == "Parametri iniziali":
    #     sApplicazione = st.selectbox('Applicazione', ('Stradale', 'Ferroviario', 'Guado'))
    #     sTipologiaDiStruttura = st.selectbox('Tipologia di Struttura', ('Circolare', 'Ellittica', 'Tre raggi di Curvatura'))
    #     sTipologiaDimateriale = st.selectbox('Tipologia di materiale (fy)', ('Acciaio S235JR', 'Acciaio S275JR'))  # resistenza del materiale in N/mm2
    #     sOndulazione = st.selectbox('Ondulazione',('T200','T100','T350'))
    #     sSpessoreLamiera = st.selectbox('Spessore Lamiera', ('4 mm', '3 mm', '6 mm'))
    #     
    #     st.write("sTipologiaDimateriale {0} ".format(sTipologiaDimateriale))
    #     st.write("tipo  {0} ".format(type(sTipologiaDimateriale)))

    if selected == "Sollecitazioni":
        st.header(f"Sollecitazioni")
        sTesto = """
        - Applicazioni stradali-autostradali in cui il ricoprimento minimo e 1/6 o 1/8 della luce della struttura (di norma
          si suggerisce di adottare a livello cautelativo e di prima approssimazione un cover minimo 1/6 della luce)
        - Applicazioni ferroviarie in cui il ricoprimento minimo adottato è pari a 1/4 la luce della struttura.
        """
        st.text(sTesto)
        
        with st.form("entry_form", clear_on_submit=True):
            col1, col2, col3  = st.columns(3)
            
            with col1:
                sApplicazione = st.selectbox('Applicazione', ('Stradale', 'Ferroviario', 'Guado'))
                sTipologiaDiStruttura = st.selectbox('Tipologia di Struttura', ('Circolare', 'Ellittica', 'Tre raggi di Curvatura'))
                sTipologiaDimateriale = st.selectbox('Tipologia di materiale (fy)', ('Acciaio S235JR', 'Acciaio S275JR'))  # resistenza del materiale in N/mm2
                sOndulazione = st.selectbox('Ondulazione',('T200','T100','T350'))
                sSpessoreLamiera = st.selectbox('Spessore Lamiera', ('4 mm', '3 mm', '6 mm'))
                
            with col2:
                nLuceMax = st.number_input('Luce massima (m)', value = 3.070, min_value=0.10, step=0.10, max_value=7.70)
                nRicoprimentoTerreno = st.number_input('Ricoprimento Terreno (m)',value=1.0)
                nRicoprimentoAsfaltoCLS = st.number_input('Ricoprimento Asfalto/CLS (m)',value=0.0)
                nDensitaTerreno = st.number_input('Densità terreno (N/m3)',value=2000)
                nDensitaAsfaltoCLS = st.number_input('Densità Asfalto/CLS (N/m3)',value=0.0)
                nCarichiVivi = st.number_input('Carichi Vivi (N/m2)',value=10000.0)
                # nRaggioGiratorio = st.number_input('Raggio Giratorio (mm)',value=0.0)
                nInerziaLineare = st.number_input('Inerzia Lineare (mm4/mm)',value=18192.0)
                nAreaLineare  = st.number_input('Area lineare (mm2)', value = 47)
            with col3:
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
                nPv = nK * (float(sDL) + nCarichiVivi)
                st.write("Pv = {0} N/m2".format( nPv))
                nCompressioneAnello = nPv * nLuceMax /2
                st.write("Compressione Anello {0} N".format(nCompressioneAnello))
                
                nRaggioGiratorio = math.sqrt(nInerziaLineare/nAreaLineare)
                st.write("Raggio Giratorio Anello {0} (mm)".format(nRaggioGiratorio))
                
                nRapportoRigidezza = nLuceMax * 1000 / nRaggioGiratorio 
                st.write("nRapportoRigidezza = {0} kN/m".format( nRapportoRigidezza) )
                
                # determinazione D/r
                if sTipologiaDimateriale == 'Acciaio S235JR':
                    nFattoreAumentoTest = 0
                    nVal235 = 235
                    if nRapportoRigidezza < 294:
                        nResistenza = nVal235
                    if nRapportoRigidezza >= 294 and nRapportoRigidezza <= 500:
                        nResistenza = 279.6 *- (574.3 / 1000000) * nRapportoRigidezza * nRapportoRigidezza
                    if nRapportoRigidezza > 500:
                        nResistenza = 34 * 1000000 / (nRapportoRigidezza * nRapportoRigidezza)
                
                st.write("Resistenza {0} N/mm2".format(nResistenza))
                
                nAreaSezione = nCompressioneAnello / nResistenza
                st.write("Area Sezione {0} mm2".format(nAreaSezione))
                
                if sTipologiaDimateriale == 'Acciaio S275JR':
                    nFattoreAumentoTest = 40
                    nVal235 = 275
                   
                nCarichiMorti = nRicoprimentoTerreno * nDensitaTerreno + nRicoprimentoAsfaltoCLS * nDensitaAsfaltoCLS
                st.write("Carichi morti = {0} kN/m".format( nCarichiMorti) )
                st.write("Compressione Anello = {0} kN/m".format( nCompressioneAnello) )

                if nAreaSezione / nAreaLineare > 1:
                    st.success('Struttura verificata', icon="✅")
                    st.snow()
                else:
                     st.warning('Struttura NON verificata', icon="⚠️")
                     
                st.write("Resistenza {0} N/mm2".format(nAreaSezione / nAreaLineare))

    # --- Visualizzazione dati ---
    if selected == "Visualizzazione":
        st.header("Documentazione teoria")
        # st.markdown("<embed src="strutture autoportanti in acciaio corrugato.pdf" width="400" height="400">", unsafe_allow_html=True)
        pdf2view = "strutture autoportanti in acciaio corrugato.pdf"
        with open(pdf2view,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = "<embed src=”data:application/pdf;base64,{base64_pdf}” width=”700″ height=”1000″ type=”application/pdf”>"
            
        st.markdown(pdf_display, unsafe_allow_html=True)
 