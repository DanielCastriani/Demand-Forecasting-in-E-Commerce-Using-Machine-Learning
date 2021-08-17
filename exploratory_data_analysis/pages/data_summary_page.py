from components.theme import update_layout
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from components.radio import RadioList
from dash.dependencies import Input, Output
from typehint.datatype import ListItem
from utils.dropdown_utils import agg_mode_list
from controllers import eda_controller

pg_id = 'price-x-ext-data-page'

agg_date_mode_list = agg_mode_list()

agg = [
    ListItem(label="Cidade", value=1),
    ListItem(label="Estado", value=2),
]


@app.callback(Output(f'{pg_id}-customer', 'figure'), [Input(f'{pg_id}-customer-agg', 'value')])
def update_customer(agg: int):
    res = eda_controller.customer_summary(agg)

    title = 'Cidade' if agg == 1 else 'Estado'
    col = 'customer_city' if agg == 1 else 'customer_state'

    df = res['costumers'].head(15)
    n_customers = res['nunique']
    n_cites = res['rows']

    title = f'{n_cites} {title}(s), {n_customers} clientes'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[col], y=df['customer_id']))

    update_layout(fig, title)

    return fig


@app.callback(Output(f'{pg_id}-seller', 'figure'), [Input(f'{pg_id}-seller-agg', 'value')])
def update_seller(agg: int):
    res = eda_controller.seller_summary(agg)

    title = 'Cidade' if agg == 1 else 'Estado'
    col = 'seller_city' if agg == 1 else 'seller_state'

    df = res['costumers'].head(15)
    n_sellers = res['nunique']
    n_cites = res['rows']

    title = f'{n_cites} {title}(s), {n_sellers} vendedor(es)'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[col], y=df['seller_id']))

    update_layout(fig, title)

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
    ]),

    Content([
        html.Div([
            html.Div([
                dcc.Graph(
                    id=f'{pg_id}-customer',
                    style={'width': '100%', 'height': '100%'},
                ),
                RadioList(id=f'{pg_id}-customer-agg', options=agg, value=agg[0]['value'])
            ], style={'width': '100%', 'height': '75%'}),

            html.Div([
                dcc.Graph(
                    id=f'{pg_id}-seller',
                    style={'width': '100%', 'height': '100%'},
                ),
                RadioList(id=f'{pg_id}-seller-agg', options=agg, value=agg[0]['value'])
            ], style={'width': '100%', 'height': '75%'}),
        ], style={'display': 'flex', 'height': '100%'})
    ]
    )
],  className='content-container')
