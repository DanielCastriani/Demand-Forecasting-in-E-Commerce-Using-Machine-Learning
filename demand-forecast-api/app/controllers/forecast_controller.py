from app.utils.df_utils import apply_filter
import pandas as pd
from app.controllers import model_controller
from app.dtos.forecast_dtos import ForecastRequestDTO
from model.forecast.sk_learn_forecast import forecast
from utils.dataset_utils import load_dataset


def filter_active_products(dataset: pd.DataFrame, days: int):
    last_date_sold = dataset.groupby('product_id')['date'].max()

    # Simulate current date since the dataset have dates from past
    curr_date = last_date_sold.max()

    last_date_sold = last_date_sold[(curr_date - last_date_sold).dt.days >= days]
    product_id_list = last_date_sold.index.unique().tolist()

    dataset = dataset[dataset['product_id'].isin(product_id_list)]

    
    count_sales = dataset['product_category_name'].value_counts()
    # More then 180 registers of sales
    cat_id = count_sales[count_sales > 180]
    cat_id = cat_id.index.unique().tolist()
    dataset = dataset[dataset['product_category_name'].isin(cat_id)]
    
    return dataset


def make_forecast(body: ForecastRequestDTO):

    dataset = load_dataset()
    config = model_controller.get_config(body['model_name'])

    dataset = filter_active_products(dataset, days=90)
    
    filters = {c: sorted(dataset[c].unique().tolist()) for c in config['keys']}

    dataset = apply_filter(body, dataset)

    if len(dataset):
        result_df, agg_mode = forecast(config=config, dataset=dataset, body=body)

    if result_df is not None:
        result_df['date'] = result_df['date'].apply(lambda s: s.strftime('%Y-%m-%d'))
        result_dict = result_df.to_dict(orient='records')
        return result_dict, filters, agg_mode

    return None, None


if __name__ == '__main__':
    pd.options.display.max_columns = None
    pd.options.display.expand_frame_repr = None

    body = ForecastRequestDTO(
        model_name='LSTM_w_2',
        window_size=3,
        # product_category_name='utilidades_domesticas',
        # order_status='shipped'
    )

    result_dict, filters = make_forecast(body)

    result = pd.DataFrame()
    print(result.head(20))
