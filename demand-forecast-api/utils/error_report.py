import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
from typehint import ErrorMetrics


def correlation(y_true: pd.Series, y_pred: np.ndarray, verbose: bool = False):
    pearson_correlation, p_value = pearsonr(y_true, y_pred)
    if verbose:
        print(f'corr: {pearson_correlation:.3f}')
        print(f'p_value: {p_value:.3f}')

    return pearson_correlation, p_value


def error_report(y_true: pd.Series, y_pred: np.ndarray, verbose: bool = False):
    mse = mean_absolute_error(y_true, y_pred)
    mae = mean_squared_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    corr, p_value = correlation(y_true, y_pred)

    if verbose:
        print(f'mse: {mse:.3f}')
        print(f'mae: {mae:.3f}')
        print(f'mape: {mape:.3f}')
        print(f'r2: {r2:.3f}')
        print(f'corr: {corr:.3f}')
        print(f'p_value: {p_value:.3f}')

    return ErrorMetrics(mse=mse, mae=mae, mape=mape, r2=r2, corr=corr)
