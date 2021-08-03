
from utils.file_utils import create_path_if_not_exists
from utils.report_utils import save_report
from configs.neural_network import create_model
import json

from configs.feature_config import config_list
from feature_engineering.make_features import make_features
from utils.config_utils import get_configs
from utils.dataset_utils import load_dataset
from utils.loggin_utils import get_loggin, timer
from utils.model_utils import create_model_folder, grid_search_keras
from utils.split_utils import split_pipeline

from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras import backend as K


def train_neural_network():
    test_date = '2018-05-01'

    console = get_loggin()
    console.info(json.dumps(get_configs(), indent=4))

    grid_parameters = {
        'model': ['a', 'a2', 'b', 'b2', 'c', 'd'],
        'lr': [.001, .0001],
        'batch_size': [64],
        'epochs': [100, 150, 200],
    }

    with timer(loggin_name='train', message_prefix=f'Train Neural Netwrok'):
        for config in config_list:
            model_name, model_path = create_model_folder(config, regressor_name='NeuralNetwork')

            with timer(loggin_name='train', message_prefix=f'train {model_name}'):
                dataset = load_dataset()
                dataset, numeric_columns = make_features(dataset, config=config)

                train_keys, test_keys, x_train, y_train, x_test, y_test = split_pipeline(
                    test_date,
                    config,
                    model_path,
                    dataset,
                    numeric_columns)

                best, error_df = grid_search_keras(
                    grid_parameters=grid_parameters,
                    x_train=x_train,
                    y_train=y_train,
                    x_test=x_test,
                    y_test=y_test)

                error_df.to_csv(create_path_if_not_exists(model_path, filename=f'grid_search.csv'), index=False)

                tensorboard_callback = TensorBoard(
                    log_dir=create_path_if_not_exists(model_path, 'tensorboard'),
                    write_graph=True)

                model = create_model(len(x_train.columns), config=best['model'], lr=best['lr'])
                model.fit(
                    x_train, y_train, validation_data=(x_test, y_test),
                    batch_size=best['batch_size'],
                    epochs=best['epochs'],
                    callbacks=[tensorboard_callback])

                model.save(create_path_if_not_exists(model_path, 'model'))

                save_report(
                    model_path=model_path,
                    train_keys=train_keys,
                    test_keys=test_keys,
                    x_train=x_train,
                    y_train=y_train,
                    x_test=x_test,
                    y_test=y_test,
                    model=model,
                )

                del model
                K.clear_session()


if __name__ == '__main__':
    train_neural_network()
