#!/usr/bin/python
# -*- coding:utf-8 -*-

## 如何给tensorFlow提供数据 ##
## 1) feed: 在程序运行的每一步，提供数据 ##
## 2) file: 在程序开始，设置输入pipeline read from file ##
## 3) preload: 定义常量或变量，存储所有数据 ##

from __future__ import print_function
import tensorflow as tf

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
x = tf.placeholder("float", shape=[None, 784])
y_ = tf.placeholder("float", shape=[None, 10])

## 第一层卷积 ##
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

## 第二层卷积 ##
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

## 连接 ##
W_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

## Dropout ##
keep_prob  = tf.placeholder('float')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

## 输出 ##
W_fc2  = weight_variable([1024, 10])
b_fc2  = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

## 训练 ##
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

sess = tf.InteractiveSession()
#sess = tf.Session() ## 与上面的InteractiveSession的区别
# a=tf.constant(5.0); b=tf.constant(6,0); c=a*b
# sess = tf.Session(); sess.run(c); sess.close()
# sess = tf.InteractiveSession(); c.eval(); sess.run(c); sess.close(0
#sess.run(tf.initialize_all_variables())
sess.run(tf.global_variables_initializer())
for i in range(10000):
	batch = mnist.train.next_batch(50)
	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
	if i%100 == 0:
		train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		test_accuracy  = accuracy.eval(feed_dict={x:mnist.test.images, y_:mnist.test.labels, keep_prob:1.0})
		print (i, 'training accuracy :', train_accuracy, 'test accuracy :', test_accuracy)

print ('test accuracy :', accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

##############################################################################



