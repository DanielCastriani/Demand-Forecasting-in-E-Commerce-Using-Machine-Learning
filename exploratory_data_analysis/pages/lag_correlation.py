import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app, categories
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from components.slider import Slider
from components.theme import update_layout
from controllers.database import load_numeric_column_names
from controllers.variable_correlation_controller import lag_correlation
from dash.dependencies import Input, Output
from numpy.lib.shape_base import tile
from utils.dropdown_utils import agg_mode_list, generate_list_items
from utils.search_utils import find_label

pg_id = 'lag-correlation'

numeric_columns = load_numeric_column_names()
numeric_columns = generate_list_items(numeric_columns)

agg_date_mode_list = agg_mode_list()

categories_list_items = generate_list_items(categories, add_all=True)


@app.callback(
    Output(f'{pg_id}-chart', 'figure'),
    [
        Input(f'{pg_id}-agg-mode', 'value'),
        Input(f'{pg_id}-variable', 'value'),
        Input(f'{pg_id}-lag-variable', 'value'),
        Input(f'{pg_id}-category', 'value'),
        Input(f'{pg_id}-window', 'value'),
    ])
def update_figure(agg_mode: str, feature_column: str, lag_feature_column: str, category: str, window: int):
    corr = lag_correlation(
        agg_mode=agg_mode,
        feature_column=feature_column,
        lag_feature_column=lag_feature_column,
        category=category,
        window=window,
    )

    if feature_column == lag_feature_column:
        lba = find_label(feature_column, numeric_columns)
        title = f"Correlação Atrasada {lba}"

        feature_column = f'{feature_column}(A)'
        lag_feature_column = f'{lag_feature_column}(B)'
    else:
        lba = find_label(feature_column, numeric_columns)
        lbb = find_label(lag_feature_column, numeric_columns)
        title = f"Correlação Atrasada {lba} x {lbb}"

    fig = px.bar(corr, x=lag_feature_column, y=feature_column)

    feature_label = find_label(category, categories_list_items)
    title = title if category == -1 else f'{title} ({feature_label})'

    update_layout(fig, title)

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
        Dropdown(id=f'{pg_id}-variable', label='Variável', value=numeric_columns[0]['value'], options=numeric_columns),
        Dropdown(id=f'{pg_id}-lag-variable', label='Variável Atrasada', value=numeric_columns[0]['value'], options=numeric_columns),
        Dropdown(id=f'{pg_id}-category', label='Categoria', value=categories_list_items[0]['value'], options=categories_list_items),
    ]),

    Content([
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': 'calc(90% - 64px)'},
        ),
        Slider(id=f'{pg_id}-window', value=10, min=3, max=90),
    ])
],  className='content-container')
