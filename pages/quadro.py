from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
from dash import dash_table

layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.H3("Atividades em Execução", className="text-center mb-4")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='quadro_table', className="dbc"),
            ])
        ])
    ], id="quadro")


# ====== Callbacks ======= #

@app.callback(
    Output('quadro_table', 'children'),
    [Input('store_atividade', 'data')]
)
def table(data):
    if data is None:
        return html.Div()  # Retorna um div vazio caso não haja dados

    df = pd.DataFrame(data)

    # Filtrando o DataFrame para incluir apenas atividades com manutenção não concluída (valor 0)
    df_filtrado = df[df['Manutenção Concluida'] == 0]

    # Aplicando a condição adicional para excluir atividades com 'Estagio' igual a "Em Espera"
    df_filtrado = df_filtrado[df_filtrado['Estagio'] != "Em Espera"]

    df_filtrado = df_filtrado.fillna('-')  # Substitui valores NaN por '-'

    # Removendo as colunas 'Manutenção Concluida' e 'Término'
    df_filtrado = df_filtrado.drop(columns=['Manutenção Concluida', 'Termino'])
    if df_filtrado.empty:
        return html.Div("Não há atividades em andamento.")  # Pode ajustar a mensagem conforme necessário


    return [dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in df_filtrado.columns],
        data=df_filtrado.to_dict('records'),  # Adiciona os dados filtrados à DataTable

        # Estilos e Configurações
        style_table={
            'overflowX': 'auto',
            'minWidth': '100%',
        },
        style_header={
            'backgroundColor': 'red',
            'color': 'white',
            'fontWeight': 'bold',
            'border': '1px solid black',
        },
        style_cell={
            'textAlign': 'left',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#FFD3D3',
                'color': 'black',
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#FFA6A6',
                'color': 'black',
            },
        ],
    )]

