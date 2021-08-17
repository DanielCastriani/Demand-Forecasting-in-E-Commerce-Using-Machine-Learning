from utils.search_utils import find_label
from components.theme import update_layout
from typing import List
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app, categories
from components.checklist import Checklist
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers.database import load_numeric_column_names
from dash.dependencies import Input, Output
from typehint.datatype import ListItem
from utils.dropdown_utils import agg_mode_list, generate_list_items

from controllers import variable_correlation_controller

pg_id = 'price-x-ext-data-page'


agg_date_mode_list = agg_mode_list()

numeric_columns = generate_list_items(load_numeric_column_names())
categories_list_items = generate_list_items(categories, add_all=True)


@app.callback(
    Output(f'{pg_id}-chart', 'figure'),
    [
        Input(f'{pg_id}-agg-mode', 'value'),
        Input(f'{pg_id}-variable', 'value'),
        Input(f'{pg_id}-category', 'value'),
        Input(f'{pg_id}-normalize-data', 'value'),
    ])
def update_figure(agg_mode: str, var_col: str, category: str, compare_mode: List[str]):
    is_normalize = 'cb-normalize' in compare_mode

    df = variable_correlation_controller.ext_data_x_feature(agg_mode, var_col, category, is_normalize)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['date'], y=df[var_col], name=var_col, mode='lines'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['dollar'], name='Dollar', mode='lines'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['ipca'], name='IPCA', mode='lines'))

    feature_label = find_label(var_col, numeric_columns)

    feature_label = f'{feature_label} (Média)' if feature_label != 'Qty' else f'{feature_label} (Soma)'

    update_layout(fig, f"{feature_label} x Dollar/IPCA", showlegend=True)

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
        Dropdown(id=f'{pg_id}-variable', label='Variável', value=numeric_columns[0]['value'], options=numeric_columns),
        Dropdown(id=f'{pg_id}-category', label='Categoria', value=categories_list_items[0]['value'], options=categories_list_items),
        Checklist(
            id=f'{pg_id}-normalize-data',
            value=['cb-normalize'],
            options=[ListItem(label='Normalizar Dados', value='cb-normalize')]
        )
    ]),

    Content(
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        )
    )
],  className='content-container')
