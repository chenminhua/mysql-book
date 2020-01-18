## A Regression Example

x_data * A = target_values， calculate A.

```py
# generate dataset
x_vals = np.random.normal(1, 0.1, 100)
y_vals = np.repeat(10., 100)

# placeholder
x_data = tf.placeholder(shape=[1], dtype=tf.float32)
y_target = tf.placeholder(shape=[1], dtype=tf.float32)

# create variable
A = tf.Variable(tf.random_normal(shape=[1]))

# add operation to graph
my_output = tf.multiply(x_data, A)

# loss function (L2 loss)
loss = tf.square(my_output - y_target)

# optimizer
train_step = tf.train.GradientDescentOptimizer(0.02).minimize(loss)

# initialize variable
sess.run(tf.global_variables_initializer())

# run the loop
for i in range(100):
    rand_index = np.random.choice(100)
    rand_x = [x_vals[rand_index]]
    rand_y = [x_vals[rand_index]]
    sess.run(train_step, feed_dict={x_data: rand_x, y_target: rand_y})
    if (i+1)%25==0:
        print('Step #' + str(i+1) + ' A = ' + str(sess.run(A)))
        print('Loss = ' + str(sess.run(loss, feed_dict={x_data: rand_x, y_target: rand_y})))
```

## A Classification Example

Normal(mean=-1, sd=1) => class 0 and Normal(mean=3, sd=1) => class 1

if sigmoid(x+A) < 0.5 then predict class 0 else class 1. Theoretically, A should be -1

```py
# generate dataset
x_vals = np.concatenate((np.random.normal(-1, 1, 50), np.random.normal(3,1,50)))
y_vals = np.concatenate((np.repeat(0., 50), np.repeat(1., 50)))

# placeholder
x_data = tf.placeholder(shape=[1], dtype=tf.float32)
y_target = tf.placeholder(shape=[1], dtype=tf.float32)

# create variable
A = tf.Variable(tf.random_normal(mean=10, shape=[1]))

# add operation to graph
my_output = tf.add(x_data, A)
### now we have to add another dimension (batch dimension) to each
my_output_expanded = tf.expand_dims(my_output, 0)
y_target_expanded = tf.expand_dims(y_target, 0)

# classificatin loss (cross entropy)
xentropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=my_output_expanded, labels=y_target_expanded)

# Optimizer
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(xentropy)

# initialize variables
sess.run(tf.global_variables_initializer())

# run the loop
for i in range(1400):
    rand_index = np.random.choice(100)
    rand_x = [x_vals[rand_index]]
    rand_y = [y_vals[rand_index]]
    sess.run(train_step, feed_dict={x_data: rand_x, y_target: rand_y})

    if (i+1)%200==0:
        print('Step #' + str(i+1) + ' A = ' + str(sess.run(A)))
        print('Loss = ' + str(sess.run(xentropy, feed_dict={x_data: rand_x, y_target: rand_y})))
    
# Evaluate Predictions
predictions = []
for i in range(len(x_vals)):
    x_val = [x_vals[i]]
    prediction = sess.run(tf.round(tf.sigmoid(my_output)), feed_dict={x_data: x_val})
    predictions.append(prediction[0])
    
accuracy = sum(x==y for x,y in zip(predictions, y_vals))/100.
print('Ending Accuracy = ' + str(np.round(accuracy, 2)))

```

## 关于 tf.expand_dims

```py
expand_dims(input, axis=None, name=None, dim=None)
    Inserts a dimension of 1 into a tensor's shape. (deprecated arguments)
    
    SOME ARGUMENTS ARE DEPRECATED. They will be removed in a future version.
    Instructions for updating:
    Use the `axis` argument instead
    
    Given a tensor `input`, this operation inserts a dimension of 1 at the
    dimension index `axis` of `input`'s shape. The dimension index `axis` starts
    at zero; if you specify a negative number for `axis` it is counted backward
    from the end.
    
    This operation is useful if you want to add a batch dimension to a single
    element. For example, if you have a single image of shape `[height, width,
    channels]`, you can make it a batch of 1 image with `expand_dims(image, 0)`,
    which will make the shape `[1, height, width, channels]`.
    
    Other examples:
    
    ```python
    # 't' is a tensor of shape [2]
    tf.shape(tf.expand_dims(t, 0))  # [1, 2]
    tf.shape(tf.expand_dims(t, 1))  # [2, 1]
    tf.shape(tf.expand_dims(t, -1))  # [2, 1]
    
    # 't2' is a tensor of shape [2, 3, 5]
    tf.shape(tf.expand_dims(t2, 0))  # [1, 2, 3, 5]
    tf.shape(tf.expand_dims(t2, 2))  # [2, 3, 1, 5]
    tf.shape(tf.expand_dims(t2, 3))  # [2, 3, 5, 1]
    ```
    
    This operation requires that:
    
    `-1-input.dims() <= dim <= input.dims()`
    
    This operation is related to `squeeze()`, which removes dimensions of
    size 1.
    
    Args:
      input: A `Tensor`.
      axis: 0-D (scalar). Specifies the dimension index at which to
        expand the shape of `input`. Must be in the range
        `[-rank(input) - 1, rank(input)]`.
      name: The name of the output `Tensor`.
      dim: 0-D (scalar). Equivalent to `axis`, to be deprecated.
    
    Returns:
      A `Tensor` with the same data as `input`, but its shape has an additional
      dimension of size 1 added.
```

## 关于 tf.nn.sigmoid_cross_entropy_with_logits

```py
sigmoid_cross_entropy_with_logits(_sentinel=None, labels=None, logits=None, name=None)
Computes sigmoid cross entropy given `logits`.

Measures the probability error in discrete classification tasks in which each
class is independent and not mutually exclusive.  For instance, one could
perform multilabel classification where a picture can contain both an elephant
and a dog at the same time.

For brevity, let `x = logits`, `z = labels`.  The logistic loss is

        z * -log(sigmoid(x)) + (1 - z) * -log(1 - sigmoid(x))
    = z * -log(1 / (1 + exp(-x))) + (1 - z) * -log(exp(-x) / (1 + exp(-x)))
    = z * log(1 + exp(-x)) + (1 - z) * (-log(exp(-x)) + log(1 + exp(-x)))
    = z * log(1 + exp(-x)) + (1 - z) * (x + log(1 + exp(-x))
    = (1 - z) * x + log(1 + exp(-x))
    = x - x * z + log(1 + exp(-x))

For x < 0, to avoid overflow in exp(-x), we reformulate the above

        x - x * z + log(1 + exp(-x))
    = log(exp(x)) - x * z + log(1 + exp(-x))
    = - x * z + log(1 + exp(x))

Hence, to ensure stability and avoid overflow, the implementation uses this
equivalent formulation

    max(x, 0) - x * z + log(1 + exp(-abs(x)))

`logits` and `labels` must have the same type and shape.

Args:
    _sentinel: Used to prevent positional parameters. Internal, do not use.
    labels: A `Tensor` of the same type and shape as `logits`.
    logits: A `Tensor` of type `float32` or `float64`.
    name: A name for the operation (optional).

Returns:
    A `Tensor` of the same shape as `logits` with the componentwise
    logistic losses.
```