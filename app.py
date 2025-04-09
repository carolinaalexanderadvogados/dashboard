import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader

from financeiro import mostrar_financeiro, fig
from tarefas import mostrar_tarefas, tarefas_hoje
from negocios import mostrar_negocios


st.set_page_config(page_title="Dashboard 2025", layout="wide")

# Carregando o arquivo de configuração
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["passwords"]
cookie = st.secrets["cookie"]

credentials = {
    "usernames": {
        user: {"name": user.capitalize(), "password": passwords[user]}
        for user in usernames
    }
}
# Autenticação
authenticator = stauth.Authenticate(
    credentials,
    cookie["name"],
    cookie["key"],
    cookie["expiry_days"],
)


authentication_status = authenticator.login(location = 'main')

# Se login for bem-sucedido
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    def cabecalho(logo_path, titulo):
        col_logo, col_titulo = st.columns([1, 5])
    
        with col_logo:
            logo = Image.open(logo_path)
            st.image(logo, width=250)  # Ajuste o tamanho conforme necessário

        with col_titulo:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; height: 100%;">
                    <h1 style="margin: 0; padding-left: 10px;">{titulo}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

    with st.sidebar:
        pagina = option_menu(
            menu_title="Menu",
            options=["Visão Geral", "Financeiro", "Negócios", "Tarefas Detalhado"],
            icons=["bi bi-house-door-fill", "bi bi-currency-dollar", "bar-chart", "bi bi-person-fill"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#ffffff"},
                "icon": {"color": "black", "font-size": "18px"},
                "nav-link": {"color": "black", "font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#C49451", "font-weight": "bold"},
            }
        )

    cabecalho("arquivos/logo.jpg", "Dashboard 2025")

    if pagina == "Visão Geral":
        st.subheader("Visão Geral")
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.subheader('Processos')
            row1, row2 = st.columns(3), st.columns(3)
            with row1[0]:
                st.metric("Vencido", value=tarefas_hoje['Vencido'].sum(), border=True)
            with row1[1]:    
                st.metric("Hoje", value=tarefas_hoje['Hoje'].sum(), border=True)
            with row1[2]:    
                st.metric("Amanhã", value=tarefas_hoje['Amanhã'].sum(), border=True)
            with row2[0]:
                st.metric("Esta Semana", value=tarefas_hoje['Esta Semana'].sum(), border=True)
            with row2[1]:    
                st.metric("Próxima Semana", value=tarefas_hoje['Próxima Semana'].sum(), border=True)
            with row2[2]:    
                st.metric("Longe", value=tarefas_hoje['Longe'].sum(), border=True)
            st.table(tarefas_hoje.sort_values(by='Vencido', ascending=False))
 



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
