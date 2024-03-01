import dash
import dash_bootstrap_components as dbc

estilos = [dbc.icons.FONT_AWESOME, dbc.themes.MINTY]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=estilos)

app.config["suppress_callback_exceptions"] = True
app.scripts.config.serve_locally = True
server = app.server
