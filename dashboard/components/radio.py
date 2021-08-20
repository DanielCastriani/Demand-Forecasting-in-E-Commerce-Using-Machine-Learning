from typing import List
import dash_core_components as dcc
from future.utils import listitems


def RadioList(id: str, options: List[listitems], value: str = None, horizontal: bool = True):
    labelStyle = {
        'marginRight': 16,
        'color': '#fff'
    }
    return dcc.RadioItems(
        id=id,
        options=options,
        value=value,
        labelStyle={'display': 'inline-block', **labelStyle} if horizontal else labelStyle,
        inputStyle={'marginRight': 4}
    )
