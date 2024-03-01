from dash.dependencies import Input, Output, State, ALL
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import json
from app import app
from datetime import date
from sql_beta import df_estagio, df_tecnico




# =========  Layout  =========== #

layout = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Cadastro de Atividades')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col(
                    [
                    html.Div(id='cadastro_table', className="dbc"),
                    html.H6("Nome do Cliente: ", className="text-left"),
                    dbc.Input(id='input-cliente', value='', type='text',
                              style={'width': '300px'})
                ], sm=12, md=6),
                dbc.Col([
                        html.H6("Numero do PES: ", className="text-left"),
                        dbc.Input(id='input-pes', value='', type='text',
                                  style={'width': '200px'})
                    ], sm=12, md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H6("Modelo do Equipamento: ", className="text-left"),
                    dbc.Input(id='input-modelo', value='', type='text',
                                          style={'width': '300px'})
                ]),
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Col([
                    html.H6("Técnico: ", className="text-left"),
                    dcc.Dropdown(
                        id="input-tecnico",
                            options=[{'label': i, 'value': i} for i in df_tecnico["Tecnico"]],
                        value="", style={'width': '300px'}, placeholder=''),
                ], style={'margin-top': '25px'}, sm=12, md=6),
                dbc.Col([
                    html.H6("Estagio: ", className="text-left"),
                    dcc.Dropdown(
                        id="input-estagio",
                            options=[{'label': i, 'value': i} for i in df_estagio["Estagio"]],
                        value="", style={'width': '300px'}, placeholder=''),
                ], style={'margin-top': '25px'}, sm=12, md=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H6("Inicio: ", className="text-left"),
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        className='dbc',
                        display_format='DD/MM/YYYY',
                        placeholder='',
                        initial_visible_month=date.today(),
                        date=date.today(),
                    ),
                ], style={'margin-top': '25px'}, sm=12, md=4
                        ),
                dbc.Col(
                    [
                        html.H6("Previsão de Término: ", className="text-left"),
                        dcc.DatePickerSingle(
                            id='expected-end-date-picker',
                            className='dbc',
                            display_format='DD/MM/YYYY',
                            placeholder='',
                            initial_visible_month=date.today(),
                            date=None,
                        )
                    ], style={'margin-top': '30px'}, sm=12, md=4
                ),
                dbc.Col([
                    dbc.Row([
                       dbc.Col([
                           html.H6("Término: ", className="text-left"),
                           dcc.DatePickerSingle(
                               id='end-date-picker',
                               className='dbc',
                               display_format='DD/MM/YYYY',
                               placeholder='',
                               initial_visible_month=date.today(),
                               date=None,
                           )
                       ])
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Switch(id='manutenção_concluida', label="Manutenção Concluida", value=False)
                        ])
                    ])
                ], style={'margin-top': '30px'}, sm=12, md=4),
            ]),
            dbc.Row([
                html.H6("Observação: ", className="text-center"),
                dbc.Textarea(id='input-observacao', placeholder="", style={'width': '80%','margin-left': '90px', 'margin-right': '120px'},),
            ], style={'margin-top': '25px'}),
            html.H5(id='div_erro')
        ]),
    dbc.ModalFooter([
        dbc.Button('Sair', id='btn-sair', n_clicks=0, className='me-md-2', color='danger'),
        dbc.Button('Cadastrar Atividade', id='btn-cadastrar', n_clicks=0, className='me-md-2', color="success"),
    ])
],id='modal_cadastro', size='lg', is_open=False)


# =============  Callbacks ============== #
# Callback para abrir o modal
@app.callback(
    Output('modal_cadastro', 'is_open'),
    Output('store_intermedio', 'data'),
    Input({'type': 'editar_pes', 'index': ALL}, 'n_clicks'),
    Input('cadastro_button', 'n_clicks'),
    Input("btn-sair", 'n_clicks'),
    State('modal_cadastro', 'is_open'),
    State('store_atividade', 'data'),
    State('store_intermedio', 'data')
)
def abrir_modal_pes(n_editar, n_cadastro, n_sair, is_open, store_atividade, store_intermedio):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    first_call = True if callback_context.triggered[0]['value'] == None else False
    if first_call:
        return is_open, store_intermedio

    if (trigg_id == 'cadastro_button') or (trigg_id == 'btn-sair'):
        df_int = pd.DataFrame(store_intermedio)
        df_int = df_int[:-1]
        store_intermedio = df_int.to_dict()

        return not is_open, store_intermedio

    if n_editar:
        trigg_dict = json.loads(callback_context.triggered[0]['prop_id'].split('.')[0])
        pes = trigg_dict['index']

        df_int = pd.DataFrame(store_intermedio)
        df_atividade = pd.DataFrame(store_atividade)
        df_atividade['Pes'] = pd.to_numeric(df_atividade['Pes'], errors='coerce')

        valores = df_atividade.loc[df_atividade['Pes'] == pes].values.tolist()
        valores = valores[0] + [True]

        df_int = df_int[:-1]
        df_int.loc[len(df_int)] = valores
        store_intermedio = df_int.to_dict()

        return not is_open, store_intermedio
