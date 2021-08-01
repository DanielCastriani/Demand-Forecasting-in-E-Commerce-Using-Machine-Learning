from typing import List
from components.checklist import Checklist
from typehint.datatype import ListItem
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app, categories
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers.database import load_numeric_column_names
from controllers.variable_correlation_controller import mean_by_cat_date
from dash.dependencies import Input, Output
from utils.dropdown_utils import agg_mode_list, generate_list_items

pg_id = 'external-data'


agg_date_mode_list = agg_mode_list()

numeric_columns = generate_list_items(load_numeric_column_names())
categories_list_items = generate_list_items(categories, add_all=True)


arr = [[i, el] for i, el in enumerate(numeric_columns) if el['value'] == 'qty']
if len(arr):
    i, el = arr[0]
    el['label'] = f"{el['label']} (Total)"
    numeric_columns[i] = el


@app.callback(
    Output(f'{pg_id}-chart', 'figure'),
    [
        Input(f'{pg_id}-agg-mode', 'value'),
        Input(f'{pg_id}-variable', 'value'),
        Input(f'{pg_id}-category', 'value'),
        Input(f'{pg_id}-compare-mode', 'value'),
    ])
def update_figure(agg_mode: str, feature: str, category: str, compare_mode: List[str]):

    is_compare = 'cp-category' in compare_mode

    df = mean_by_cat_date(agg_mode, feature, category, is_compare)

    fig = go.Figure()

    if is_compare:
        for i, group in enumerate(df.groupby('product_category_name')):
            g_info, df_g = group
            trace_visible = True if i == 0 else 'legendonly'

            fig.add_trace(go.Scatter(x=df_g['date'], y=df[feature], name=g_info, mode='lines', visible=trace_visible))
    else:
        fig.add_trace(go.Scatter(x=df['date'], y=df[feature], name='', mode='lines', visible=True))

    fig.update_layout(template='plotly_dark', title="Média por Data",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      showlegend=True)

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
        Dropdown(id=f'{pg_id}-variable', label='Variável', value=numeric_columns[0]['value'], options=numeric_columns),
        Dropdown(id=f'{pg_id}-category', label='Categoria', value=categories_list_items[0]['value'], options=categories_list_items),
        Checklist(
            id=f'{pg_id}-compare-mode',
            options=[ListItem(label='Comparar Categorias', value='cp-category')]
        )
    ]),

    Content(
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        )
    )

    # Slider(id='slider', value=30, min=5, max=120)
],  className='content-container')
