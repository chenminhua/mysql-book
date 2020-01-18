### create tensor

```py
my_tensor = tf.zeros([1, 20])
print(sess.run(my_tensor))

### create variable
my_var = tf.Variable(tf.zeros([1, 20]))
sess.run(my_var.initializer)
sess.run(my_var)

### create tensors based on other tensor's shape
tf.zeros_like(my_var)
tf.ones_like(my_var)

### filling a tensor with a constant
tf.fill([2,3], -1)
tf.constant([8,6,7,5])
tf.constant(-1, shape=[2,3])

### creating tensors based on sequences and ranges
tf.linspace(start=0.0, stop=1.0, num=3)
tf.range(start=6, limit=15, delta=3)

### random number
rnorm_var = tf.random_normal([2,3], mean=0.0, stddev=1.0)
runif_var = tf.random_uniform([2,3], minval=0, maxval=4)
```

### declare a placeholder

```py
x = tf.placeholder(tf.float32, shape=(4,4))
rand_array = np.random.rand(4,4)

### create a tensor to perform an operation, y is a Tensor
y = tf.identity(x)
print(sess.run(y, feed_dict={x: rand_array}))
```

### declare matrices

```py
identity_matrix = tf.diag([1.0, 1.0, 1.0])

# 2 * 3 random norm matrix
A = tf.truncated_normal([2, 3])

# 2 * 3 constant matrix
B = tf.fill([2,3], 5.0)

# 3 * 2 random uniform matrix
C = tf.random_uniform([3,2])

# create matrix from np array
D = tf.convert_to_tensor(np.array([[1,2],[2,3]]))
```

### matrix operation

```py
sess.run(A+B)
sess.run(tf.matmul(B, identity_matrix))
sess.run(tf.transpose(C))
sess.run(tf.matrix_determinant(D))
sess.run(tf.matrix_inverse(D))
sess.run(tf.cholesky(identity_matrix))

eigenvalues, eigenvectors = sess.run(tf.self_adjoint_eig(D))
```

### Arithmetic Operations

```py
sess.run(tf.div(3,4))
sess.run(tf.truediv(3,4))
sess.run(tf.floordiv(3.0, 4.0))

sess.run(tf.mod(22.0, 5.0))

sess.run(tf.cross([1., 0., 0.], [0, 1., 0.]))

sess.run(tf.sin(3.1416))
sess.run(tf.cos(3.1416))
sess.run(tf.div(tf.sin(3.1416/4.), tf.cos(3.1416/4.)))
```

### custom operation

```py
def custom_polynomial(x_val):
    return (tf.substact(3 * tf.square(x_val), x_val) + 10)

for num in test_nums:
    print(sess.run(custom_polynomial(num)))
```
