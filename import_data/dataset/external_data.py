
import pandas as pd
from constants.consts import str_month_int
from constants.urls import DOLLAR_URL, IPCA_URL
from utils.http_utils import download_json_if_not_exist


def load_ipca(path: str = './data/') -> pd.DataFrame:
    json = download_json_if_not_exist(IPCA_URL, path=path, file_name='ipca.json')
    ipca = pd.DataFrame(json[1:])
    ipca_df = ipca.apply(lambda r: pd.Series(r['D3N'].split(' ') + [r['V']],
                                             index=['m', 'y', 'ipca']), axis=1)
    ipca_df['y'] = ipca_df['y'].astype(int)
    ipca_df['m'] = ipca_df['m'].apply(lambda x: str_month_int[x])

    ipca_df['ipca'] = ipca_df['ipca'].astype(float)
    return ipca_df


def load_dollar(path: str = './data/') -> pd.DataFrame:
    json = download_json_if_not_exist(DOLLAR_URL, path=path, file_name='dollar.json')

    dollar_df = pd.DataFrame(json[1:])
    dollar_df['data'] = dollar_df['data'].apply(lambda x: pd.to_datetime(x))

    idx = pd.date_range(dollar_df['data'].min(), dollar_df['data'].max())
    dollar_df = dollar_df.set_index('data')
    dollar_df = dollar_df.reindex(idx)

    dollar_df['valor'] = dollar_df['valor'].fillna(method='ffill')

    dollar_df = dollar_df.reset_index()

    dollar_df.columns = ['date', 'dollar']

    dollar_df['dollar'] = dollar_df['dollar'].astype(float)

    return dollar_df
