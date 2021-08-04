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

    html.Div([
        html.Div([], id='side-bar-menu', className='side-bar-menu-container hide-side-menu'),
        html.Div(id='page-content', className='content'),

    ], className='content-container'),

], className='main-container')


@app.callback(Output('side-bar-menu', 'className'), [Input('side-bar-menu', 'className'), Input('menu-button', 'n_clicks')])
def toggle_menu(className: str, n_clicks):
    class_list = className.split(' ')

    if n_clicks > 0:
        hide_className = 'hide-side-menu'

        if hide_className in class_list:
            class_list.remove(hide_className)
        else:
            class_list.append(hide_className)

    return ' '.join(class_list)


@app.server.route('/public/<path:path>')
def static_files(path: str):
    static_folder = os.path.join(os.getcwd(), 'public')
    return send_from_directory(static_folder, path)


@app.callback([Output('side-bar-menu', 'children'), Output('page-content', 'children')], Input('url', 'pathname'))
def display_page(pathname):
    route = next((c for c in main_routes if c['url'] == pathname), None)

    side_menu_path = [{**m, 'is_active': True} if m['url'] == pathname else m for m in main_routes]

    side_menu = SideBar(side_menu_path)

    if route:
        on_load = route.get('on_load_callback')
        if on_load:
            on_load()

        return side_menu, route['app']
    else:
        return side_menu, '404'


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
