import dash_html_components as html
import dash_core_components as dcc

from components.containers import Content, FilterContainer
from components.dropdown import Dropdown
from components.slider import Slider












layout = html.Div([
    FilterContainer([
    ]),

    Content([
    ])
],  className='content-container')