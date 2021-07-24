import dash_html_components as html


def TopBar():
    return html.Nav([
        html.Div([
            html.H6('Dashboard')
        ]),

    ], className="top-menu-container")
