from typehint.datatype import ListItem
from typing import Dict, List, Union
from utils.dropdown_utils import generate_list_items

import pandas as pd


def filter_df(df: pd.DataFrame, column: str, value: Union[str, int] = -1):
    if value != -1:
        df = df[df[column] == value]

    return df


def get_report_filter(key: str, filters: Dict, styles: List, className: str, options: List):
    values = filters.get(key)

    className: List = className.split(' ') if className is not None else []

    if values:
        if 'hide' in className:
            className.remove('hide')

        options.append(generate_list_items(values, add_all=True))
    else:
        if 'hide' not in className:
            className.append('hide')
        options.append([])

    styles.append(''.join(className))

    return styles, options


def forecast_filter(
        is_delayed_classname: str,
        order_status_classname: str,
        product_category_name_classname: str,
        seller_id_classname: str,
        type_classname: str,
        filters: Dict[str, List],
        styles: List[str],
        options: List[ListItem]):
    styles, options = get_report_filter('is_delayed', filters, styles, is_delayed_classname, options)
    styles, options = get_report_filter('order_status', filters, styles, order_status_classname, options)
    styles, options = get_report_filter('product_category_name', filters, styles, product_category_name_classname, options)
    styles, options = get_report_filter('seller_id', filters, styles, seller_id_classname, options)
    styles, options = get_report_filter('type', filters, styles, type_classname, options)

    return styles, options


def forecast_filter_fill_output(
        is_delayed_classname: str,
        order_status_classname: str,
        product_category_name_classname: str,
        seller_id_classname: str,
        type_classname: str):
    styles = [
        is_delayed_classname,
        order_status_classname,
        product_category_name_classname,
        seller_id_classname,
        type_classname, ]
    options = [[]] * 5
    return styles, options
