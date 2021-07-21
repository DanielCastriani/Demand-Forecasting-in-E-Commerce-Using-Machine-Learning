from typing import TypedDict
from dash.development.base_component import Component



class Route(TypedDict):
    url: str
    title: str
    app: Component
