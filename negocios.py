import streamlit as st
import pandas as pd
from datasets import negocios_relacionamento, negocios_processos, filtro
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from utils import format_number

def mostrar_negocios():

    COR_VERMELHO = "#C6244B"
    COR_AZUL = "#222B32"
    COR_LARANJA = "#FF692D"
    COR_DOURADO = "#C49451"


    st.subheader("Negócios Processos")
    col1,col2,col3,col4,col5,col6 = st.columns(6)

    ajuizamento_atual = int(negocios_processos['1. Ajuizamento'].values[0])
    ajuizamento_anterior = int(negocios_processos['1. Ajuizamento'].values[1])

    pgrau_atual = int(negocios_processos['2. Primeiro Grau'].values[0])
    pgrau_anterior = int(negocios_processos['2. Primeiro Grau'].values[1])

    sgrau_atual = int(negocios_processos['3. Segundo Grau'].values[0])
    sgrau_anterior = int(negocios_processos['3. Segundo Grau'].values[1])

    outras_inst_atual = int(negocios_processos['4. Outras Instâncias'].values[0])
    outras_inst_anterior = int(negocios_processos['4. Outras Instâncias'].values[1])

    cumprimento_atual = int(negocios_processos['5. Cumprimento'].values[0])
    cumprimento_anterior = int(negocios_processos['5. Cumprimento'].values[1])

    pgto_atual = int(negocios_processos['6. Pagamento'].values[0])
    pgto_anterior = int(negocios_processos['6. Pagamento'].values[1])



    with col1: 
        ajuizamento_delta = ajuizamento_atual - ajuizamento_anterior
        st.metric(label ="Ajuizamento", value = ajuizamento_atual, delta = ajuizamento_delta, border=True)
    with col2: 
        pgrau_delta = pgrau_atual - pgrau_anterior
        st.metric(label ="Primeiro Grau", value = pgrau_atual, delta =  pgrau_delta, border=True)
    with col3: 
        sgrau_delta = sgrau_atual - sgrau_anterior
        st.metric(label ="Segundo Grau", value = sgrau_atual, delta =  sgrau_delta, border=True)
    with col4: 
        outras_inst_delta = outras_inst_atual - outras_inst_anterior 
        st.metric(label ="Outras Instâncias", value = outras_inst_atual, delta =  outras_inst_delta, border=True)
    with col5: 
        cumprimento_delta = cumprimento_atual - cumprimento_anterior
        st.metric(label ="Cumprimento", value =  cumprimento_atual, delta =  cumprimento_delta, border=True)    
    with col6: 
        pgto_delta = pgto_atual-pgto_anterior 
        st.metric(label ="Pagamento", value = pgto_atual, delta =  pgto_delta, border=True)


    st.subheader("Evolução dos Processos ao Longo do Tempo")

    # Criar menu deslizante para escolher a métrica
    opcoes = negocios_processos.columns[1:]  # Excluir a coluna de Data
    coluna_selecionada = st.selectbox("Selecione a métrica:", opcoes)

    # Criar gráfico de evolução
    fig = px.line(negocios_processos.sort_values(by='Data', ascending=True), x="Data", y=coluna_selecionada, markers=True, title=f"Evolução de {coluna_selecionada}")

    fig.update_traces(line=dict(color=COR_VERMELHO))

    # Customizar layout
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Quantidade",
        hovermode="x unified",
        template="plotly_dark"
    )

    # Mostrar gráfico
    st.plotly_chart(fig)

    st.subheader("Negócios Relacionamento")

    # Criar colunas para métricas
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Definir variáveis para valores atuais e anteriores
    contato_atual = int(negocios_relacionamento['1. Contato'].values[0])
    contato_anterior = int(negocios_relacionamento['1. Contato'].values[1])

    coletar_docs_atual = int(negocios_relacionamento['2. Coletar DOCs'].values[0])
    coletar_docs_anterior = int(negocios_relacionamento['2. Coletar DOCs'].values[1])

    viabilidade_atual = int(negocios_relacionamento['3. Viabilidade'].values[0])
    viabilidade_anterior = int(negocios_relacionamento['3. Viabilidade'].values[1])

    contratacao_atual = int(negocios_relacionamento['4. Contratação'].values[0])
    contratacao_anterior = int(negocios_relacionamento['4. Contratação'].values[1])

    implementacao_atual = int(negocios_relacionamento['5. Implementação'].values[0])
    implementacao_anterior = int(negocios_relacionamento['5. Implementação'].values[1])

    encerramento_atual = int(negocios_relacionamento['6. Encerramento'].values[0])
    encerramento_anterior = int(negocios_relacionamento['6. Encerramento'].values[1])

    # Exibir métricas
    with col1:
        contato_delta = contato_atual - contato_anterior
        st.metric(label="Contato", value=contato_atual, delta=contato_delta, border=True)

    with col2:
        coletar_docs_delta = coletar_docs_atual - coletar_docs_anterior
        st.metric(label="Coletar DOCs", value=coletar_docs_atual, delta=coletar_docs_delta, border=True)

    with col3:
        viabilidade_delta = viabilidade_atual - viabilidade_anterior
        st.metric(label="Viabilidade", value=viabilidade_atual, delta=viabilidade_delta, border=True)

    with col4:
        contratacao_delta = contratacao_atual - contratacao_anterior
        st.metric(label="Contratação", value=contratacao_atual, delta=contratacao_delta, border=True)

    with col5:
        implementacao_delta = implementacao_atual - implementacao_anterior
        st.metric(label="Implementação", value=implementacao_atual, delta=implementacao_delta, border=True)

    with col6:
        encerramento_delta = encerramento_atual - encerramento_anterior
        st.metric(label="Encerramento", value=encerramento_atual, delta=encerramento_delta, border=True)

    # Gráfico de evolução do relacionamento
    st.subheader("Evolução do Relacionamento ao Longo do Tempo")

    # Criar menu deslizante para escolher a métrica
    opcoes_relacionamento = negocios_relacionamento.columns[1:]  # Excluir a coluna de Data
    coluna_selecionada_relacionamento = st.selectbox("Selecione a métrica do relacionamento:", opcoes_relacionamento)

    # Criar gráfico de evolução para negócios_relacionamento
    fig_relacionamento = px.line(
        negocios_relacionamento.sort_values(by='Data', ascending=True),
        x="Data",
        y=coluna_selecionada_relacionamento,
        markers=True,
        title=f"Evolução de {coluna_selecionada_relacionamento}"
    )

    fig_relacionamento.update_traces(line=dict(color=COR_LARANJA))

    

    # Customizar layout do gráfico
    fig_relacionamento.update_layout(
        xaxis_title="Data",
        yaxis_title="Quantidade",
        hovermode="x unified",
        template="plotly_dark"
    )

    # Mostrar gráfico
    st.plotly_chart(fig_relacionamento)
