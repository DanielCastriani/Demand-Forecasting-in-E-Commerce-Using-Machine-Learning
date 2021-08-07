from model.train.lstm import lstm
from model.train.knn import train_knn
from model.train.neural_network import train_neural_network
from model.train.rfr import train_tree

if __name__ == '__main__':
    train_knn()
    train_tree()
    train_neural_network()
    lstm()
