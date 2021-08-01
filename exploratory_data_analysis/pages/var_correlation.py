import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app, categories
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers.database import load_database, load_numeric_column_names
from controllers.variable_correlation_controller import feature_correlation
from dash.dependencies import Input, Output
from utils.dropdown_utils import agg_mode_list, generate_list_items

pg_id = 'var-correlation'

numeric_columns = load_numeric_column_names()
numeric_columns = generate_list_items(numeric_columns)

agg_date_mode_list = agg_mode_list()
categories_list_items = generate_list_items(categories, add_all=True)


@app.callback(
    Output(f'{pg_id}-chart', 'figure'),
    [
        Input(f'{pg_id}-agg-mode', 'value'),
        Input(f'{pg_id}-variable', 'value'),
        Input(f'{pg_id}-category', 'value'),
    ])
def update_figure(agg_mode: str, feature: str, category: str):
    corr = feature_correlation(agg_mode=agg_mode, feature=feature, category=category)

    fig = px.bar(corr, x='features', y=feature)
    fig.update_layout(template='plotly_dark', title="Correlação entre Variáveis",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      transition={"duration": 300})

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
        Dropdown(id=f'{pg_id}-variable', label='Variável', value=numeric_columns[0]['value'], options=numeric_columns),
        Dropdown(id=f'{pg_id}-category', label='Categoria', value=categories_list_items[0]['value'], options=categories_list_items),
    ]),

    Content(
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        ),

    )

    # Slider(id='slider', value=30, min=5, max=120)
],  className='content-container')
