import tensorflow as tf
import os
from .generator import Generator
from .discriminator import Discriminator
from .reader import Reader


class CycleGAN:
    def __init__(self,
                 X_train_file='',
                 Y_train_file='',
                 batch_size=1,
                 image_size=256,
                 use_lsgan=True,
                 norm='instance',
                 lambda1=10,
                 lambda2=10,
                 learning_rate=2e-4,
                 beta1=0.5,
                 ngf=64):
        """
        :param X_train_file: string, X tfrecords file for train
        :param Y_train_file: string, Y tfrecords file for train
        :param batch_size: integer, batch size
        :param image_size: integer, image size
        :param use_lsgan: boolean
        :param norm: 'instance' or 'batch'
        :param lambda1: integer, weight for forward cycle loss (X->Y->X)
        :param lambda2: integer, weight for backward cycle loss (Y->X->Y)
        :param learning_rate:
        :param beta1: momentum term of Adam
        :param ngf: number of gen filters in first conv layer
        """
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.use_lsgan = use_lsgan
        use_sigmoid = not use_lsgan
        self.batch_size = batch_size
        self.image_size = image_size
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.X_train_file = X_train_file
        self.Y_train_file = Y_train_file

        self.is_training = tf.placeholder_with_default(True, shape=[], name='is_training')

        self.G = Generator('G', self.is_training, ngf=ngf, norm=norm, image_size=image_size)
        self.D_Y = Discriminator('D_Y', self.is_training, norm=norm, use_sigmoid=use_sigmoid)
        self.F = Generator('F', self.is_training, ngf=ngf, norm=norm, image_size=image_size)
        self.D_X = Discriminator('D_X', self.is_training, norm=norm, use_sigmoid=use_sigmoid)

        self.fake_x = tf.placeholder(tf.float32, shape=[batch_size, image_size, image_size, 3])
        self.fake_y = tf.placeholder(tf.float32, shape=[batch_size, image_size, image_size, 3])

    def model(self):
        X_reader = Reader(self.X_train_file, name='X',
                          image_size=self.image_size, batch_size=self.batch_size)
        Y_reader = Reader(self.Y_train_file, name='Y',
                          image_size=self.image_size, batch_size=self.batch_size)

        x = X_reader.feed()
        y = Y_reader.feed()

    def optimize(self):
        pass

    def discriminator_loss(self):
        pass

    def generator_loss(self):
        pass

    def cycle_consistency_loss(self):
        pass