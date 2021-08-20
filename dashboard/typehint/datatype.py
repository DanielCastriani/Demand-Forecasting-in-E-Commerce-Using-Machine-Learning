from typing import Any, Literal, TypedDict, Union


Number = Union[int, float]

AggregationMode = Literal['y', 'm', 'w', 'd']


class ListItem(TypedDict):
    label: str
    value: Any
