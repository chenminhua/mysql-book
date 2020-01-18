import tflearn
from tflearn.layers.core import input_data
from tflearn.layers.conv import conv_2d, max_pool_2d

def convnet():
    net = input_data(shape=[None, 28, 28, 1])
    net = conv_2d(net, 32, 1, activation='relu')