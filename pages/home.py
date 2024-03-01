from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from app import app
from sql_beta import df_estagio, df_tecnico

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# ======== Styles ========= #
card_style = {'height': '100%', 'margin-bottom': '12px'}

# Funções para gerar os Cards
# Checar o DataFrame e gerar Icones
def gerar_icones(df_atividade_aux, i):
    df_aux = df_atividade_aux.iloc[i]
    if df_aux['Manutenção Concluida'] == 'Sim':
        concluida = 'fa fa-check'
        color_c = 'green'
        concluida_text = 'Concluido'
    elif df_aux['Manutenção Concluida'] == 'Não':
        concluida = 'fa fa-times'
        color_c = 'red'
        concluida_text = 'Andamento'

    return df_aux, concluida, color_c, concluida_text

# Card padrão de contagem
def gerar_card_padrao(qnt_pes):
    card_padrao = dbc.Card([
        dbc.CardBody([
            html.H3(f"{qnt_pes} PES Encontrados", style={'font-weight': 'bold', 'color': 'gray'})
        ])
    ], style={'height': '100%', 'margin-bottom': '12px', 'backgroung=color': 'red'})
    return card_padrao

# Card qualquer de processo
def gerar_card_pes(df_aux, color_c, concluida, concluida_text):
    card_pes = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H2(f"Pes nº {df_aux['Pes']}")
                        ])
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            html.Ul([
                                html.Li([html.B('Cliente: ', style={'font-weight': 'bold'}), f"{df_aux['Cliente']}"]),
                                html.Li([html.B('Equipamento: ', style={'font-weight': 'bold'}), f"{df_aux['Equipamento']}"]),
                                html.Li([html.B('Estagio: ', style={'font-weight': 'bold'}), f"{df_aux['Estagio']}"]),
                                html.Li([html.B('Tecnico: ', style={'font-weight': 'bold'}), f"{df_aux['Tecnico']}"]),
                                html.Li([html.B('Observação: ', style={'font-weight': 'bold'}), f"{df_aux['Observação']}"]),
                            ])
                        ])
                    ])

                ],sm=12, md=6, style={'border-right': '2px solid lightgrey'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Ul([
                                html.Li([html.B('Inicio/Término: ', style={'font-weight': 'bold'}), f"{df_aux['Inicio']} - {df_aux['Termino']}"]),
                                html.Li([html.B('Previsão de Término: ', style={'font-weight': 'bold'}), f"{df_aux['Previsão de Término']}"]),
                            ])
                        ])
                    ], style={'margin-bottom': '32px'}),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Status", style={'margin-bottom': 0}),
                        ], sm=5, style={'text-align': 'right'}),
                        dbc.Col([
                            html.I(className=f'{concluida} fa-2x dbc', style={'color': f'{color_c}'}),
                        ], sm=2),
                        dbc.Col([
                            html.H5(f'{concluida_text}', style={'margin-bottom': 0}),
                        ], sm=5, style={'text-align': 'left'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([html.I(className="fa fa-pencil fa-2x")], style={'color': 'black'}, size='sm', outline=True,
                                       id={'type': 'editar_pes', 'index': int(df_aux['Pes'])})
                        ], md=2),
                        dbc.Col([
                            dbc.Button([html.I(className="fa fa-trash fa-2x")], style={'color': 'black'}, size='sm', outline=True,
                                       id={'type': 'deletar_pes', 'index': int(df_aux['Pes'])})
                        ], md=2),
                    ], style={'display': 'flex', 'justify-content': 'flex-end'})
                ], sm=12, md=6, style={'height': '100%', 'margin-top': 'auto', 'margin-bottom': 'auto'})
            ], style={'margin-top': '12px'})
        ])
    ], style=card_style, className='card_padrao')
    return card_pes

# ======== Layout ========= #
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("ENCONTRE A ATIVIDADE QUE VOCE PROCURA", style={'text-align': 'left', 'margin-left': '32px'})
        ], className='text-center')
    ], style={'margin-top': '14px'}),
    html.Hr(),
    dbc.Row([
        # Filtros
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Nº do PES"),
                                ], sm=12)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(id='pes_filter', placeholder='Insira...', type="number")
                                ], sm=12, md=12, lg=8),
                                dbc.Col([
                                    dbc.Button([html.I(className='fa fa-search')], id='pesquisar_num_pes', color="danger")
                                ], sm=12, md=12, lg=4)
                            ], style={'margin-bottom': '32px'}),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Status")
                                ])
                            ], style={'margin-top': '32px'}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[{"label": "Concluidos", "value": 1}],
                                        id="switches",
                                        switch=True

                                    ),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Estagio")
                                ])
                            ], style={'margin-top': '32px'}),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id="drop_estagio",
                                        options=[{'label': i, 'value': i} for i in df_estagio["Estagio"]],
                                        placeholder='Selecione o Estagio',
                                        className='dbc'
                                    ),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Nome do Cliente")
                                ])
                            ], style={'margin-top': '24px'}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button([html.I(className='fa fa-search')], id="pesquisar_cliente", color='light')
                                ], sm=2),
                                dbc.Col([
                                    dbc.Input(id="input_cliente_pesquisar", placeholder='Digite o nome do cliente', type='text')
                                ], sm=10)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Tecnicos")
                                ])
                            ], style={'margin-top': '24px'}),
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='Drop_tecnicos_filter',
                                        options=[{'label': i, 'value': i} for i in df_tecnico["Tecnico"]],
                                        placeholder='Selecione o Tecnico',
                                        className='dbc'
                                    ),
                                )
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("Todos os PES", id="pesquisa_todos", style={'width': '100%'}, color='danger')
                                ])
                            ], style={'margin-top': '24px'})
                        ], style={'margin': '20px'})
                    ])
                ])
            ])
        ],sm=12, md=5, lg=4),
        dbc.Col([
            dbc.Container(id='card_generator', fluid=True, style={'width': '100%', 'padding': '0px 0px 0px 0px', 'margin': '0px 0px 0px 0px'})
        ], sm=12, md=7, lg=8, style={'padding-left': '0px'})
    ])
], fluid=True, style={'height': '100%', 'padding':'10px', 'margin': 0, 'padding-left': 0 })

