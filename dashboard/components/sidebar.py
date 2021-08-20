
from typing import List

from typehint.route_types import Route

from components.menu import MenuItem


def SideBar(main_routes: List[Route]):

    return [MenuItem(r) for r in main_routes if r['show_menu']]
