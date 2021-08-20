
from typing import List

from pages import (
    forecast_page,
    index,
    lag_correlation,
    mean_by_date,
    performace_report_page,
    price_x_ext_data_page,
    report_page,
    var_correlation,
    data_summary_page)

from typehint import Route

main_routes: List[Route] = [
    Route(url='/', title='Index', app=index.layout, show_menu=False),
    Route(url='/data_summary_page', title='Sumário', app=data_summary_page.layout, show_menu=True, icon='fa-chart-area'),
    Route(url='/mean_by_date', title='Média Por Dia', app=mean_by_date.layout, show_menu=True, icon='fa-calendar'),
    Route(
        url='/price_x_external', title='Preço x Dados Externos', app=price_x_ext_data_page.layout, show_menu=True,
        icon='fa-external-link-square-alt'),
    Route(
        url='/var_correlation', title='Correlação entre Variáveis', app=var_correlation.layout, show_menu=True, icon='fa-chart-bar'),
    Route(url='/lag_correlation', title='Correlação Atrasada', app=lag_correlation.layout, show_menu=True, icon='fa-history'),
    Route(
        url='/performace_report_page', title='Relatório de Performance', app=performace_report_page.layout, show_menu=True,
        icon='fa-table'),
    Route(url='/model_train_report', title='Relatório de Treino', app=report_page.layout, show_menu=True, icon='fa-file-excel'),
    Route(url='/forecast_page', title='Previsão de Demanda', app=forecast_page.layout, show_menu=True, icon='fa-chart-line'), ]
