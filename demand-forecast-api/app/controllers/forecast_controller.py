import pandas as pd
from app.controllers import model_controller
from app.dtos.forecast_dtos import ForecastRequestDTO
from model.forecast.sk_learn_forecast import forecast
from utils.dataset_utils import load_dataset


def make_forecast(body: ForecastRequestDTO):
    dataset = load_dataset()
    config = model_controller.get_config(body['model_name'])

    res = forecast(config=config, dataset=dataset, body=body)

    if res is not None:
        return res.to_dict(orient='records')


if __name__ == '__main__':
    pd.options.display.max_columns = None
    body = ForecastRequestDTO(
        model_name='LSTM_m_1',
        window_size=3
    )

    result = make_forecast(body)
