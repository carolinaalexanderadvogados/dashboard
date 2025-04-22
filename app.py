import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import plotly.graph_objects as go
import plotly.express as px
from datasets import filtro, tarefas, negocios_processos

from financeiro import mostrar_financeiro
from tarefas import mostrar_tarefas
from negocios import mostrar_negocios

# Configurações da página
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

authentication_status = authenticator.login(location='main')

# Se login for bem-sucedido
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    def cabecalho(logo_path, titulo):
        col_logo, col_titulo = st.columns([1, 5])
        with col_logo:
            logo = Image.open(logo_path)
            st.image(logo, width=250)

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
        Dados = {
            'Nome': [
                "Alexander Santana", "Alice Rocha", "André Corá", "Carolina Takeda",
                "Henrique Choinski", "Isabele Martins", "Julia Bittencourt",
                "Luiz Carrano", "Marco Santana", "Paula Uriarte",
                "Pedro Silveira", "Schiefler Advocacia"
            ],
            'Apelido': [
                "Alexander", "Alice", "André", "Carolina", "Henrique",
                "Isabele", "Julia", "Carrano", "Marco", "Paula",
                "Pedro", "Schiefler"
            ],
            "Cargo": [
                "Advogado", " Financeiro e suporte na análise de dados.", "Estagiário", "Estagiário", "Advogado",
                "Secretária executivo", "Estagiário", "Advogado", "Advogado", "Secretária executivo",
                "Advogado", "Parceiro"
            ]
        }
        df_cargos = pd.DataFrame(Dados)
        advogados = df_cargos[df_cargos["Cargo"].str.strip() == "Advogado"]["Nome"]
        
        st.subheader("Visão Geral")
        with st.container():
            st.subheader('Processos')
            data = tarefas["Data"].max()
            tarefas_hoje = tarefas[tarefas['Data'] == data]
            tarefas_advogados = tarefas_hoje[tarefas_hoje["Nome"].isin(advogados)]

            row1 = st.columns(3)
            row2 = st.columns(3)
            
            with row1[0]:
                st.metric("Vencido", value=tarefas_hoje['Vencido'].sum(), border=True)
            with row1[1]:
                st.metric("Hoje", value=tarefas_hoje['Hoje'].sum(), border=True)
            with row1[2]:
                st.metric("Amanhã", value=tarefas_hoje['Amanhã'].sum(), border=True)
            with row2[0]:
                st.metric("Esta Semana", value=tarefas_hoje['Esta semana'].sum(), border=True)
            with row2[1]:
                st.metric("Próxima Semana", value=tarefas_hoje['Próxima semana'].sum(), border=True)
            with row2[2]:
                st.metric("Longe", value=tarefas_hoje['Longe'].sum(), border=True)
            
            st.table(tarefas_advogados[['Nome', 'Vencido', 'Hoje']].sort_values(by='Vencido', ascending=False))

            # Negócios por Etapa
            colunas = ['1. Ajuizamento', '2. Primeiro Grau', '3. Segundo Grau', '4. Outras Instâncias', '5. Cumprimento', '6. Pagamento']
            linha_mais_recente = negocios_processos[negocios_processos['Data'] == negocios_processos['Data'].max()]
            valores = linha_mais_recente[colunas].iloc[0]

            # Montando DataFrame para o gráfico
            df_etapas = pd.DataFrame({
                'Etapa': colunas,
                'Quantidade': valores.values
            })

            # Gráfico de barras interativo
            fig_neg_proc = px.bar(
                df_etapas,
                x='Etapa',
                y='Quantidade',
                color='Etapa',
                title=f"Negócios por Etapa - {linha_mais_recente['Data'].dt.strftime('%d/%m/%Y').values[0]}",
                color_discrete_sequence=['#C6244B', '#222B32', '#FF692D', '#C49451', '#888888', '#1F77B4']
            )

            fig_neg_proc.update_layout(
                xaxis_title="Etapas",
                yaxis_title="Quantidade",
                xaxis_tickangle=-45
            )

            # Exibindo gráfico
            st.plotly_chart(fig_neg_proc, use_container_width=True)

        with st.container():
            # Indicador de Oxigênio
            data_mais_recente = filtro['Data'].values[0]
            data_mais_recente = pd.to_datetime(data_mais_recente)
            oxigenio_objetivo = 24
            oxigenio_atual = (filtro.loc[filtro['Data'] == data_mais_recente, 'Oxigênio Meses'].values[0])/100 if not filtro.empty else 0
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=oxigenio_atual,
                title={"text": "Oxigênio em Meses"},
                gauge={
                    "axis": {"range": [0, oxigenio_objetivo]},
                    "bar": {"color": "#fcfaf7"},
                    "steps": [
                        {"range": [0, 8], "color": "#ff6464"},
                        {"range": [8, 16], "color": "#ffe162"},
                        {"range": [16, oxigenio_objetivo], "color": "#91c483"}
                    ]
                }
            ))

            fig = fig.update_layout(
                paper_bgcolor="#ffffff",
                font={"color": "black", "family": "Arial"},
            )

            st.plotly_chart(fig, use_container_width=True)

    elif pagina == "Financeiro":
        mostrar_financeiro()

    elif pagina == "Negócios":
        mostrar_negocios()

    elif pagina == "Tarefas Detalhado":
        mostrar_tarefas()

elif st.session_state["authentication_status"] == False:
    st.error('Usuário ou senha incorretos')
elif st.session_state["authentication_status"] == None:
    st.warning('Por favor, insira seu nome de usuário e senha')
