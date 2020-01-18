```py
# start a graph session
sess = tf.Session()

...

# add summaries to tensorboard
merged = tf.summary.merge_all()

# initialize graph writer
writer = tf.summary.FileWriter("/tmp/variable_logs", graph=sess.graph)
```


### 启动tensorboard

```
tensorboard --logdir=/tmp
# 然后访问 http://0.0.0.0:6006/
```