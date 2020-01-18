import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("../../data/mnist", one_hot=True)
# mnist.train.labels.shape = (55000, 10);
# mnist.train.images.shape = (55000, 784);
# mnist.test.labels.shape = (5000, 10);
# mnist.test.images.shape = (5000, 784);

# parameters
### training param
learning_rate = 0.001
num_steps = 2000
batch_size = 128
display_steps = 50

### model param
num_input = 784
num_classes = 10
dropout_rate = 0.2


### helper func
def conv2d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    # MaxPool2D wrapper
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                          padding='SAME')


def conv_net(input, reuse=False, is_training=True):
    print("reuse, ", reuse)
    with tf.variable_scope('ConvNet', reuse=reuse):
        w1 = tf.get_variable('w1', initializer=tf.random_normal([5, 5, 1, 32]))
        b1 = tf.get_variable('b1', initializer=tf.random_normal([32]))
        conv1 = conv2d(tf.reshape(input, shape=[-1, 28, 28, 1]), w1,b1)  # (?, 28, 28, 32)
        conv1 = maxpool2d(conv1, k=2)  # (?, 14, 14, 32)

        w2 = tf.get_variable('w2', initializer=tf.random_normal([5, 5, 32, 64]))
        b2 = tf.get_variable('b2', initializer=tf.random_normal([64]))
        conv2 = conv2d(conv1, w2, b2)  # (?, 14, 14, 64)
        conv2 = maxpool2d(conv2, k=2)  # (?, 7, 7, 64)

        w3 = tf.get_variable('w3', initializer=tf.random_normal([7 * 7 * 64, 1024]))
        b3 = tf.get_variable('b3', initializer=tf.random_normal([1024]))
        fc1 = tf.matmul(tf.reshape(conv2, [-1, 3136]), w3)
        fc1 = tf.add(fc1, b3)
        fc1 = tf.nn.relu(fc1)
        fc1 = tf.layers.dropout(fc1, rate=dropout_rate, training=is_training)  # (?, 1024)

        w4 = tf.get_variable('w4', initializer=tf.random_normal([1024, num_classes]))
        b4 = tf.get_variable('b4', initializer=tf.random_normal([num_classes]))

        out = tf.matmul(fc1, w4)
        out = tf.add(out, b4)  # (?, 10)
    return out


X = tf.placeholder(tf.float32, shape=[None, num_input])
Y = tf.placeholder(tf.float32, shape=[None, num_classes])


# multi GPU
gpu_nums = 2
X_list = tf.split(X, gpu_nums)
Y_list = tf.split(Y, gpu_nums)
losses = []
for gpu_id in range(int(gpu_nums)):
    with tf.device(tf.DeviceSpec(device_type='GPU', device_index=gpu_id)):
        reuse = False if gpu_id == 0 else True
        _x, _y = X_list[gpu_id], Y_list[gpu_id]
        train_out = conv_net(_x, reuse=reuse)
        losses.append(tf.nn.softmax_cross_entropy_with_logits(logits=train_out, labels=_y))
        if gpu_id == 0:
            # do predicting test only on gpu0
            valid_out = conv_net(_x, reuse=True, is_training=False)
            valid_pred = tf.nn.softmax(valid_out)
            valid_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=valid_out, labels=_y))
            valid_correct_pred = tf.equal(tf.argmax(valid_pred, 1), tf.argmax(_y, 1))
            valid_acc = tf.reduce_mean(tf.cast(valid_correct_pred, tf.float32))

loss = tf.reduce_mean(tf.concat(losses, axis=0))
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss, colocate_gradients_with_ops=True)


# init
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# train
for step in range(1, num_steps + 1):
    batch_x, batch_y = mnist.train.next_batch(batch_size)
    # run optimization op
    sess.run(train_step, feed_dict={X: batch_x, Y: batch_y})
    if step % display_steps == 0 or step == 1:
        v_loss, v_acc = sess.run([valid_loss, valid_acc], feed_dict={X: batch_x, Y: batch_y})
        print("Step {}, loss= {}, Training Accuracy= {}".format(step, v_loss, v_acc))

print("Optimization Finished!")

# Calculate accuracy for 256 MNIST test images
print("Testing Accuracy:", sess.run(valid_acc, feed_dict={X: mnist.test.images,
                                    Y: mnist.test.labels}))

sess.close()
