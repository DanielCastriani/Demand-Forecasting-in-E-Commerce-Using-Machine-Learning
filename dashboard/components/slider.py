from typing import Any, Dict

import dash_core_components as dcc
import numpy as np
from dash.development.base_component import Component
from typehint.datatype import Number


def Slider(
        id: str,
        value: Number = Component.UNDEFINED,
        min: Number = Component.UNDEFINED,
        max: Number = Component.UNDEFINED,
        steps: int = 5,
        marks: Dict[Any, str] = Component.UNDEFINED):

    if marks and min and max and steps:
        marks = {
            str(x): str(x)
            for x in np.arange(min, max, steps)
        }

        marks[str(max)] = str(max)

    return dcc.Slider(id=id, min=min, max=max, value=value, marks=marks, tooltip={'always_visible': False})
