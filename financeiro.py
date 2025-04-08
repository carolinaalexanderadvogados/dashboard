import streamlit as st
import pandas as pd
from datasets import financeiro, filtro
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from utils import format_number

def mostrar_financeiro():

    COR_VERMELHO = "#C6244B"
    COR_AZUL = "#222B32"
    COR_LARANJA = "#FF692D"
    COR_DOURADO = "#C49451"



    col2, col3, col4 = st.columns(3)

    data_mais_recente = filtro['Data'].values[0]
    data_mais_recente = pd.to_datetime(data_mais_recente) 

    receita_atual = filtro['Receitas'].values[0]
    receita_anterior = filtro['Receitas'].values[1]

    despesa_atual = filtro['Despesas'].values[0]
    despesa_anterior = filtro['Despesas'].values[1]

    caixa_atual = filtro['Caixa'].values[0]
    caixa_anterior = filtro['Caixa'].values[1]

    data_mais_recente_str = data_mais_recente.strftime('%d/%m/%Y')


    with col2: 
        receita_mais_recente = format_number(receita_atual, "R$")
        receita_delta = receita_atual - receita_anterior 
        receita_delta_porcent = (receita_delta / receita_atual) * 100 if receita_atual != 0 else 0
        delta_formatado = f"{receita_delta_porcent:.2f}%"
        st.metric(label="Receita", value=receita_mais_recente, delta=delta_formatado, border=True)
    with col3: 
        despesa_mais_recente = format_number(despesa_atual, "R$")
        despesa_delta = despesa_atual - despesa_anterior
        despesa_delta_porcent = (despesa_delta / despesa_atual) * 100 if despesa_atual != 0 else 0
        despesa_formatada = f"{despesa_delta_porcent:.2f}%"
        st.metric(label="Despesas", value=despesa_mais_recente, delta=despesa_formatada, border=True)
    with col4: 
        caixa_mais_recente = format_number(caixa_atual, "R$")
        caixa_delta = caixa_atual - caixa_anterior 
        caixa_delta_porcent = (caixa_delta / caixa_atual) * 100 if caixa_atual != 0 else 0
        caixa_formatada = f"{caixa_delta_porcent:.2f}%"
        st.metric(label="Caixa", value=caixa_mais_recente, delta=caixa_formatada, border=True)

        oxigenio_objetivo = 24
        oxigenio_atual = filtro.loc[filtro['Data'] == data_mais_recente, 'Oxigênio Meses'].values[0] if not filtro.empty else 0

    graf1, graf2 = st.columns(2)

    with graf1: 
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=oxigenio_atual,
            title={"text": "Oxigênio em Meses"},
            gauge={
                "axis": {"range": [0, oxigenio_objetivo]},
                "bar": {"color": "#f7e1c1"},  # Cor da agulha
                "steps": [
                    {"range": [0, 6], "color": "#E63950"},  # Período crítico
                    {"range": [6, 12], "color": "#C6244B"},  # Período de atenção
                    {"range": [12, oxigenio_objetivo], "color":	"#920E30"}  # Situação confortável
                ]
            }
        ))

        fig = fig.update_layout(
        paper_bgcolor="#ffffff",
        font={"color": "white", "family": "Arial"},
        )

        st.plotly_chart(fig, use_container_width=True)
    with graf2: 
        fig_receitas = px.line(
            filtro.sort_values(by='Data', ascending=True),
            x="Data",
            y="Receitas",
            markers=True,
            title="Evolução Receita"
        )
        fig_receitas.update_traces(line=dict(color=COR_VERMELHO))

        # Customizar layout do gráfico
        fig_receitas.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor",
            hovermode="x unified",
            template="plotly_dark"
        )

        # Mostrar gráfico
        st.plotly_chart(fig_receitas)

    graf3, graf4 = st.columns(2)
    with graf3: 
        fig_despesas = px.line(
            filtro.sort_values(by='Data', ascending=True),
            x="Data",
            y="Despesas",
            markers=True,
            title="Evolução Despesas"
        )
        fig_despesas.update_traces(line=dict(color=COR_LARANJA))

        # Customizar layout do gráfico
        fig_despesas.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor",
            hovermode="x unified",
            template="plotly_dark"
        )

        # Mostrar gráfico
        st.plotly_chart(fig_despesas)
    with graf4: 
        fig_caixa = px.line(
            filtro.sort_values(by='Data', ascending=True),
            x="Data",
            y="Caixa",
            markers=True,
            title="Evolução Caixa"
        )
        fig_caixa.update_traces(line=dict(color=COR_DOURADO))

        # Customizar layout do gráfico
        fig_caixa.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor",
            hovermode="x unified",
            template="plotly_dark"
        )

        # Mostrar gráfico
        st.plotly_chart(fig_caixa)

    graf5, graf6 = st.columns(2) 

    with graf5: 
        fig_oxigenio = px.line(
            filtro.sort_values(by='Data', ascending=True),
            x="Data",
            y="Oxigênio Meses",
            markers=True,
            title="Evolução Oxigênio"
        )

        fig_oxigenio.update_traces(line=dict(color=COR_VERMELHO))

        # Customizar layout do gráfico
        fig_oxigenio.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor",
            hovermode="x unified",
            template="plotly_dark"
        )

        # Mostrar gráfico
        st.plotly_chart(fig_oxigenio)    

    

        


        



            

        

