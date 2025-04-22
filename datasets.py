import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# Definição de escopos
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Autenticação com as credenciais do Streamlit
service_account_info = dict(st.secrets["gcp_service_account"])
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

# Abertura da planilha
planilha_completa = client.open(
    title="Dashboard 2025",
    folder_id="1E6lnp2Q5eFOfzbbq56Sff4DlQnWA66D1"
)

# Carregando os dados das abas
tarefas = pd.DataFrame(planilha_completa.get_worksheet(1).get_all_records())
negocios_relacionamento = pd.DataFrame(planilha_completa.get_worksheet(3).get_all_records())
negocios_processos = pd.DataFrame(planilha_completa.get_worksheet(4).get_all_records())
financeiro = pd.DataFrame(planilha_completa.get_worksheet(2).get_all_records())

# --- FORMATAÇÃO ---

# Limpeza dos nomes das colunas
financeiro.columns = financeiro.columns.str.strip()

# Conversão de data e oxigênio
financeiro['Data'] = pd.to_datetime(financeiro['Data'], format='%d/%m/%Y')
financeiro['Oxigênio Meses'] = financeiro['Oxigênio Meses'].astype(str).apply(
    lambda x: float(x.replace('.', '').replace(',', '.')))

# Função de conversão de moeda
def converter_moeda(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        if valor == '' or valor == 'nan':
            return 0.0
        return float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
    elif pd.isna(valor):
        return 0.0
    return valor

# Filtro com base nas receitas
filtro = financeiro[financeiro['Receitas'].notna() & (financeiro['Receitas'] != '')]
filtro.columns = filtro.columns.str.strip()
filtro = filtro.sort_values(by='Data', ascending=False)

# Conversão das colunas monetárias
colunas_monetarias = ['Receitas', 'Despesas', 'Média Despesas 12 meses', 'Caixa', 'Investimento Itaú', 'Conta Itaú']
for coluna in colunas_monetarias:
    if coluna in filtro.columns:
        filtro[coluna] = filtro[coluna].apply(converter_moeda)
    else:
        print(f"[AVISO] Coluna '{coluna}' não encontrada em 'filtro'.")

# Datas nos dados de negócios
negocios_relacionamento.columns = negocios_relacionamento.columns.str.strip()
negocios_relacionamento['Data'] = pd.to_datetime(negocios_relacionamento['Data'], format='%d/%m/%Y')
negocios_relacionamento = negocios_relacionamento.sort_values(by='Data', ascending=False)

negocios_processos.columns = negocios_processos.columns.str.strip()
negocios_processos['Data'] = pd.to_datetime(negocios_processos['Data'], format='%d/%m/%Y')
negocios_processos = negocios_processos.sort_values(by='Data', ascending=False)

# Conversão de data nas tarefas
tarefas.columns = tarefas.columns.str.strip()
tarefas['Data'] = pd.to_datetime(tarefas['Data'], format='%d/%m/%Y')
