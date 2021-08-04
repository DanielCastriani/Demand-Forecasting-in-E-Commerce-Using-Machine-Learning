

from utils.config_utils import get_config
import pandas as pd

def load_dataset() -> pd.DataFrame:
    hdfs_url: str = get_config('HDFS')

    df = pd.read_parquet(f'{hdfs_url}/dataset.parquet')

    df['date'] = pd.to_datetime(df['date'])

    return df