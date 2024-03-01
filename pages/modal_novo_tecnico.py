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
                        dbc.Label("Nome do Tecnico"),
                        dbc.Input(id="tecnico_nome", type="text")
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Cargo"),
                        dbc.Input(id="tecnico_cargo", type="text")
                    ]),
                ]),
                html.H5(id='div_erro2')
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancelar_novo_tecnico_button", color="danger"),
                dbc.Button("Salvar", id="save_novo_tecnico_button", color="success")
            ])
        ], id="modal_novo_tecnico", size="lg", is_open=False)

# ======== Callbacks ========= #
# Callback para adicionar novos estagios
@app.callback(
    Output("store_tecnico", "data"),
    Output("div_erro2", "children"),
    Output("div_erro2", 'style'),
    Input("save_novo_tecnico_button", "n_clicks"),
    State("store_tecnico", "data"),
    State("tecnico_nome", "value"),
    State("tecnico_cargo", "value"),
)
def novo_estagio(n, dataset, Tecnico, Cargo):
    erro = []
    style = []
    if n:
        if None in [Tecnico, Cargo]:
            return dataset, ["Todos os dados são obrigatórios para registro!"], {'margin-bottom': '15px',
                                                                                 "color": 'red'}

        df_tecnico = pd.DataFrame(dataset)

        if Tecnico in df_tecnico["Tecnico"].values:
            return dataset, [f"Tecnico{Tecnico} ja existe no sistema!"], {'margin-bottom': '15px',
                                                                         'color': 'red'}
        elif Cargo in df_tecnico["Cargo"].values:
            return dataset, [f"Tecnico{Cargo} ja existe no sistema!"], {'margin-bottom': '15px',
                                                                         'color': 'red'}

        df_tecnico.loc[df_tecnico.shape[0]] = [Tecnico, Cargo]
        dataset = df_tecnico.to_dict()

        return dataset, ["Cadastro realizado com sucesso!"], {'margin-bottom': '15px',
                                                              'color': 'green'}
    return dataset, erro, {}
