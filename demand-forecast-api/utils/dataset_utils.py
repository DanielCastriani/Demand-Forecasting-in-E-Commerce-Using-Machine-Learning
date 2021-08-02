

from utils.config_utils import get_configs
import pandas as pd

def load_dataset() -> pd.DataFrame:
    hdfs_url: str = get_configs('hdfs')

    df = pd.read_parquet(f'{hdfs_url}/dataset.parquet')

    df['date'] = pd.to_datetime(df['date'])

    return df