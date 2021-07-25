from typing import List, Union
from dash.development.base_component import Component
import dash_html_components as html


def FilterContainer(children: Union[Component, List[Component]]):

    return html.Div(children, className='filter-container padding-container')


def Content(children: Union[Component]):

    return html.Div(children, className='padding-container')
