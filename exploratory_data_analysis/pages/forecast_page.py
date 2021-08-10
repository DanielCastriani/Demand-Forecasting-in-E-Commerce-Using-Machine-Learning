import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from components.slider import Slider
from controllers import forecast_controller, report_controller
from dash.dependencies import Input, Output
from dash_table import DataTable
from utils.df_utils import concat_lines
from utils.filter_utils import forecast_filter, forecast_filter_fill_output

pg_id = 'forecast-page'


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

    Output(f'{pg_id}-report', 'columns'),
    Output(f'{pg_id}-report', 'data'),

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
    Input(f'{pg_id}-window', 'value'),
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

    window: int

):
    fig = go.Figure()

    fill_filters = model_name == -1

    forecast_table_cols = []
    forecast_table_data = []

    if not fill_filters:

        success, df, filters = forecast_controller.make_forecast(
            model_name=model_name,
            is_delayed=is_delayed,
            order_status=order_status,
            product_category_name=product_category_name,
            seller_id=seller_id,
            datatype=datatype,
            window_size=window
        )

        styles = []
        options = []

        if success:
            fill_filters = False
            styles, options = forecast_filter(
                is_delayed_classname,
                order_status_classname,
                product_category_name_classname,
                seller_id_classname,
                type_classname,
                filters,
                styles,
                options)

            values = [c for c in df.columns if 'qty' in c]
            df_plot = df.pivot_table(values, index=['type', 'date'], aggfunc='sum')
            df_plot = df_plot.reset_index()

            df_plot = concat_lines(df_plot, g1='real', g2='forecast')

            groups = list(enumerate(df_plot.groupby('type')))
            for i, group in groups:
                g_info, df_g = group
                fig.add_trace(go.Scatter(x=df_g['date'], y=df_g['qty'], name=g_info.capitalize(), mode='lines'))

            forecast_table_cols = [{'name': c, 'id': c, 'presentation': 'markdown'} for c in df.columns]
            forecast_table_data = df.to_dict(orient='records')

            for item in forecast_table_data:
                for i in range(1, len(values)):
                    ca, cb = values[i-1], values[i]
                    if item[ca] < item[cb]:
                        item[ca] = f'![Decreased](public/img/chevron-down-solid.svg) {item[ca]}'
                    elif item[ca] > item[cb]:
                        item[ca] = f'![Increased](public/img/chevron-up-solid.svg) {item[ca]}'
                    else:
                        item[ca] = f'![Equal](public/img/equals-solid.svg) {item[ca]}'

    if fill_filters:
        styles, options = forecast_filter_fill_output(
            is_delayed_classname,
            order_status_classname,
            product_category_name_classname,
            seller_id_classname,
            type_classname)

    fig.update_layout(
        template='plotly_dark',
        title="Previsão de Demanda (soma)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        transition={"duration": 300})

    return [fig, *styles, *options, forecast_table_cols, forecast_table_data]


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
        Slider(id=f'{pg_id}-window', value=4, min=1, max=12),
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        ),


        html.Div(

            DataTable(
                id=f'{pg_id}-report',
                columns=[],
                data=[],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                page_action="native",
                page_current=0,
                page_size=20,
                style_cell={'textAlign': 'left'},
            ),
            style={'margin': "32px 16px 88px 16px"}
        )
    ])
],  className='content-container')
