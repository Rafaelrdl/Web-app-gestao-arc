from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from app import app

# ======== Layout ========= #
layout = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Adicione Um Novo Estagio")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Descrição"),
                        dbc.Input(id="estagio_nome", type="text")
                    ]),
                ]),
                html.Hr(),
                html.H5(id='div_erro3')
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancelar_novo_estagio_button", color="danger"),
                dbc.Button("Salvar", id="save_novo_estagio_button", color="success")
            ])
        ], id="modal_novo_estagio", size="lg", is_open=False)

# ======== Callbacks ========= #
# Callback para adicionar novos estagios
@app.callback(
    Output("store_estagio", "data"),
    Output("div_erro3", "children"),
    Output("div_erro3", 'style'),
    Input("save_novo_estagio_button", "n_clicks"),
    State("store_estagio", "data"),
    State("estagio_nome", "value"),
)
def novo_estagio(n, dataset, Estagio):
    erro = []
    style = []
    if n:
        if None in [Estagio]:
            return dataset, ["Todos os dados são obrigatórios para registro!"], {'margin-bottom': '15px',
                                                                                 "color": 'red'}

        df_estagio = pd.DataFrame(dataset)

        if Estagio in df_estagio["Estagio"].values:
            return dataset, [f"Estagio {Estagio} ja existe no sistema!"], {'margin-bottom': '15px',
                                                                         'color': 'red'}

        df_estagio.loc[df_estagio.shape[0]] = [Estagio]
        dataset = df_estagio.to_dict()

        return dataset, ["Cadastro realizado com sucesso!"], {'margin-bottom': '15px',
                                                              'color': 'green'}
    return dataset, erro, {}
