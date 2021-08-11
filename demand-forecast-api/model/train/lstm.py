
import tensorflow as tf
from configs.feature_config import config_list
from configs.lstm import create_lstm_model
from configs.neural_network import create_neural_network_model
from feature_engineering.make_features import make_features
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from utils.config_utils import get_config
from utils.dataset_utils import load_dataset
from utils.file_utils import create_path_if_not_exists
from utils.loggin_utils import get_loggin, timer
from utils.model_utils import create_model_folder, grid_search_keras
from utils.report_utils import save_report
from utils.split_utils import split_pipeline


def lstm():
    test_date = '2018-05-01'

    console = get_loggin()
    console.info(f'N_JOBS: {get_config("N_JOBS")}')

    grid_parameters = {
        'model': ['b', 'a'],
        'lr': [.00001],
        'batch_size': [96],
        'epochs': [250],
    }

    with timer(loggin_name='train', message_prefix=f'LSTM') as console:
        console.info(f'GPU: {tf.test.is_gpu_available()}')
        for config in config_list:
            model_name, model_path = create_model_folder(config, regressor_name='LSTM')
            console.info(f'{model_name}')

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
                    create_model_callback=create_lstm_model,
                    grid_parameters=grid_parameters,
                    x_train=x_train,
                    y_train=y_train,
                    x_test=x_test,
                    y_test=y_test)

                error_df.to_csv(create_path_if_not_exists(model_path, filename=f'grid_search.csv'), index=False)

                tensorboard_callback = TensorBoard(
                    log_dir=create_path_if_not_exists(model_path, 'tensorboard'),
                    write_graph=True)

                early_stopping = EarlyStopping(
                    monitor='loss',
                    patience=15,
                    min_delta=0.001,
                    restore_best_weights=True
                )

                model = create_lstm_model(len(x_train.columns), config=best['model'], lr=best['lr'])
                model.fit(
                    x_train, y_train, validation_data=(x_test, y_test),
                    batch_size=best['batch_size'],
                    epochs=best['epochs'],
                    callbacks=[tensorboard_callback, early_stopping])

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
    lstm()
