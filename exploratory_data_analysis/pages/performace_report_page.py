import dash_html_components as html
from dash_table import DataTable
from components.containers import Content
from controllers import report_controller

pg_id = 'performace-report'


performance_result = report_controller.performance_report()
performance_result_keys =  list(performance_result[0].keys()) if len(performance_result)> 0 else []
performance_result_cols= [{'name': c, 'id': c} for c in performance_result_keys]


layout = html.Div([
    Content([
        html.Div(

            DataTable(
                id=f'{pg_id}-report', 
                columns=performance_result_cols, 
                data=performance_result),
            style={'padding': 16}
        )
    ])
],  className='content-container')
