import dash_html_components as html


def TopBar():
    return html.Nav([
        html.Div(
            html.I(className='fas fa-bars white-icon'),
            id='menu-button', className='fab', n_clicks=0),

        html.H6('Dashboard', className='title')

    ], className="top-menu-container")
