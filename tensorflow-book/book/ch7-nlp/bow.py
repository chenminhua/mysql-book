import tensorflow as tf
import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import string
import requests
import io
from zipfile import ZipFile
from tensorflow.contrib import learn
from bow_util import get_texts_data, normalize_text, split_dataset

tf.reset_default_graph()
sess = tf.Session()

# load dataset (spam, ham)
texts, target = get_texts_data()

# normalize text
texts = normalize_text(texts)

# # plot histogram of text lengths
# text_lengths = [len(x.split()) for x in texts]
# text_lengths = [x for x in text_lengths if x < 50]
# plt.hist(text_lengths, bins=25)
# plt.title('Histogram of # of Words in Texts')
# plt.show()

# choose max text word length at 25
senten_size = 25
min_word_freq = 3

# setup vocabulary processor  (所有句子都变成25个词，删除词频<3的词)
vocab_processor = learn.preprocessing.VocabularyProcessor(
    senten_size, min_frequency=min_word_freq)

# transform documents to word-id matrix
transformed_texts = np.array(
    [x for x in vocab_processor.transform(texts)])   # (5574, 25)
embedding_size = len(np.unique(transformed_texts))  # 8165

# split data to train/test
texts_train, texts_test, target_train, target_test = split_dataset(
    texts, target, len(texts))

# setup index matrix for one-hot-encoding
id_mat = tf.diag(tf.ones(shape=[embedding_size]))

# create variables for logistic regression
A = tf.Variable(tf.random_normal(shape=[embedding_size, 1]))
b = tf.Variable(tf.random_normal(shape=[1, 1]))

# placeholder, input a sentence, output a class (spam/ham)
x_data = tf.placeholder(shape=[senten_size], dtype=tf.int32)
y_target = tf.placeholder(shape=[1, 1], dtype=tf.float32)

# text-vocab embedding， embedding a sentence to x_embed
x_embed = tf.nn.embedding_lookup(id_mat, x_data)
x_col_sums = tf.reduce_sum(x_embed, 0)

# operations
x_col_sums_2D = tf.expand_dims(x_col_sums, 0)
model_output = tf.add(tf.matmul(x_col_sums_2D, A), b)

# loss
loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
    logits=model_output, labels=y_target))

# prediction operation
prediction = tf.sigmoid(model_output)

# optimizer
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(loss)

# initialize
sess.run(tf.global_variables_initializer())

# start logistic regression
print('Starting Training Over {} Sentences.'.format(len(texts_train)))
loss_vec = []
train_acc_all = []
train_acc_avg = []
for ix, t in enumerate(vocab_processor.fit_transform(texts_train)):
    y_data = [[target_train[ix]]]

    # Run through each observation for training
    sess.run(train_step, feed_dict={x_data: t, y_target: y_data})
    temp_loss = sess.run(loss, feed_dict={x_data: t, y_target: y_data})
    loss_vec.append(temp_loss)

    if (ix + 1) % 10 == 0:
        print('Training Observation #{}, Loss = {}'.format(ix+1, temp_loss))

    # Keep trailing average of past 50 observations accuracy
    # Get prediction of single observation
    [[temp_pred]] = sess.run(prediction, feed_dict={
                             x_data: t, y_target: y_data})
    # Get True/False if prediction is accurate
    train_acc_temp = target_train[ix] == np.round(temp_pred)
    train_acc_all.append(train_acc_temp)
    if len(train_acc_all) >= 50:
        train_acc_avg.append(np.mean(train_acc_all[-50:]))

# Get test set accuracy
print('Getting Test Set Accuracy For {} Sentences.'.format(len(texts_test)))
test_acc_all = []
for ix, t in enumerate(vocab_processor.fit_transform(texts_test)):
    y_data = [[target_test[ix]]]

    if (ix + 1) % 50 == 0:
        print('Test Observation #{}'.format(str(ix+1)))

    # Keep trailing average of past 50 observations accuracy
    # Get prediction of single observation
    [[temp_pred]] = sess.run(prediction, feed_dict={
                             x_data: t, y_target: y_data})
    # Get True/False if prediction is accurate
    test_acc_temp = target_test[ix] == np.round(temp_pred)
    test_acc_all.append(test_acc_temp)

print('\nOverall Test Accuracy: {}'.format(np.mean(test_acc_all)))

# Plot training accuracy over time
plt.plot(range(len(train_acc_avg)), train_acc_avg,
         'k-', label='Train Accuracy')
plt.title('Avg Training Acc Over Past 50 Generations')
plt.xlabel('Generation')
plt.ylabel('Training Accuracy')
plt.show()
