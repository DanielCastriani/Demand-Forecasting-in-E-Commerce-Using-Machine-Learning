from app.utils.df_utils import apply_filter
import pandas as pd
from app.controllers import model_controller
from app.dtos.forecast_dtos import ForecastRequestDTO
from model.forecast.sk_learn_forecast import forecast
from utils.dataset_utils import load_dataset


def make_forecast(body: ForecastRequestDTO):

    dataset = load_dataset()
    config = model_controller.get_config(body['model_name'])

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
        model_name='LSTM_w_1',
        window_size=3,
        product_category_name='utilidades_domesticas',
        order_status='shipped'
    )

    result_dict, filters = make_forecast(body)

    result = pd.DataFrame()
    print(result.head(20))
