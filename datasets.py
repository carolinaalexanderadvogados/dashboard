import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json



scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

service_account_info = dict(st.secrets["gcp_service_account"])
creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=scopes)

client = gspread.authorize(creds)

planilha_completa = client.open(
    title="Dashboard 2025", 
    folder_id="1E6lnp2Q5eFOfzbbq56Sff4DlQnWA66D1"
    )

tarefas = planilha_completa.get_worksheet(1)
tarefas = tarefas.get_all_records()
tarefas = pd.DataFrame(tarefas)

negocios_relacionamento  = planilha_completa.get_worksheet(3)
negocios_relacionamento  = negocios_relacionamento.get_all_records()
negocios_relacionamento  = pd.DataFrame(negocios_relacionamento )

negocios_processos  = planilha_completa.get_worksheet(4)
negocios_processos  = negocios_processos.get_all_records()
negocios_processos  = pd.DataFrame(negocios_processos)

financeiro = planilha_completa.get_worksheet(2)
financeiro  = financeiro.get_all_records()
financeiro = pd.DataFrame(financeiro)




#FORMATAÇÃO FINANCEIRO 

#formatação de data, e coluna de mês
financeiro['Data'] = pd.to_datetime(financeiro['Data'], format='%d/%m/%Y')
financeiro['Oxigênio Meses'] = financeiro['Oxigênio Meses'].astype(str).apply(lambda x: float(x.replace('.', '').replace(',', '.')))


# formatação de moeda para número 
def converter_moeda(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        if valor == '' or valor == 'nan':
            return 0.0  # ou use np.nan se quiser deixar como NaN
        return float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
    elif pd.isna(valor):
        return 0.0  # ou np.nan
    return valor

colunas_monetarias = ['Receitas', 'Despesas', 'Caixa', 'Investimento Itaú', 'Conta Itaú']


for coluna in colunas_monetarias:
    financeiro[coluna] = financeiro[coluna].apply(converter_moeda)

#filtro de data mais recente tal que Receitas é não vazio: 

filtro = financeiro[financeiro['Receitas'].notna() & (financeiro['Receitas'] != '')]
filtro = filtro.sort_values(by='Data', ascending=False)

#FORMATAÇÃO NEGÓCIOS 

negocios_relacionamento['Data'] = pd.to_datetime(negocios_relacionamento['Data'], format='%d/%m/%Y')
negocios_relacionamento = negocios_relacionamento.sort_values(by='Data', ascending=False)
negocios_processos['Data'] = pd.to_datetime(negocios_processos['Data'], format='%d/%m/%Y')
negocios_processos = negocios_processos.sort_values(by='Data', ascending=False)

tarefas['Data'] =pd.to_datetime(tarefas['Data'], format='%d/%m/%Y')