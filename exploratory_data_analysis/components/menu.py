from typehint import Route
import dash_html_components as html


def MenuItem(route: Route):
    className = ['menu-item']

    if route.get('is_active', False):
        className.append('menu-active')

    icon = route.get('icon', 'fa-bars')

    return html.A([
        html.I(className=f'fas {icon}', style={'marginRight': '16px'}),
        route['title']
    ], href=route['url'], className=' '.join(className))
