from typehint import Route
import dash_html_components as html


def MenuItem(route: Route):
    className = ['menu-item']

    if route.get('is_active', False):
        className.append('menu-active')

    return html.A(route['title'], href=route['url'], className=' '.join(className))
