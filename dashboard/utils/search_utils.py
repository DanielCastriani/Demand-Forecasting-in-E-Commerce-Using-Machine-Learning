from typing import Any, List
from typehint import ListItem


def find_label(value: Any, filter_list: List[ListItem]):
    return next((c['label'] for c in filter_list if c['value'] == value), '')