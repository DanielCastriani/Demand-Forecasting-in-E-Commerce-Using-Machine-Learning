from typing import List
from typehint import ListItem


def generate_list(values: List[str]):
    return [ListItem(value=x, label=x.replace('_', ' ').capitalize()) for x in values]


def agg_mode_list():
    return [
        ListItem(value='y', label='Ano'),
        ListItem(value='m', label='Mês'),
        ListItem(value='w', label='Semana'),
        ListItem(value='d', label='Dia'),
    ]
