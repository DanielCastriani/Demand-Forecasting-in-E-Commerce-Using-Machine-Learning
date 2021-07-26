from controllers.variable_correlation_controller import feature_correlation, lag_correlation
import dash_core_components as dcc
import dash_html_components as html
from app import app
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers.database import load_numeric_column_names
from dash.dependencies import Input, Output
from utils.dropdown_utils import generate_list
import plotly.express as px
from components.slider import Slider
from utils.dropdown_utils import agg_mode_list

pg_id = 'lag-correlation'

numeric_columns = load_numeric_column_names()
numeric_columns = generate_list(numeric_columns)

agg_date_mode_list = agg_mode_list()


@app.callback(
    Output(f'{pg_id}-chart', 'figure'),
    [
        Input(f'{pg_id}-agg-mode', 'value'),
        Input(f'{pg_id}-variable', 'value'),
        Input(f'{pg_id}-lag-variable', 'value'),
        Input(f'{pg_id}-window', 'value'),
    ])
def update_figure(agg_mode: str, feature_column: str, lag_feature_column: str, window: int):
    corr = lag_correlation(
        agg_mode=agg_mode,
        feature_column=feature_column,
        lag_feature_column=lag_feature_column,
        window=window,
    )

    if feature_column==lag_feature_column:
        feature_column = f'{feature_column}(A)'
        lag_feature_column = f'{lag_feature_column}(B)'

    fig = px.bar(corr, x=lag_feature_column, y=feature_column)
    fig.update_layout(template='plotly_dark', title="Correlação Atrasada",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
        Dropdown(id=f'{pg_id}-variable', label='Variável', value=numeric_columns[0]['value'], options=numeric_columns),
        Dropdown(id=f'{pg_id}-lag-variable', label='Variável Atrasada', value=numeric_columns[0]['value'], options=numeric_columns),
    ]),

    Content([
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': 'calc(90% - 64px)'},
        ),
        Slider(id=f'{pg_id}-window', value=10, min=3, max=90),
    ])
],  className='content-container')
