import dash_html_components as html
from dash_table import DataTable
from components.containers import Content
from controllers import report_controller
from app import app
from dash.dependencies import Input, Output

pg_id = 'performace-report'


@app.callback([
    Output(f'{pg_id}-report', 'columns'),
    Output(f'{pg_id}-report', 'data'),
], Input('url', 'pathname'))
def on_load(_: str):
    performance_result = report_controller.performance_report()
    performance_result_keys = list(performance_result[0].keys()) if len(performance_result) > 0 else []
    performance_result_cols = [{'name': c, 'id': c} for c in performance_result_keys]

    return performance_result_cols, performance_result


layout = html.Div([
    Content([
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
            ),
            style={'padding': 16}
        )
    ])
],  className='content-container')