#callback para CRUD de processos
@app.callback(
    Output('store_atividade', 'data'),
    Output('div_erro', 'children'),
    Output('div_erro', 'style'),
    Output('input-pes', 'value'),
    Output('input-cliente', 'value'),
    Output('input-modelo', 'value'),
    Output('input-tecnico', 'value'),
    Output('input-estagio', 'value'),
    Output('start-date-picker', 'date'),
    Output('expected-end-date-picker', 'date'),
    Output('end-date-picker', 'date'),
    Output('manutenção_concluida', 'value'),
    Output('input-observacao', 'value'),
    Output('input-pes', 'disabled'),
    Input('cadastro_button', 'n_clicks'),
    Input('btn-cadastrar', 'n_clicks'),
    Input({'type': 'deletar_pes', 'index': ALL}, 'n_clicks'),
    Input('store_intermedio', 'data'),
    State('modal_cadastro', 'is_open'),
    State('store_atividade', 'data'),
    State('input-pes', 'value'),
    State('input-cliente', 'value'),
    State('input-modelo', 'value'),
    State('input-tecnico', 'value'),
    State('input-estagio', 'value'),
    State('start-date-picker', 'date'),
    State('expected-end-date-picker', 'date'),
    State('end-date-picker', 'date'),
    State('manutenção_concluida', 'value'),
    State('input-observacao', 'value'),
    prevent_initial_call=True
)
def crud_pes(n_cadastro, n_save, n_delete, store_int, is_open, store_atividade, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao):
    first_call = True if (callback_context.triggered[0]['value'] == None or callback_context.triggered[0]['value'] == False) else False
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if first_call:
        no_pes = cliente = modelo = tecnico = estagio = start_date = expected_date = end_date = observacao = None
        manutencao_concluida = False
        return store_atividade, [], {}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False

    if trigg_id == 'btn-cadastrar':
        df_atividade = pd.DataFrame(store_atividade)
        df_int = pd.DataFrame(store_int)

        if len(df_int.index) == 0: #Novo processo
            if None in [no_pes, cliente, modelo, estagio, start_date]:
                return store_atividade, ["Todos dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red'}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False
            if (no_pes in df_atividade['Pes'].values):
                return store_atividade, ["Número de processo ja existe no sistema!"], {'margin-bottom': '15px', 'color': 'red'}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False


            start_date = pd.to_datetime(start_date).date()
            try:
                expected_date = pd.to_datetime(expected_date).date()
            except:
                pass
            try:
                end_date = pd.to_datetime(end_date).date()
            except:
                pass

            df_atividade.reset_index(drop=True, inplace=True)

            manutencao_concluida = 0 if manutencao_concluida == False else 1
            if manutencao_concluida == 0: end_date = None

            df_atividade.loc[df_atividade.shape[0]] = [no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao]

            store_atividade = df_atividade.to_dict()
            no_pes = cliente = modelo = tecnico = estagio = start_date = expected_date = end_date = observacao = None
            manutencao_concluida = False
            return store_atividade, ['Processo salvo com sucesso!'], {'margin-bottom': '15px', 'color': 'green'}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False

        else:  # Edição de processo
            manutencao_concluida = 0 if manutencao_concluida == False else 1
            if manutencao_concluida == 0: end_date = None
            df_atividade['Pes'] = pd.to_numeric(df_atividade['Pes'], errors='coerce')
            index = df_atividade.loc[df_atividade['Pes'] == no_pes].index[0]
            df_atividade.loc[index, df_atividade.columns] = [no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao]

            store_atividade = df_atividade.to_dict()
            no_pes = cliente = modelo = tecnico = estagio = start_date = expected_date = end_date = observacao = None
            manutencao_concluida = False
            return store_atividade, ['Processo salvo com sucesso!'], {'margin-bottom': '15px', 'color': 'green'}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False

    if 'deletar_pes' in trigg_id:
        df_atividade = pd.DataFrame(store_atividade)

        trigg_id_dict = json.loads(trigg_id)
        pes = trigg_id_dict['index']
        df_atividade['Pes'] = pd.to_numeric(df_atividade['Pes'], errors='coerce')
        index_pes = df_atividade.loc[df_atividade['Pes'] == pes].index[0]
        df_atividade.drop(index_pes, inplace=True)
        df_atividade.reset_index(drop=True, inplace=True)

        store_atividade = df_atividade.to_dict()
        no_pes = cliente = modelo = tecnico = estagio = start_date = expected_date = end_date = observacao = None
        manutencao_concluida = False
        return store_atividade, [], {}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False

    if(trigg_id == 'store_intermedio') and is_open:
        try:
            df = pd.DataFrame(callback_context.triggered[0]['value'])
            df_atividade = pd.DataFrame(store_atividade)
            valores = df.head(1).values.tolist()[0]
            print(valores)

            no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, disabled = valores

            manutencao_concluida = False if manutencao_concluida == 0 else True

            return store_atividade, ['Modo de Edição: Número de Processo não pode ser alterado'], {'margin-bottom': '15px', 'color': 'green'}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, disabled
        except:
            no_pes = cliente = modelo = tecnico = estagio = start_date = expected_date = end_date = observacao = None
            manutencao_concluida = False
            return store_atividade, [], {}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False

    no_pes = cliente = modelo = tecnico = estagio = start_date = expected_date = end_date = observacao = None
    manutencao_concluida = False
    return store_atividade, [], {}, no_pes, cliente, modelo, tecnico, estagio, start_date, expected_date, end_date, manutencao_concluida, observacao, False

# Callback para atualizar o dropdown de tecnicos e estagio
# Tecnicos
@app.callback(
    Output('input-tecnico', 'options'),
    Input('store_tecnico', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return[{'label': i, 'value': i} for i in df['Tecnico']]

# Estagio
@app.callback(
    Output('input-estagio', 'options'),
    Input('store_estagio', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return[{'label': i, 'value': i} for i in df['Estagio']]
