
from typing import List
from typehint import Route

from pages import index, var_correlation


main_routes: List[Route] = [
    Route(url='/', title='Index', app=index.layout, show_menu=False),
    Route(url='/var_correlation', title='Correlação entre Variáveis', app=var_correlation.layout, show_menu=True),
]
