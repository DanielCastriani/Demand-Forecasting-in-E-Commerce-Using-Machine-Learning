
from typing import Any, List

import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component
from typehint.datatype import ListItem


def Dropdown(
        id: str, value: Any = Component.UNDEFINED, options: List[ListItem] = [],
        clearable=False, label: str = '', optionHeight: int = 35, visible: bool = True):

    className = ''

    if not visible:
        className = f'hide {className}'

    return html.Div([
        
        html.P(label, className='label'),

        dcc.Dropdown(
            id=id,
            value=value,
            options=options,
            clearable=clearable,
            optionHeight=optionHeight,
        )

    ], id=f'{id}-div', style={'marginBottom': 16}, className=className)
