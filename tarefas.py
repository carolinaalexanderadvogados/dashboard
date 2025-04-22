import streamlit as st
import pandas as pd
import plotly.express as px
from datasets import tarefas

def mostrar_tarefas():

    COR_VERMELHO = "#C6244B"
    COR_AZUL = "#222B32"
    COR_LARANJA = "#FF692D"
    COR_DOURADO = "#C49451"


    Dados = {
        'Nomes': [
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

    df_dados = pd.DataFrame(Dados)
    nomes_disponiveis = df_dados["Nomes"]
    pessoa_selecionada = st.selectbox("Selecione uma pessoa:", nomes_disponiveis)

    
    cargo_pessoa = df_dados[df_dados["Nomes"] == pessoa_selecionada]["Cargo"].values[0]
    apelido_pessoa_selecionada = df_dados[df_dados["Nomes"] == pessoa_selecionada]["Apelido"].values[0]
    data = tarefas["Data"].max()
    tarefas_hoje = tarefas[tarefas['Data'] == data]
    tarefas_hoje_pessoa = tarefas_hoje[tarefas_hoje['Nome'] == pessoa_selecionada]
    tarefas_pessoa = tarefas[tarefas['Nome'] == pessoa_selecionada]

    
    col1, col2 = st.columns([1, 2])

    
    with col1:
        st.image("fotos/" + apelido_pessoa_selecionada + ".jpg", width=150)
        st.subheader(pessoa_selecionada)
        st.write(f"**Função:** {cargo_pessoa}")

    
    with col2:
        st.subheader("Resumo das Tarefas")
        st.metric(label="Data", value=data.strftime("%d/%m/%Y"))

        if cargo_pessoa == "Advogado":
            st.subheader("Prazo processual")

            row1, row2 = st.columns(3), st.columns(3)
            with row1[0]:
                st.metric("Vencido", tarefas_hoje_pessoa['Vencido'].sum(), border=True)
            with row1[1]:
                st.metric("Hoje", tarefas_hoje_pessoa['Hoje'].sum(), border=True)
            with row1[2]:
                st.metric("Amanhã", tarefas_hoje_pessoa['Amanhã'].sum(), border=True)

            with row2[0]:
                st.metric("Esta Semana", tarefas_hoje_pessoa['Esta semana'].sum(), border=True)
            with row2[1]:
                st.metric("Próxima Semana", tarefas_hoje_pessoa['Próxima semana'].sum(), border=True)
            with row2[2]:
                st.metric("Longe", tarefas_hoje_pessoa['Longe'].sum(), border=True)
            st.subheader("Tarefas")

            row3, row4 = st.columns(3), st.columns(3)

            with row3[0]:
                st.metric("Sprint", tarefas_hoje_pessoa['Sprint'].sum(), border=True)
            with row3[1]:
                st.metric("Pendência", tarefas_hoje_pessoa['Pendência'].sum(), border=True)
            with row3[2]:
                st.metric("Reunião", tarefas_hoje_pessoa['Reunião'].sum(), border=True)

            with row4[0]:
                st.metric("Responder", tarefas_hoje_pessoa['Responder'].sum(), border=True)
            with row4[1]:
                st.metric("Organizar", tarefas_hoje_pessoa['Organizar'].sum(), border=True)
            with row4[2]:
                st.metric("Monitorar", tarefas_hoje_pessoa['Monitorar'].sum(), border=True)

            fig_prazo = px.line(
            tarefas[tarefas["Nome"]==pessoa_selecionada],
            x="Data",
            y="Prazo Processual",
            markers=False,
            title="Evolução Prazo Processual"
            )

            fig_prazo.update_traces(line=dict(color=COR_VERMELHO))

            # Customizar layout do gráfico
            fig_prazo.update_layout(
                xaxis_title="Data",
                yaxis_title="Valor",
                hovermode="x unified",
                template="plotly_dark"
            )

            st.plotly_chart(fig_prazo)
            tarefas_agrupadas = tarefas_hoje_pessoa[["Sprint", "Pendência", "Reunião", "Responder", "Organizar", "Monitorar"]].sum()
            fig_pizza = px.pie(tarefas_hoje_pessoa, values=tarefas_agrupadas.values, names=tarefas_agrupadas.index, title="Tipos de Tarefas" )
            st.plotly_chart(fig_pizza)

            opcoes = ["Sprint", "Pendência", "Reunião", "Responder", "Organizar", "Monitorar"]
            coluna_selecionada_adv = st.selectbox("Selecione a métrica:", opcoes)
            fig_adv_tarefas = px.line(
            tarefas_pessoa.sort_values(by='Data', ascending=True),
            x="Data",
            y=coluna_selecionada_adv,
            markers=True,
            title=f"Evolução de {coluna_selecionada_adv}"
    )
            fig_adv_tarefas.update_traces(line=dict(color=COR_LARANJA))

    

    # Customizar layout do gráfico
            fig_adv_tarefas.update_layout(
                xaxis_title="Data",
                yaxis_title="Quantidade",
                hovermode="x unified",
                template="plotly_dark"
            )

            # Mostrar gráfico
            st.plotly_chart(fig_adv_tarefas)

        elif cargo_pessoa == "Parceiro":
            row1, row2 = st.columns(3), st.columns(3)
            with row1[0]:
                st.metric("Vencido", tarefas_hoje_pessoa['Vencido'].sum(), border=True)
            with row1[1]:
                st.metric("Hoje", tarefas_hoje_pessoa['Hoje'].sum(), border=True)
            with row1[2]:
                st.metric("Amanhã", tarefas_hoje_pessoa['Amanhã'].sum(), border=True)

            with row2[0]:
                st.metric("Esta Semana", tarefas_hoje_pessoa['Esta semana'].sum(), border=True)
            with row2[1]:
                st.metric("Próxima Semana", tarefas_hoje_pessoa['Próxima semana'].sum(), border=True)
            with row2[2]:
                st.metric("Longe", tarefas_hoje_pessoa['Longe'].sum(), border=True)
            st.subheader("Tarefas")

            fig_prazo = px.line(
            tarefas[tarefas["Nome"]==pessoa_selecionada],
            x="Data",
            y="Prazo Processual",
            markers=False,
            title="Evolução Prazo Processual"
            )

            fig_prazo.update_traces(line=dict(color=COR_VERMELHO))

            st.plotly_chart(fig_prazo)


        else:   



            st.subheader("Tarefas")

            row3, row4 = st.columns(3), st.columns(3)

            with row3[0]:
                st.metric("Sprint", tarefas_hoje_pessoa['Sprint'].sum(), border=True)
            with row3[1]:
                st.metric("Pendência", tarefas_hoje_pessoa['Pendência'].sum(), border=True)
            with row3[2]:
                st.metric("Reunião", tarefas_hoje_pessoa['Reunião'].sum(), border=True)

            with row4[0]:
                st.metric("Responder", tarefas_hoje_pessoa['Responder'].sum(), border=True)
            with row4[1]:
                st.metric("Organizar", tarefas_hoje_pessoa['Organizar'].sum(), border=True)
            with row4[2]:
                st.metric("Monitorar", tarefas_hoje_pessoa['Monitorar'].sum(), border=True)

            tarefas_agrupadas = tarefas_hoje_pessoa[["Sprint", "Pendência", "Reunião", "Responder", "Organizar", "Monitorar"]].sum()
            fig_pizza = px.pie(values=tarefas_agrupadas.values, names=tarefas_agrupadas.index, title="Tipos de Tarefas")
            st.plotly_chart(fig_pizza)

           

            opcoes = ["Sprint", "Pendência", "Reunião", "Responder", "Organizar", "Monitorar"]
            coluna_selecionada_func = st.selectbox("Selecione a métrica:", opcoes)
            fig_func_tarefas = px.line(
            tarefas_pessoa.sort_values(by='Data', ascending=True),
            x="Data",
            y=coluna_selecionada_func,
            markers=True,
            title=f"Evolução de {coluna_selecionada_func}"
    )
            fig_func_tarefas.update_traces(line=dict(color=COR_LARANJA))

    

    # Customizar layout do gráfico
            fig_func_tarefas.update_layout(
                xaxis_title="Data",
                yaxis_title="Quantidade",
                hovermode="x unified",
                template="plotly_dark"
            )

            # Mostrar gráfico
            st.plotly_chart(fig_func_tarefas)
