from dash import dcc, html, Input, Output
import pandas as pd
import sqlite3
from app import *
from pages import sidebar, home, quadro
from sql_beta import df_estagio, df_tecnico, df_atividade


# =========  Criar estrutura para Store intermediaria   =========== #
data_int = {
    'Pes': [],
    'Cliente': [],
    'Equipamento': [],
    'Tecnico': [],
    'Estagio': [],
    'Inicio': [],
    'Previsão de Término': [],
    'Termino': [],
    'Manutenção Concluida': [],
    'Observação': [],
    'disabled': []
}

store_int = pd.DataFrame(data_int)

# =========  Layout  =========== #

app.layout = dbc.Container([
    # Store e Location
    dcc.Location(id='url'),
    dcc.Store(id='store_intermedio', data=store_int.to_dict()),
    dcc.Store(id='store_tecnico', data=df_tecnico.to_dict()),
    dcc.Store(id='store_estagio', data=df_estagio.to_dict()),
    dcc.Store(id='store_atividade', data=df_atividade.to_dict()),
    html.Div(id='div_fantasma'),

    # Layout
    dbc.Row([
        dbc.Col([
            sidebar.layout
        ], md=2, style={"padding": "0px"}),
        dbc.Col([
            dbc.Container(id="page-content", fluid=True, style={"height": "100%", "width": "100%",
                                                                "padding-left": "14px"})
        ], style={"padding": "0px"})
    ])

], fluid=True)


@app.callback(Output("page-content", "children"), Input("url",
                                                        "pathname"))
def render_page_content(pathname):
    if pathname == "/home" or pathname == "/":
        return home.layout

    if pathname == "/quadro":
        return quadro.layout

@app.callback(
    Output('div_fantasma', 'children'),
    Input('store_tecnico', 'data'),
    Input('store_estagio', 'data'),
    Input('store_atividade', 'data'),
)

def update_file (tecnico_data, estagio_data, atividade_data):
    df_tecnico_aux = pd.DataFrame(tecnico_data)
    df_estagio_aux = pd.DataFrame(estagio_data)
    df_atividade_aux = pd.DataFrame(atividade_data)


    conn = sqlite3.connect('sistema.db')

    df_tecnico_aux.to_sql('tecnico', conn, if_exists='replace', index=False)
    conn.commit()
    df_estagio_aux.to_sql('estagio', conn, if_exists='replace', index=False)
    conn.commit()
    df_atividade_aux.to_sql('atividade', conn, if_exists="replace", index=False)
    return []


if __name__ == "__main__":
    app.run_server(port=8055, debug=True)


