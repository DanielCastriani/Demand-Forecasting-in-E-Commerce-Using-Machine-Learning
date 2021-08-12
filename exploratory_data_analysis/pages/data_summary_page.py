from utils.dropdown_utils import agg_mode_list
from components.dropdown import Dropdown
from typing import List
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from components.containers import Content, FilterContainer
from dash.dependencies import Input, Output

pg_id = 'price-x-ext-data-page'

agg_date_mode_list = agg_mode_list()


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
    ]),

    Content(
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        )
    )
],  className='content-container')
