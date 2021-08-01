import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from controllers.database import load_numeric_column_names
from controllers.variable_correlation_controller import mean_by_cat_date
from dash.dependencies import Input, Output
from utils.dropdown_utils import agg_mode_list, generate_list_items

pg_id = 'external-data'


agg_date_mode_list = agg_mode_list()

numeric_columns = generate_list_items(load_numeric_column_names())


@app.callback(
    Output(f'{pg_id}-chart', 'figure'),
    [
        Input(f'{pg_id}-agg-mode', 'value'),
        Input(f'{pg_id}-variable', 'value'),
    ])
def update_figure(agg_mode: str, feature: str):

    df = mean_by_cat_date(agg_mode, feature)

    fig = go.Figure()

    for i, group in enumerate(df.groupby('product_category_name')):
        g_info, df_g = group
        trace_visible = True if i == 0 else 'legendonly'

        fig.add_trace(go.Scatter(x=df_g['date'], y=df[feature], name=g_info, mode='lines', visible=trace_visible))

    fig.update_layout(template='plotly_dark', title="Correlação entre Variáveis",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      showlegend=True)

    return fig


layout = html.Div([
    FilterContainer([
        Dropdown(id=f'{pg_id}-agg-mode', label='Agregar por', value=agg_date_mode_list[2]['value'], options=agg_date_mode_list),
        Dropdown(id=f'{pg_id}-variable', label='Variável', value=numeric_columns[0]['value'], options=numeric_columns),
    ]),

    Content(
        dcc.Graph(
            id=f'{pg_id}-chart',
            style={'width': '100%', 'height': '90%'},
        )
    )

    # Slider(id='slider', value=30, min=5, max=120)
],  className='content-container')
