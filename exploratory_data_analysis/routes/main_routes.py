
from typing import List
from typehint import Route

from pages import index, var_correlation, lag_correlation, mean_by_date, report_page


main_routes: List[Route] = [
    Route(url='/', title='Index', app=index.layout, show_menu=False),
    Route(url='/var_correlation',    title='Correlação entre Variáveis', app=var_correlation.layout, show_menu=True, icon='fa-chart-bar'),
    Route(url='/lag_correlation',    title='Correlação Atrasada', app=lag_correlation.layout, show_menu=True, icon='fa-history'),
    Route(url='/mean_by_date',       title='Preço x Dados Externos', app=mean_by_date.layout, show_menu=True, icon='fa-chart-line'),
    Route(url='/model_train_report', title='Relatório de Treino', app=report_page.layout, show_menu=True, icon='fa-file-excel', on_load_callback =report_page.on_load),
]
