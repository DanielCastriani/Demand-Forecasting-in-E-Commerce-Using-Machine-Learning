from typing import List
import dash_core_components as dcc
from typehint import ListItem


def Checklist(id: str, options: List[ListItem], value: List[str] = [], horizontal: bool = False):
    labelStyle = {'display': 'inline-block'} if horizontal else {}
    labelStyle['color'] = '#fff'

    return dcc.Checklist(
        id=id,
        options=options,
        value=value,
        labelStyle=labelStyle,
        inputStyle={'marginRight': '8px'},
    )
