from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table
from app import app

# ======== Layout ========= #
layout = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Estagios Cadastrados")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        html.Div(id='estagio_table', className="dbc"),
                    ]),
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Sair", id="sair_button_estagio", color="danger"),
                dbc.Button("Novo", id="novo_estagio_button", color="success")
            ])
        ], id="modal_estagio", size="lg", is_open=False)


# ====== Callbacks ======= #

@app.callback(
    Output('estagio_table', 'children'),
    Input('store_estagio', 'data')
    # Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def table(data):
    df = pd.DataFrame(data)

    df = df.fillna('-')
    return [dash_table.DataTable(
        id='datatable',
        columns = [{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        page_size=10,
        page_current=0)]