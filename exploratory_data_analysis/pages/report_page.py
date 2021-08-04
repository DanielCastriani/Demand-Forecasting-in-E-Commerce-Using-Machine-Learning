import pandas as pd
from utils.dropdown_utils import generate_list_items
from typehint.datatype import ListItem
from typing import Dict, List
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers import report_controller
from dash.dependencies import Input, Output
from app import app

pg_id = 'train-report'

success, body = report_controller.load_model_list()

files = body if success else []


def on_load():
    global files

    success, body = report_controller.load_model_list()
    if success:
        files = body

    return files


def get_filter(key: str, filters: Dict, styles: List, className: str, options: List):
    values = filters.get(key)

    className: List = className.split(' ') if className is not None else []

    if values:
        if 'hide' in className:
            className.remove('hide')

        options.append(generate_list_items(values, add_all=True))
    else:
        if 'hide' not in className:
            className.append('hide')
        options.append([])

    styles.append(''.join(className))

    return styles, options


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

    if model_name != -1:
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

            styles, options = get_filter('is_delayed', filters, styles, is_delayed_classname, options)
            styles, options = get_filter('order_status', filters, styles, order_status_classname, options)
            styles, options = get_filter('product_category_name', filters, styles, product_category_name_classname, options)
            styles, options = get_filter('seller_id', filters, styles, seller_id_classname, options)
            styles, options = get_filter('type', filters, styles, type_classname, options)

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df['date'], y=df['real'], name='Real', mode='lines'))

            if df['type'].nunique() > 1:
                df = df.sort_values('date')
                first = df[df['type'] == 'test'].head(1)
                first['type'] = 'train'
                df = pd.concat([df, first])
                df = df.sort_values('date')

            groups = list(enumerate(df.groupby('type')))
            for i, group in groups:
                g_info, df_g = group
                fig.add_trace(go.Scatter(x=df_g['date'], y=df_g['predicted'], name=g_info.capitalize(), mode='lines'))

        else:
            styles, options = fill_output(is_delayed_classname, order_status_classname,
                                          product_category_name_classname, seller_id_classname, type_classname)

    else:
        styles, options = fill_output(is_delayed_classname, order_status_classname,
                                      product_category_name_classname, seller_id_classname, type_classname)

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
        Dropdown(id=f'{pg_id}-report-list', label='Modelo', value=-1, options=files, optionHeight=65),
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


def fill_output(is_delayed_classname, order_status_classname, product_category_name_classname, seller_id_classname, type_classname):
    styles = [
        is_delayed_classname,
        order_status_classname,
        product_category_name_classname,
        seller_id_classname,
        type_classname, ]
    options = [[]] * 5
    return styles, options
