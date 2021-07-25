from components.containers import Content, FilterContainer
from components.slider import Slider
import dash_core_components as dcc
import dash_html_components as html

from app import app

layout = html.Div([
    FilterContainer([
        html.P('a'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
        html.P('b'),
    ]),

    Content(
        html.P('b'),

    )

    # Slider(id='slider', value=30, min=5, max=120)
],  className='content-container')
