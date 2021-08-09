from typing import Literal
from tensorflow.keras.layers import Input, Dense, LSTM
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam


def config_a(input: Input):
    x = LSTM(128)(input)
    x = Dense(128, activation='relu')(x)
    return x


def config_b(input: Input):
    x = LSTM(128, return_sequences=True)(input)
    x = LSTM(128)(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)

    return x


def config_c(input: Input):
    x = LSTM(256, return_sequences=True)(input)
    x = LSTM(256)(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    return x


configs = {
    'a': config_a,
    'b': config_b,
    'c': config_c,
}


def create_lstm_model(input_len: int, config: Literal['a', 'b', 'c'], lr: float):
    hidden_layer = configs.get(config, config_a)

    input = Input(shape=(input_len, 1))
    x = hidden_layer(input)
    outputs = Dense(1)(x)

    model = Model(inputs=[input], outputs=outputs)

    optimizer = Adam(learning_rate=lr)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse', 'mape'])
    return model
