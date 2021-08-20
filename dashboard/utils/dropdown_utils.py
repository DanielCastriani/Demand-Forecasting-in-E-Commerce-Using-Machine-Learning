from typing import List
from typehint import ListItem


def generate_list_items(values: List[str], add_all: bool = False):
    arr = [ListItem(value=x, label=str(x).replace('_', ' ').capitalize()) for x in values]

    arr = [ListItem(label=i['label'], value=str(i['value']))
           if isinstance(i['value'], bool) else i for i in arr]

    if add_all:
        return[ListItem(value=-1, label='Todos'), *arr]

    return arr


def agg_mode_list():
    return [
        ListItem(value='y', label='Ano'),
        ListItem(value='m', label='Mês'),
        ListItem(value='w', label='Semana'),
        ListItem(value='d', label='Dia'),
    ]
