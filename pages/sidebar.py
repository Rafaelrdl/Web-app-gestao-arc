from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from pages import modal_cadastro, modal_tecnico, modal_estagio, modal_novo_estagio, modal_novo_tecnico

style_sidebar = {
    "box-shadow": "2px 2px 10px 0px rgba(10, 9, 7, 0.10)",
    "margin": "10px",
    "padding": "10px",
    "height": "100vh",
    "margin-right":"-10px"
}

# Removendo o 'width' fixo do estilo do botão
button_style = {
    'color': 'white',
    'background-color': 'red',
    'border': '1px solid white',
    'border-radius': '5px',
    'padding': '10px',
    'text-align': 'center',
}

# Utilizar classes do Bootstrap para tornar os elementos responsivos
layout = dbc.Container([
    modal_novo_estagio.layout,
    modal_novo_tecnico.layout,
    modal_tecnico.layout,
    modal_estagio.layout,
    modal_cadastro.layout,
    dbc.Card(
    [
        html.H1('ARC',
                style={
                    'fontFamily': 'Namata, sans-serif',
                    'fontStyle': 'italic',
                    'fontWeight': 'bold',
                    'color': 'red',
                    'font-size': '60px'
                }),
        html.H3("Oficina",
                style={
                    'fontFamily': 'Namata, sans-serif',
                    'fontStyle': 'italic',
                    'fontWeight': 'bold',
                    'color': 'red',
                    'font-size': '30px'
                }),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink([html.I(className='fa-solid fa-house dbc'), "\tInício"], href="/home", active="True", style=button_style)),
                        dbc.NavItem(dbc.NavLink([html.I(className='fa-solid fa-circle-plus dbc'),"\tCadastro"], id='cadastro_button', active="True", style=button_style)),
                        dbc.NavItem(dbc.NavLink([html.I(className='fa-solid fa-display dbc'),"\tQuadro"], href="/quadro", active="True", style=button_style)),
                        dbc.NavItem(dbc.NavLink([html.I(className='fa-solid fa-users dbc'),"\tTécnicos"], id='tecnico_button', active="True", style=button_style)),
                        dbc.NavItem(dbc.NavLink([html.I(className='fa-solid fa-filter dbc'),"\tEstágios"], id='estagio_button',  active="True", style=button_style)),
                    ],
                    vertical=True,  # Esta propriedade faz com que os botões se alinhem verticalmente
                    pills=True,  # Esta propriedade destaca o link ativo
                    className="flex-column",  # Classe Bootstrap para direção da flexbox em coluna
                    fill=True
                )
            ])
        ]),

    ], style=style_sidebar
)
])

# ======= Callbacks ======= #
# Abrir Modal Novo Estagio
@app.callback(
    Output('modal_novo_estagio', "is_open"),
    Input('novo_estagio_button', 'n_clicks'),
    Input("cancelar_novo_estagio_button", 'n_clicks'),
    State('modal_novo_estagio', "is_open")
)
def toggle_modal(n, n2, is_open):
    if n or n2:
        return not is_open
    return is_open

# Abrir Modal Estagio
@app.callback(
    Output('modal_estagio', "is_open"),
    Input('estagio_button', 'n_clicks'),
    Input('sair_button_estagio', 'n_clicks'),
    Input('novo_estagio_button', 'n_clicks'),
    State('modal_estagio', 'is_open'),
)
def toggle_modal(n, n2, n3, is_open):
    if n or n2 or n3:
        return not is_open
    return is_open


# Abrir Modal Novo Tecnico
@app.callback(
    Output('modal_novo_tecnico', "is_open"),
    Input('novo_tecnico_button', 'n_clicks'),
    Input("cancelar_novo_estagio_button", 'n_clicks'),
    State('modal_novo_tecnico', "is_open")
)
def toggle_modal(n, n2, is_open):
    if n or n2:
        return not is_open
    return is_open

# Abrir Modal tecnico
@app.callback(
    Output('modal_tecnico', "is_open"),
    Input('tecnico_button', 'n_clicks'),
    Input('novo_tecnico_button', 'n_clicks'),
    Input('sair_button_tecnico', 'n_clicks'),
    State('modal_tecnico', 'is_open'),
)
def toggle_modal(n, n2, n3, is_open):
    if n or n2 or n3:
        return not is_open
    return is_open
