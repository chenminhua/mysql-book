## visualize a scalar value

```py
summary_writer = tf.summary.FileWriter('tensorboard', tf.get_default_graph())

if not os.path.exists('tensorboard'):
    os.makedirs('tensorboard')

# create input data
x_data = np.arange(1000)/10.
y_data = x_data * 2. + np.random.normal(loc=0.0, scale=25, size=1000)

# split into train/test
train_ix = np.random.choice(len(x_data), size=int(len(x_data)*0.9), replace=False)
test_ix = np.setdiff1d(np.arange(1000), train_ix)
x_data_train, y_data_train = x_data[train_ix], y_data[train_ix]
x_data_test, y_data_test = x_data[test_ix], y_data[test_ix]

# placeholder
x_input = tf.placeholder(tf.float32, [None])
y_input = tf.placeholder(tf.float32, [None])

# variable
m = tf.Variable(tf.random_normal([1], dtype=tf.float32), name='Slope')

# model operation
output = tf.multiply(m, x_input, name='Batch_multiplication')

# loss
loss = tf.reduce_mean(tf.abs(output - y_input), name='L1_loss')

# optimizer
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

# visualize a scalar
with tf.name_scope('Slope_Estimate'):
    tf.summary.scalar('Slope_Estimate', tf.squeeze(m))
```

## visualize a histogram values

## add a custom matplotlib graph to tensorboard