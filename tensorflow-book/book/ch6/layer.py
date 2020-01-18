import tensorflow as tf
import numpy as np

tf.reset_default_graph()

sess = tf.Session()

# ensure reproducibility
seed=13
np.random.seed(seed)
tf.set_random_seed(seed)


# model parameter
conv_size = 2
conv_stride_size = 2
maxpool_size = 2
maxpool_stride_size = 1

# generate 1D data
data_size = [10, 10]
data = np.random.normal(size=data_size)

# placeholder
x_input = tf.placeholder(dtype=tf.float32, shape=data_size)

# convolution
def conv_layer(input, my_filter, stride):
    input_3d = tf.expand_dims(input, 0)   # batch
    input_4d = tf.expand_dims(input_3d, 3)   # channel

    convolution_output = tf.nn.conv2d(input_4d, filter=my_filter, 
                            strides=[1, stride, stride, 1], padding="VALID")
    # get rid of unnecessary dims
    return tf.squeeze(convolution_output)

def activation(input):
    return tf.nn.relu(input)

def max_pool(input, height, width, stride):
    input_3d = tf.expand_dims(input, 0)   # batch
    input_4d = tf.expand_dims(input_3d, 3)   # channel
    return tf.squeeze(tf.nn.max_pool(input_4d, ksize=[1, height, width, 1],
                                    strides=[1, stride, stride, 1], padding="VALID"))

#--------Fully Connected--------
def fully_connected(input_layer, num_outputs):
    # In order to connect our whole W byH 2d array, we first flatten it out to
    # a W times H 1D array.
    flat_input = tf.reshape(input_layer, [-1])
    # We then find out how long it is, and create an array for the shape of
    # the multiplication weight = (WxH) by (num_outputs)
    weight_shape = tf.squeeze(tf.stack([tf.shape(flat_input),[num_outputs]]))
    # Initialize the weight
    weight = tf.random_normal(weight_shape, stddev=0.1)
    # Initialize the bias
    bias = tf.random_normal(shape=[num_outputs])
    # Now make the flat 1D array into a 2D array for multiplication
    input_2d = tf.expand_dims(flat_input, 0)
    # Multiply and add the bias
    full_output = tf.add(tf.matmul(input_2d, weight), bias)
    # Get rid of extra dimension
    return tf.squeeze(full_output)

my_filter = tf.Variable(tf.random_normal(shape=[conv_size, conv_size, 1, 1]))
my_convolution_output = conv_layer(x_input, my_filter, stride=conv_stride_size)

my_activation_output = activation(my_convolution_output)

my_maxpool_output = max_pool(my_activation_output, 
                             maxpool_size, maxpool_size,maxpool_stride_size)


my_full_output = fully_connected(my_maxpool_output, 5)

# initialize 
sess.run(tf.global_variables_initializer())

feed_dict = {x_input: data}

print('>>>> 2D Data <<<<')

# Convolution Output
print('Input = %s array' % (x_input.shape.as_list()))
print('%s Convolution, stride size = [%d, %d] , results in the %s array' % 
      (my_filter.get_shape().as_list()[:2],conv_stride_size,conv_stride_size,my_convolution_output.shape.as_list()))
print(sess.run(my_convolution_output, feed_dict=feed_dict))

# Activation Output
print('\nInput = the above %s array' % (my_convolution_output.shape.as_list()))
print('ReLU element wise returns the %s array' % (my_activation_output.shape.as_list()))
print(sess.run(my_activation_output, feed_dict=feed_dict))

# Max Pool Output
print('\nInput = the above %s array' % (my_activation_output.shape.as_list()))
print('MaxPool, stride size = [%d, %d], results in %s array' % 
      (maxpool_stride_size,maxpool_stride_size,my_maxpool_output.shape.as_list()))
print(sess.run(my_maxpool_output, feed_dict=feed_dict))

# Fully Connected Output
print('\nInput = the above %s array' % (my_maxpool_output.shape.as_list()))
print(my_maxpool_output.shape)
print('Fully connected layer on all %d rows results in %s outputs:' % 
      (my_maxpool_output.shape.as_list()[0],my_full_output.shape.as_list()[0]))
print(sess.run(my_full_output, feed_dict=feed_dict))