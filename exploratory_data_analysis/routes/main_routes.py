
from typing import List
from typehint import Route

from pages import index, var_correlation


main_routes: List[Route] = [
    Route(url='/', title='', app=index.layout),
    Route(url='/var_correlation', title='Correlação entre Variáveis', app=var_correlation.layout),
]
