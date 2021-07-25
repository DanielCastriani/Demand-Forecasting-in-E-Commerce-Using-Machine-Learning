from components.topbar import TopBar
import os
from components.sidebar import SideBar
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from routes.main_routes import main_routes
from flask import send_from_directory

from app import app


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    TopBar(),
    html.Div([], id='side-bar', className='side-bar-container'),

    html.Div(id='page-content', className='content'),
], className='main-container')


@app.server.route('/public/<path:path>')
def static_files(path):
    static_folder = os.path.join(os.getcwd(), 'public')
    return send_from_directory(static_folder, path)


@app.callback([
    Output('side-bar', 'children'),
    Output('page-content', 'children'),
],
    Input('url', 'pathname'))
def display_page(pathname):
    route = next((c for c in main_routes if c['url'] == pathname), None)

    side_menu_path = [{**m, 'is_active': True} if m['url'] == pathname else m for m in main_routes]

    side_menu = SideBar(side_menu_path)

    if route:
        return side_menu, route['app']
    else:
        return side_menu, '404'


if __name__ == '__main__':
    app.run_server(debug=True)
