from typing import Callable, Optional, TypedDict
from dash.development.base_component import Component


class Route(TypedDict):
    url: str
    title: str
    app: Component
    is_active: Optional[bool]
    show_menu: bool
    icon: Optional[str]
    on_load_callback: Optional[Callable]