# =============  Callbacks ============== #
# callback para atualizar o dropdown de estagio
@app.callback(
    Output('drop_estagio','options'),
    Input('store_estagio', 'data')
)
def atu_estagio(data):
    df = pd.DataFrame(data)
    return[{'label': i, 'value': i} for i in df["Estagio"]]

# callback para atualizar o dropdown de tecnico
@app.callback(
    Output('Drop_tecnicos_filter', 'options'),
    Input('store_tecnico', 'data')
)
def atu_tecnico(data):
    df = pd.DataFrame(data)
    return[{'label': i, 'value': i} for i in df["Tecnico"]]

# Callback para gerar o conteudo dos cards
@app.callback(
    Output('card_generator', 'children'),
    Output('drop_estagio', 'value'),
    Output('Drop_tecnicos_filter', 'value'),
    Output('pes_filter', 'value'),
    Output('input_cliente_pesquisar', 'value'),
    Input('pesquisar_cliente', 'n_clicks'),
    Input('pesquisa_todos', 'n_clicks'),
    Input('drop_estagio', 'value'),
    Input('Drop_tecnicos_filter', 'value'),
    Input('pesquisar_num_pes', 'n_clicks'),
    Input('store_atividade', 'data'),
    Input('store_tecnico', 'data'),
    Input('store_estagio', 'data'),
    Input('switches', 'value'),
    State('pes_filter', 'value'),
    State('input_cliente_pesquisar', 'value'),
)
def generate_cards(n, n2, estagio_filter, tecnico_filter, n3, atividade_data, tecnico_data, estagio_data, switches,
                   pes_filter, cliente):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # iniciar os cards
    cards = []

    # Iniciar possiveis dataframes
    df_tecnico_aux = pd.DataFrame(tecnico_data)
    df_atividade_aux = pd.DataFrame(atividade_data)
    df_estagio_aux = pd.DataFrame(estagio_data)


    if (trigg_id == '' or trigg_id == 'store_atividade' or trigg_id == 'store_tecnico'
            or trigg_id == 'store_estagio' or trigg_id == 'pesquisa_todos' or trigg_id == 'switches_value'):
        if trigg_id != 'pesquisa_todos':
            if switches == 1:  # Verifica se o valor 1 está na lista de valores do switch
                df_atividade_aux = df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 1]



        df_atividade_aux = df_atividade_aux.sort_values(by='Inicio', ascending=False)

        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 0, 'Manutenção Concluida'] = 'Não'
        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 1, 'Manutenção Concluida'] = 'Sim'

        df_atividade_aux = df_atividade_aux.fillna('-')
        # inserir o card padrão
        qnt_pes = len(df_atividade_aux)
        cards += [gerar_card_padrao(qnt_pes)]

        for i in range(len(df_atividade_aux)):
            df_aux, concluida, color_c, concluida_text = gerar_icones(df_atividade_aux, i)
            card = gerar_card_pes(df_aux, color_c, concluida, concluida_text)
            cards += [card]

        return cards, None, None, None, None

    # Pesquisa de texto por número de pes
    elif trigg_id == 'pesquisar_num_pes':
        # Dados
        df_atividade_aux = df_atividade_aux.loc[df_atividade_aux['Pes'] == pes_filter].sort_values(by='Inicio', ascending=False)
        print(f"Conteudo de df atividade aux:{df_atividade_aux}\n\n")

        if len(df_atividade_aux) == 0:
            cards += [gerar_card_padrao(len(df_atividade_aux))]
            return cards, None, pes_filter, None, None

        # Processos
        df_atividade_aux = df_atividade_aux.sort_values(by='Inicio', ascending=False)

        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 0, 'Manutenção Concluida'] = 'Não'
        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 1, 'Manutenção Concluida'] = 'Sim'

        df_atividade_aux = df_atividade_aux.fillna('-')

        # Inserindo o card padrão com a quantidade de processos
        qnt_pes = len(df_atividade_aux)
        cards += [gerar_card_padrao(qnt_pes)]

        # Itenrando sobre os processos possíveis
        for i in range(len(df_atividade_aux)):
            df_aux, concluida, color_c, concluida_text = gerar_icones(df_atividade_aux, i)
            card = gerar_card_pes(df_aux, concluida, color_c, concluida_text)
            cards += [card]

        return cards, None, None, None, None

    # pesquisar por nome do cliente
    elif trigg_id == 'pesquisar_cliente':
        if cliente in df_atividade_aux['Cliente'].values:

            # Dados
            df_atividade_aux = df_atividade_aux.loc[df_atividade_aux['Cliente'] == cliente].sort_values(by='Inicio', ascending=False)
            nome = df_atividade_aux.iloc[0]['Cliente']

            # Card do cliente
            card_cliente = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4(f"Cliente: {nome}"),
                        ]),
                    ])
                ])
            ], style=card_style)
            cards += [card_cliente]

            # Processos
            df_atividade_aux = df_atividade_aux.sort_values(by='Inicio', ascending=False)

            df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 0, 'Manutenção Concluida'] = 'Não'
            df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 1, 'Manutenção Concluida'] = 'Sim'

            df_atividade_aux = df_atividade_aux.fillna('-')

            # Inserindo o card padrão com a quantidade de processos
            qnt_pes = len(df_atividade_aux)
            cards += [gerar_card_padrao(qnt_pes)]

            # Itenrando sobre os processos possíveis
            for i in range(len(df_atividade_aux)):
                df_aux, concluida, color_c, concluida_text = gerar_icones(df_atividade_aux, i)
                card = gerar_card_pes(df_aux, concluida, color_c, concluida_text)
                cards += [card]

            return cards, None, None, None, cliente
        else:
            card = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.I(className='fa fa-exclamation dbc', style={'font-size': '4em'})
                        ], sm=3, className='text-center'),
                        dbc.Col([
                            html.H1("Nenhum Cliente correspondente ao que foi digitado no banco de dados.")
                        ], sm=9)
                    ])
                ])
            ], style=card_style)
            cards += [card]

            return cards, None, None, cliente, None

        # filtro dropdown dos estagios ok
    elif (trigg_id == 'drop_estagio'):
        # Dados
        df_aux = df_estagio_aux.loc[df_estagio_aux['Estagio'] == estagio_filter]
        status = estagio_filter

        # Card do Estagio
        card_estagio = dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4(f"Estagio: {status}"),
                        html.Hr(),
                    ]),
                ])
            ])
        ], style=card_style)
        cards += [card_estagio]

        # Processos
        df_atividade_aux = df_atividade_aux[df_atividade_aux['Estagio'] == status]
        df_atividade_aux = df_atividade_aux.sort_values(by='Inicio', ascending=False)

        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 0, 'Manutenção Concluida'] = 'Não'
        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 1, 'Manutenção Concluida'] = 'Sim'

        df_atividade_aux = df_atividade_aux.fillna('-')

        # Inserindo o card padrão com a quantidade de processos
        qnt_pes = len(df_atividade_aux)
        cards += [gerar_card_padrao(qnt_pes)]

        # Itenrando sobre os processos possíveis
        for i in range(len(df_atividade_aux)):
            df_aux, concluida, color_c, concluida_text = gerar_icones(df_atividade_aux, i)
            card = gerar_card_pes(df_aux, concluida, color_c, concluida_text)
            cards += [card]

        return cards, estagio_filter, None, None, None

        # filtro dropdown dos estagios OK
    elif (trigg_id == 'Drop_tecnicos_filter'):
        # Dados
        df_aux = df_tecnico_aux.loc[df_tecnico_aux['Tecnico'] == tecnico_filter]
        tecnico = tecnico_filter
        cargo = df_aux.iloc[0]['Cargo']

        # Card do Estagio
        card_tecnico = dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4(f"Tecnico: {tecnico}"),
                        html.Hr(),
                        html.H4(f"Cargo: {cargo}"),
                    ]),
                ])
            ])
        ], style=card_style)
        cards += [card_tecnico]

        # Processos
        df_atividade_aux = df_atividade_aux[df_atividade_aux['Tecnico'] == tecnico]
        df_atividade_aux = df_atividade_aux.sort_values(by='Inicio', ascending=False)

        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 0, 'Manutenção Concluida'] = 'Não'
        df_atividade_aux.loc[df_atividade_aux['Manutenção Concluida'] == 1, 'Manutenção Concluida'] = 'Sim'

        df_atividade_aux = df_atividade_aux.fillna('-')

        # Inserindo o card padrão com a quantidade de processos
        qnt_pes = len(df_atividade_aux)
        cards += [gerar_card_padrao(qnt_pes)]

        # Itenrando sobre os processos possíveis
        for i in range(len(df_atividade_aux)):
            df_aux, concluida, color_c, concluida_text = gerar_icones(df_atividade_aux, i)
            card = gerar_card_pes(df_aux, concluida, color_c, concluida_text)
            cards += [card]

        return cards, None, tecnico_filter, None, None


