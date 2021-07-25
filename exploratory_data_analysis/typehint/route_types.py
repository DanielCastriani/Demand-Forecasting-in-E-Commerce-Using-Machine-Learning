from typing import Optional, TypedDict
from dash.development.base_component import Component


class Route(TypedDict):
    url: str
    title: str
    app: Component
    is_active: Optional[bool]
    show_menu: bool
    icon: Optional[str]
