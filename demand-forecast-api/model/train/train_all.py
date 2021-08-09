from utils.loggin_utils import timer
from model.train.lstm import lstm
from model.train.knn import train_knn
from model.train.neural_network import train_neural_network
from model.train.rfr import train_tree

if __name__ == '__main__':

    with timer(loggin_name='train', message_prefix=f'Train ALL'):
        lstm()
        train_neural_network()
        train_tree()
        train_knn()
