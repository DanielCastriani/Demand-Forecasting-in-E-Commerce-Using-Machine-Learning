import dash_html_components as html
import re


def Card(id: str, title: str, value: str, precision: int = 2, prefix: str = ''):
    if isinstance(value, int):
        str_value = '{:,d}'.format(value)

    elif isinstance(value, float):
        mask = '{:,.'+str(precision)+'f}'
        str_value = mask.format(value)

    else:
        str_value = str(value)

    str_value = f'{prefix}{str_value}'

    return html.Div([
        html.P(title, className='card-title', id=f'{id}-title'),
        html.P(str_value, className='card-value', id=f'{id}-value'),
    ], className='card', id=id)
