y = Ax + b

```py
# get dataset
iris = datasets.load_iris()
x_vals = np.array([x[3] for x in iris.data]) # (150,)
y_vals = np.array([y[0] for y in iris.data]) # (150,)

batch_size = 25

# placeholder
x_data = tf.placeholder(shape=[None, 1], dtype=tf.float32)
y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)

# variables
A = tf.Variable(tf.random_normal(shape=[1,1]))
b = tf.Variable(tf.random_normal(shape=[1,1]))

# operation (y = Ax + b)
model_output = tf.add(tf.matmul(x_data, A), b)

# loss (L2 loss)
loss = tf.reduce_mean(tf.square(y_target - model_output))

# optimizer
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

# initialize variables
sess.run(tf.global_variables_initializer())

# train
loss_vec = []
for i in range(100):
    rand_index = np.random.choice(len(x_vals), size=batch_size)
    rand_x = np.transpose([x_vals[rand_index]])
    rand_y = np.transpose([y_vals[rand_index]])
    sess.run(train_step, feed_dict={x_data: rand_x, y_target: rand_y})
    temp_loss = sess.run(loss, feed_dict={x_data: rand_x, y_target: rand_y})
    loss_vec.append(temp_loss)
    if (i+1)%25==0:
        print('Step #' + str(i+1) + ' A = ' + str(sess.run(A)) + ' b = ' + str(sess.run(b)))
        print('Loss = ' + str(temp_loss))


# Plot loss over time
plt.plot(loss_vec, 'k-')
plt.title('L2 Loss per Generation')
plt.xlabel('Generation')
plt.ylabel('L2 Loss')
plt.show()
```

### lasso

```py
# Declare Lasso loss function
# Lasso Loss = L2_Loss + heavyside_step,
# Where heavyside_step ~ 0 if A < constant, otherwise ~ 99
lasso_param = tf.constant(0.9)
heavyside_step = tf.truediv(1., tf.add(1., tf.exp(tf.multiply(-50., tf.subtract(A, lasso_param)))))
regularization_param = tf.multiply(heavyside_step, 99.)
loss = tf.add(tf.reduce_mean(tf.square(y_target - model_output)), regularization_param)
```

### ridge

```py
# Declare the Ridge loss function
# Ridge loss = L2_loss + L2 norm of slope
ridge_param = tf.constant(1.)
ridge_loss = tf.reduce_mean(tf.square(A))
loss = tf.expand_dims(tf.add(tf.reduce_mean(tf.square(y_target - model_output)), tf.multiply(ridge_param, ridge_loss)), 0)
```