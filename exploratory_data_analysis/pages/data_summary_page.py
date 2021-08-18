from components.card import Card
from utils.search_utils import find_label
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


agg_2 = [
    ListItem(label="Total", value=-1),
    ListItem(label="Cidade", value=1),
    ListItem(label="Estado", value=2),
]


def update_chart(sellected_agg: int, feature: str, label: str, nbars: int = 15):
    res = eda_controller.feature_count(sellected_agg, feature)

    df = res['df'].head(nbars)
    n_categories = res['nunique']
    n_rows = res['rows']

    if sellected_agg != -1:
        title = find_label(sellected_agg, agg_2)
        title = f'{n_rows} {title}(s), {n_categories} {label}'
    else:
        title = f'{n_categories} {label}'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[df.columns[0]], y=df['count']))

    update_layout(fig, title)

    return fig


@app.callback(
    Output(f'{pg_id}-summary-info-container', 'children'), Input('url', 'pathname'))
def on_load(_: str):
    res = eda_controller.stats_info()

    return html.Div([

        Card(title='Média vendas Iterm Pedido', value=res['mean_product_qty'], id=f'{pg_id}-mean_product_qty'),
        Card(title='Total Vendas', value=res['total_qty'], id=f'{pg_id}-total_qty'),

        Card(title='Lucro Total', value=res['total_profit'], id=f'{pg_id}-total_profit', prefix='R$ '),
        Card(title='Média Lucro Diario/Produto', value=res['mean_product_profit'], id=f'{pg_id}-mean_product_profit', prefix='R$ '),


        Card(title='Média dias aprovação pedido', value=res['mean_days_to_approve'], id=f'{pg_id}-mean_days_to_approve'),

        Card(title='Média dias  postar Pedido', value=res['mean_days_to_post'], id=f'{pg_id}-mean_days_to_post'),
        Card(title='Máximo dias  posta Peidio', value=res['max_days_to_post'], id=f'{pg_id}-max_days_to_post'),

        Card(title='Média dias entrega', value=res['mean_days_to_deliver'], id=f'{pg_id}-mean_days_to_deliver'),
        Card(title='Mínimo dias entrega', value=res['min_days_to_deliver'], id=f'{pg_id}-min_days_to_deliver'),
        Card(title='Máximo dias entrega', value=res['max_days_to_deliver'], id=f'{pg_id}-max_days_to_deliver'),

        Card(title='Média estimativa Entrega', value=res['mean_days_estimated_to_deliver'], id=f'{pg_id}-mean_days_estimated_to_deliver'),
        Card(title='Mínimo estimativa Entrega', value=res['min_days_estimated_to_deliver'], id=f'{pg_id}-min_days_estimated_to_deliver'),
        Card(title='Máximo estimativa Entrega', value=res['max_days_estimated_to_deliver'], id=f'{pg_id}-max_days_estimated_to_deliver'),



    ], className='summary-info-container')


@app.callback(Output(f'{pg_id}-categories', 'figure'), [Input(f'{pg_id}-categories-agg', 'value')])
def update_categories(sellected_agg: int):
    return update_chart(sellected_agg, 'product_category_name', 'Categoria(s)', 30)


@app.callback(Output(f'{pg_id}-customer', 'figure'), [Input(f'{pg_id}-customer-agg', 'value')])
def update_customer(sellected_agg: int):
    return update_chart(sellected_agg, 'customer_id', 'Cliente(s)', 15)


@app.callback(Output(f'{pg_id}-seller', 'figure'), [Input(f'{pg_id}-seller-agg', 'value')])
def update_seller(sellected_agg: int):
    return update_chart(sellected_agg, 'seller_id', 'Vendedor(es)', 15)


@app.callback(Output(f'{pg_id}-order-status', 'figure'), [Input(f'{pg_id}-order-status-agg', 'value')])
def update_seller(sellected_agg: int):
    return update_chart(sellected_agg, 'order_status', 'Status', 15)

@app.callback(Output(f'{pg_id}-is-delayed', 'figure'), [Input(f'{pg_id}-is-delayed-agg', 'value')])
def update_seller(sellected_agg: int):
    return update_chart(sellected_agg, 'is_delayed', 'Em Atraso', 15)

layout = html.Div([

    Content([

        html.Div([], id=f'{pg_id}-summary-info-container'),

        html.Div([
            html.Div([
                dcc.Graph(
                    id=f'{pg_id}-categories',
                    style={'width': '100%', 'height': '100%'},
                ),
                RadioList(id=f'{pg_id}-categories-agg', options=agg_2, value=agg_2[0]['value'])
            ], style={'width': '100%'}, className='summary-chart-row'),
        ]),


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
        ], style={'display': 'flex'}, className='summary-chart-row'),

        html.Div([
            html.Div([
                dcc.Graph(
                    id=f'{pg_id}-order-status',
                    style={'width': '100%', 'height': '100%'},
                ),
                RadioList(id=f'{pg_id}-order-status-agg', options=agg_2, value=agg_2[0]['value'])
            ], style={'width': '100%', 'height': '75%'}),

            html.Div([
                dcc.Graph(
                    id=f'{pg_id}-is-delayed',
                    style={'width': '100%', 'height': '100%'},
                ),
                RadioList(id=f'{pg_id}-is-delayed-agg', options=agg_2, value=agg_2[0]['value'])
            ], style={'width': '100%', 'height': '75%'}),



        ], style={'display': 'flex'}, className='summary-chart-row')





    ]),
],  className='content-container')
