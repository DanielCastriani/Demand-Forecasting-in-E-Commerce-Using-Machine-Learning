
from typing import List

import dash_html_components as html
from dash_html_components.A import A
from dash_html_components.Div import Div
from typehint.route_types import Route

from components.menu import MenuItem


def SideBar(main_routes: List[Route]):

    return [MenuItem(r) for r in main_routes if r['show_menu']]
