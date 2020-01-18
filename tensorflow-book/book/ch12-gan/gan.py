import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("../../data/mnist", one_hot=True)

# imgs_to_show, labels_to_show = mnist.train.next_batch(9)
# plt.figure()
# for i in range(9):
#     plt.subplot(3,3,i+1)
#     plt.imshow(imgs_to_show[i].reshape([28, 28]))
#     plt.title("number {}".format(np.argmax(labels_to_show[i])))
# plt.show()

# train parameters
num_steps = 20000
batch_size = 32

# network parameters
image_size = 784
gen_hidden_dim = 256
disc_hidden_dim = 256
noise_dim = 200

# generator, input noise, output image
def generator(x, reuse=False):
    with tf.variable_scope('Generator', reuse=reuse):
        # tf will automatically create variables and calculate their shape, based on the input
        x = tf.layers.dense(x, units=6 * 6 * 128)
        x = tf.nn.tanh(x)
        # reshape to a 4-D array of images: (batch, height, width, channels), height = width = 6
        x = tf.reshape(x, shape=[-1, 6, 6, 128])
        # deconvolution to (batch, 14, 14, 64)
        # deprecated, use tf.keras.layers.Conv2DTranspose instead.
        # 卷积核中的in_channels 与需要进行卷积操作的数据的 channels 是一样的。
        x = tf.layers.conv2d_transpose(x, 64, 4, strides=2)   
        # deconvolution to (batch, 28, 28, 1)
        x = tf.layers.conv2d_transpose(x, 1, 2, strides=2)
        # apply sigmoid to clip values between 0 and 1
        return tf.nn.sigmoid(x)

# discriminator, input image, output prediction Real/Fake
def discriminator(x, reuse=False):
    with tf.variable_scope('Discriminator', reuse=reuse):
        x = tf.layers.conv2d(x, 64, 5)
        x = tf.nn.tanh(x)
        x = tf.layers.average_pooling2d(x, 2, 2)
        x = tf.layers.conv2d(x, 128, 5)
        x = tf.nn.tanh(x)
        x = tf.layers.average_pooling2d(x, 2, 2)
        x = tf.contrib.layers.flatten(x)
        x = tf.layers.dense(x, 1024)
        x = tf.nn.tanh(x)
        x = tf.layers.dense(x, 2)
    return x

# build network
## placeholder
noise_input = tf.placeholder(tf.float32, shape=[None, noise_dim])
real_image_input = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])

## generator network
gen_sample = generator(noise_input)

## build 2 discriminator network, one from real input, one from generated samples
disc_real = discriminator(real_image_input)
disc_fake = discriminator(gen_sample, reuse=True)   # notice this reuse
disc_concat = tf.concat([disc_real, disc_fake], axis=0)

# build the stacked  (generator / discriminator)
stacked_gan = discriminator(gen_sample, reuse=True) # notice this reuse

# build targets (real or fake image)
disc_target = tf.placeholder(tf.int32, shape=[None])
gen_target = tf.placeholder(tf.int32, shape=[None])

# loss
disc_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=disc_concat, labels=disc_target))
gen_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=stacked_gan, labels=gen_target))

# optimizer
optimizer_gen = tf.train.AdamOptimizer(0.001)
optimizer_disc = tf.train.AdamOptimizer(0.001)

# traning varialbes for each optimizer
# by default in tf, all variables are updated by each optimizer, 
# so we need to precise for each one the specific variable to update.
gen_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Generator')
disc_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Discriminator')

# train operations
train_gen = optimizer_gen.minimize(gen_loss, var_list=gen_vars)
train_disc = optimizer_disc.minimize(disc_loss, var_list=disc_vars)

# initialize the variables
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# train!!
for i in range(1, num_steps+1):
    batch_x, _ = mnist.train.next_batch(batch_size)
    batch_x = np.reshape(batch_x, newshape=[-1, 28, 28, 1])
    # generate noise to feed to generator
    z = np.random.uniform(-1., 1., size=[batch_size, noise_dim])

    # prepare  targets (real image: 1, fake image: 0)
    # the first half of data fed to the disc are real images, the other half are fake images (coming from the generator)
    batch_disc_y = np.concatenate([np.ones([batch_size]), np.zeros([batch_size])], axis=0)
    # generator tries to fool the discriminator, thus targets are 1.
    batch_gen_y = np.ones([batch_size])

    # train
    feed_dict = {real_image_input: batch_x, noise_input: z, disc_target: batch_disc_y, gen_target: batch_gen_y}

    _, _, gl, dl = sess.run([train_gen, train_disc, gen_loss, disc_loss], feed_dict=feed_dict)

    if i % 100 == 0 or i == 1:
        print("step {}: generator loss: {}, discriminator loss: {}".format(i, gl, dl))

    
f, a = plt.subplots(4, 10, figsize=(10,4))
for i in range(10):
    z = np.random.uniform(-1., 1., size=[4, noise_dim])
    g = sess.run(gen_sample, feed_dict={noise_input: z})
    print("===================")
    print(np.repeat(g[0][:,:, np.newaxis], 3, axis=2))
    for j in range(4):
        img = np.reshape(np.repeat(g[j][:,:, np.newaxis], 3, axis=2), newshape=(28,28,3))
        a[j][i].imshow(img)
f.show()
plt.draw()
sess.close()
plt.waitforbuttonpress()
        

