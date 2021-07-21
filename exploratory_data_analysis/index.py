import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from routes.main_routes import main_routes

from app import app


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    route = next((c for c in main_routes if c['url'] == pathname), None)

    if route:
        return route['app']
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
