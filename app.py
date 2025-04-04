import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader

from financeiro import mostrar_financeiro
from tarefas import mostrar_tarefas
from negocios import mostrar_negocios


st.set_page_config(page_title="Dashboard 2025", layout="wide")

# Carregando o arquivo de configuração
config = st.secrets['login']
# Autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authentication_status = authenticator.login(location = 'main')

# Se login for bem-sucedido
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    def cabecalho(logo_path, titulo):
        col_logo, col_titulo = st.columns([1, 5])
        with col_logo:
            logo = Image.open(logo_path)
            st.image(logo, width=300)
        with col_titulo:
            st.title(titulo)

    with st.sidebar:
        pagina = option_menu(
            menu_title="Menu",
            options=["Visão Geral", "Financeiro", "Negócios", "Tarefas Detalhado"],
            icons=["bi bi-house-door-fill", "bi bi-currency-dollar", "bar-chart", "bi bi-person-fill"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#222B32"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#C6244B", "font-weight": "bold"},
            }
        )

    cabecalho("arquivos/logo.jpg", "Dashboard 2025")

    if pagina == "Visão Geral":
        st.subheader("Visão Geral")

    elif pagina == "Financeiro":
        mostrar_financeiro()

    elif pagina == "Negócios":
        mostrar_negocios()

    elif pagina == "Tarefas Detalhado":
        mostrar_tarefas()

# Mensagens para login mal sucedido ou ainda não autenticado
elif st.session_state["authentication_status"] == False:
    st.error('Usuário ou senha incorretos')
elif st.session_state["authentication_status"] == None:
    st.warning('Por favor, insira seu nome de usuário e senha')
