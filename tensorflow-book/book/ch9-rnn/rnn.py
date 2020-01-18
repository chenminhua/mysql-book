import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import re
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from util.dataset import get_spam_text_dataset, split_dataset, clean_text, shuffle_dataset
tf.reset_default_graph()

# parameters
epochs = 20
batch_size = 250
max_sequence_length = 25
rnn_size = 10
embedding_size = 50
min_word_frequency = 10
learning_rate = 0.0005
dropout_keep_prob = tf.placeholder(tf.float32)

text_data_train, text_data_target = get_spam_text_dataset() 

# Clean texts
text_data_train = [clean_text(x) for x in text_data_train]
text_data_target = np.array(text_data_target)

# Change texts into numeric vectors
vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(max_sequence_length,
                                                                     min_frequency=min_word_frequency)
text_processed = np.array(list(vocab_processor.fit_transform(text_data_train)))

# Shuffle and Split train/test set
x_train, x_test, y_train, y_test = split_dataset(text_processed, text_data_target, len(text_data_train), 0.8)
vocab_size = len(vocab_processor.vocabulary_)
print("Vocabulary Size: {:d}".format(vocab_size))
print("80-20 Train Test split: {:d} -- {:d}".format(len(y_train), len(y_test)))

# Create placeholders
x_data = tf.placeholder(tf.int32, [None, max_sequence_length])
y_output = tf.placeholder(tf.int32, [None])

# Create embedding
embedding_mat = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0))    # 933 * 50
embedding_output = tf.nn.embedding_lookup(embedding_mat, x_data)   # ? * 25 * 50

cell = tf.contrib.rnn.BasicRNNCell(num_units=rnn_size)

output, state = tf.nn.dynamic_rnn(cell, embedding_output, dtype=tf.float32)   # ? * 25 * 10
output = tf.nn.dropout(output, dropout_keep_prob)     # ? * 25 * 10

# Get output of RNN sequence
output = tf.transpose(output, [1, 0, 2])      # 25 * ? * 10  
last = tf.gather(output, int(output.get_shape()[0]) - 1)   # ? * 10

# 再来个输出层
weight = tf.Variable(tf.truncated_normal([rnn_size, 2], stddev=0.1))
bias = tf.Variable(tf.constant(0.1, shape=[2]))
logits_out = tf.matmul(last, weight) + bias

# Loss function
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits_out, labels=y_output))

accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(logits_out, 1), tf.cast(y_output, tf.int64)), tf.float32))

train_step = tf.train.RMSPropOptimizer(learning_rate).minimize(loss)

# Start a graph
sess = tf.Session()
sess.run(tf.global_variables_initializer())

train_loss = []
test_loss = []
train_accuracy = []
test_accuracy = []

num_batches = int(len(x_train)/batch_size) + 1

# Start training
for epoch in range(epochs):

    # Shuffle training data
    x_train, y_train = shuffle_dataset(x_train, y_train)
    
    # TO DO CALCULATE GENERATIONS ExACTLY
    for i in range(num_batches):
        # Select train data
        min_ix = i * batch_size
        max_ix = np.min([len(x_train), ((i+1) * batch_size)])
        x_train_batch = x_train[min_ix:max_ix]
        y_train_batch = y_train[min_ix:max_ix]
        
        # Run train step
        train_dict = {x_data: x_train_batch, y_output: y_train_batch, dropout_keep_prob:0.5}
        sess.run(train_step, feed_dict=train_dict)
        
    # Run loss and accuracy for training
    temp_train_loss, temp_train_acc = sess.run([loss, accuracy], feed_dict=train_dict)
    train_loss.append(temp_train_loss)
    train_accuracy.append(temp_train_acc)
    
    # Run Eval Step
    test_dict = {x_data: x_test, y_output: y_test, dropout_keep_prob:1.0}
    temp_test_loss, temp_test_acc = sess.run([loss, accuracy], feed_dict=test_dict)
    test_loss.append(temp_test_loss)
    test_accuracy.append(temp_test_acc)
    print('Epoch: {}, Test Loss: {:.2}, Test Acc: {:.2}'.format(epoch+1, temp_test_loss, temp_test_acc))
    
# Plot loss over time
epoch_seq = np.arange(1, epochs+1)
plt.plot(epoch_seq, train_loss, 'k--', label='Train Set')
plt.plot(epoch_seq, test_loss, 'r-', label='Test Set')
plt.title('Softmax Loss')
plt.xlabel('Epochs')
plt.ylabel('Softmax Loss')
plt.legend(loc='upper left')
plt.show()

# Plot accuracy over time
plt.plot(epoch_seq, train_accuracy, 'k--', label='Train Set')
plt.plot(epoch_seq, test_accuracy, 'r-', label='Test Set')
plt.title('Test Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='upper left')
plt.show()