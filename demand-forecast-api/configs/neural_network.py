from typing import Literal
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam


def config_a(input: Input):

    x = Dense(64, activation='tanh')(input)
    x = Dropout(0.2)(x)

    x = Dense(64, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    return x


def config_b(input: Input):
    x = Dense(128, activation='tanh')(input)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)

    return x


def config_c(input: Input):
    x = Dense(128, activation='tanh')(input)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)

    return x


def config_d(input: Input):

    x = Dense(128, activation='tanh')(input)
    x = Dropout(0.2)(x)

    x = Dense(128, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)

    return x


def config_e(input: Input):
    x = Dense(256, activation='tanh')(input)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(256, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(512, activation='tanh')(x)
    x = Dropout(0.2)(x)

    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)

    return x


configs = {
    'a': config_a,
    'b': config_b,
    'c': config_c,
    'd': config_d,
    'e': config_e,
}


def create_neural_network_model(input_len: int, config: Literal['a', 'b', 'c', 'd'], lr: float):
    hidden_layer = configs.get(config, config_a)

    input = Input(shape=(input_len))
    x = hidden_layer(input)
    outputs = Dense(1)(x)

    model = Model(inputs=[input], outputs=outputs)

    optimizer = Adam(learning_rate=lr)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse', 'mape'])
    return model
