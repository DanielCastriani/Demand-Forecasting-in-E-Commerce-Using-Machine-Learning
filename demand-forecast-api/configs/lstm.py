from typing import Literal
from tensorflow.keras.layers import Input, Dense, LSTM, Dropout
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam


def config_a(input: Input):
    x = LSTM(96)(input)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)

    return x


def config_b(input: Input):
    x = LSTM(96)(input)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)

    return x


def config_c(input: Input):
    x = LSTM(64, return_sequences=True)(input)
    x = LSTM(64)(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)

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
