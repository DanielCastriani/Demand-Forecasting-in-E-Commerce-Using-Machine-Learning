from typing import Dict, List
from utils.df_utils import concat_lines

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from app import app
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers import report_controller
from dash.dependencies import Input, Output
from utils.filter_utils import forecast_filter, forecast_filter_fill_output, get_report_filter

pg_id = 'train-report'


@app.callback(Output(f'{pg_id}-report-list', 'options'), Input('url', 'pathname'))
def on_load(_: str):
    success, body = report_controller.load_model_list()
    files = []
    if success:
        files = body

    return files


@app.callback([
    Output(f'{pg_id}-chart', 'figure'),

    Output(f'{pg_id}-is-delayed-div', 'className'),
    Output(f'{pg_id}-order-status-div', 'className'),
    Output(f'{pg_id}-category-div', 'className'),
    Output(f'{pg_id}-seller-id-div', 'className'),
    Output(f'{pg_id}-type-div', 'className'),

    Output(f'{pg_id}-is-delayed', 'options'),
    Output(f'{pg_id}-order-status', 'options'),
    Output(f'{pg_id}-category', 'options'),
    Output(f'{pg_id}-seller-id', 'options'),
    Output(f'{pg_id}-type', 'options'),

], [
    Input(f'{pg_id}-report-list', 'value'),
    Input(f'{pg_id}-is-delayed-div', 'className'),
    Input(f'{pg_id}-order-status-div', 'className'),
    Input(f'{pg_id}-category-div', 'className'),
    Input(f'{pg_id}-seller-id-div', 'className'),
    Input(f'{pg_id}-type-div', 'className'),


    Input(f'{pg_id}-is-delayed', 'value'),
    Input(f'{pg_id}-order-status', 'value'),
    Input(f'{pg_id}-category', 'value'),
    Input(f'{pg_id}-seller-id', 'value'),
    Input(f'{pg_id}-type', 'value'),
])
def uptate_report(
    model_name: str,
    is_delayed_classname: str,
    order_status_classname: str,
    product_category_name_classname: str,
    seller_id_classname: str,
    type_classname: str,

    is_delayed: str,
    order_status: str,
    product_category_name: str,
    seller_id: str,
    datatype: str,

):
    fig = go.Figure()

    fill_filters = model_name == -1

    if not fill_filters:
        success, df, filters = report_controller.get_report(
            model_name,
            is_delayed,
            order_status,
            product_category_name,
            seller_id,
            datatype,
        )

        styles = []
        options = []

        if success:

            styles, options = forecast_filter(
                is_delayed_classname,
                order_status_classname,
                product_category_name_classname,
                seller_id_classname,
                type_classname,
                filters,
                styles,
                options)

            fig.add_trace(go.Scatter(x=df['date'], y=df['real'], name='Real', mode='lines'))

            df = concat_lines(df)

            groups = list(enumerate(df.groupby('type')))
            for i, group in groups:
                g_info, df_g = group
                fig.add_trace(go.Scatter(x=df_g['date'], y=df_g['predicted'], name=g_info.capitalize(), mode='lines'))

        else:
            fill_filters = True

    if fill_filters:
        styles, options = forecast_filter_fill_output(
            is_delayed_classname,
            order_status_classname,
            product_category_name_classname,
            seller_id_classname,
            type_classname)

    fig.update_layout(
        template='plotly_dark',
        title="Treino/Test x Valor Real (soma)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        transition={"duration": 300})

    return [fig, *styles, *options]

layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-report-list', label='Modelo', value=-1, options=[], optionHeight=65),

        Dropdown(id=f'{pg_id}-is-delayed', label='Em atraso', value=-1, options=[], visible=False),
        Dropdown(id=f'{pg_id}-order-status', label='Status do pedido', value=-1, options=[], visible=False),
        Dropdown(id=f'{pg_id}-category', label='Categoria', value=-1, options=[], visible=False),
        Dropdown(id=f'{pg_id}-seller-id', label='Vendedor', value=-1, options=[], visible=False),
        Dropdown(id=f'{pg_id}-type', label='Tipo', value=-1, options=[], visible=False),
    ]),

    Content([
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        )
    ])

    # Slider(id='slider', value=30, min=5, max=120)
],  className='content-container')
