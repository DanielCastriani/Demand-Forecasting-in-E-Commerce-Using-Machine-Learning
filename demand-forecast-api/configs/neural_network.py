from typing import Literal
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam


def config_a(input: Input):
    x = Dense(64, activation='relu')(input)
    x = Dense(64, activation='relu')(x)
    return x


def config_a2(input: Input):
    x = Dense(64, activation='tanh')(input)
    x = Dense(64, activation='tanh')(x)
    return x


def config_b(input: Input):
    x = Dense(64, activation='relu')(input)
    x = Dense(64, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    return x


def config_b2(input: Input):
    x = Dense(64, activation='tanh')(input)
    x = Dense(64, activation='tanh')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    return x


def config_c(input: Input):
    x = Dense(64, activation='relu')(input)
    x = Dense(64, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    return x


def config_d(input: Input):
    x = Dense(256, activation='relu')(input)
    x = Dense(256, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    return x


configs = {
    'a': config_a,
    'a2': config_a2,
    'b': config_b,
    'b2': config_b2,
    'c': config_c,
    'd': config_d,
}


def create_neural_network_model(input_len: int, config: Literal['a', 'b', 'c'], lr: float):
    hidden_layer = configs.get(config, config_a)

    input = Input(shape=(input_len))
    x = hidden_layer(input)
    outputs = Dense(1)(x)

    model = Model(inputs=[input], outputs=outputs)

    optimizer = Adam(learning_rate=lr)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse', 'mape'])
    return model
