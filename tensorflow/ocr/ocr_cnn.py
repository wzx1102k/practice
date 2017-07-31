import tensorflow as tf
import numpy as np
import cv2
import sys

def weight_variable(shape):
    #create random variable
    #truncated_normal (shape, mean, stddev)  gauss function
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def con2d(x, W):
    #strides[1,x_mov, y_mov,1]  step: x_mov = 1 y_mov = 1, stride[0]&stride[3] =1
    #input size is same with output same
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pooling_2x2(x):
    #step change to 2
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def read_and_decode(tf_record_path): # read iris_contact.tfrecords
    filename_queue = tf.train.string_input_producer([tf_record_path])# create a queue

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)#return file_name and file
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'cnt': tf.FixedLenFeature([], tf.int64),
                                           'img_raw' : tf.FixedLenFeature([], tf.string),
                                           'label': tf.FixedLenFeature([], tf.string),
                                       })#return image and label

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [10000])  #reshape image
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5 #throw img tensor
    cnt = features['cnt'] #throw label tensor
    label = tf.decode_raw(features['label'], tf.uint8)
    label = tf.reshape(label, [324])
    label = tf.cast(label, tf.float32)
    return cnt, img, label

## initial cnn variables
IMAGE_DIR = './png/train/'
LABEL_FILE = './label.txt'
sample_list = [
        '2', '3', '4', '5', '6', '7',
        '8', '9', 'a', 'b', 'c', 'd',
        'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'm', 'n', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x',
        'y', 'z', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'K', 'M',
        'N', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z']

## rgb 200 * 50 * 3
## gray 200 * 50
xs = tf.placeholder(tf.float32, [None, 10000]) # gray
ys = tf.placeholder(tf.float32, [None, 324])  #54*6
keep_prob = tf.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1, 200, 50, 1])

#5X5 patch, size:1 height:32
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

#conv1 layer
h_conv1 = tf.nn.relu(con2d(x_image, W_conv1) + b_conv1) # output 200 * 50 * 32
h_pool1 = max_pooling_2x2(h_conv1)  # output 100 * 25 * 32

#conv2 layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_con2 = tf.nn.relu(con2d(h_pool1, W_conv2) + b_conv2) #output 100*25*64
h_pool2 = max_pooling_2x2(h_con2)  #output 50 * 13 * 64
'''
#conv3 layer
W_conv3 = weight_variable([5, 5, 64, 128])
b_conv3 = bias_variable([128])

h_con3 = tf.nn.relu(con2d(h_pool2, W_conv3) + b_conv3) #output 100*25*64
h_pool3 = max_pooling_2x2(h_con3)  #output 25 * 7 * 128'''

#func1 layer
W_fc1 = weight_variable([50*13*64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 50*13*64]) # [n_samples, 7, 7, 64] ==> [n_samples, 7*7*64]
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

'''W_fc1 = weight_variable([25*7*128, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool3, [-1, 25*7*128]) # [n_samples, 7, 7, 64] ==> [n_samples, 7*7*64]
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)'''

#func2_layer_1
W_fc2_1 = weight_variable([1024, 54])
b_fc2_1 = bias_variable([54])

fc2_1 = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2_1) + b_fc2_1)

#func2_layer_2
W_fc2_2 = weight_variable([1024, 54])
b_fc2_2 = bias_variable([54])

fc2_2 = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2_2) + b_fc2_2)

#func2_layer_3
W_fc2_3 = weight_variable([1024, 54])
b_fc2_3 = bias_variable([54])

fc2_3 = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2_3) + b_fc2_3)

#func2_layer_4
W_fc2_4 = weight_variable([1024, 54])
b_fc2_4 = bias_variable([54])

fc2_4 = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2_4) + b_fc2_4)

#func2_layer_5
W_fc2_5 = weight_variable([1024, 54])
b_fc2_5 = bias_variable([54])

fc2_5 = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2_5) + b_fc2_5)

#func2_layer_6
W_fc2_6 = weight_variable([1024, 54])
b_fc2_6 = bias_variable([54])

fc2_6 = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2_6) + b_fc2_6)

predict = tf.concat([fc2_1, fc2_2, fc2_3, fc2_4, fc2_5, fc2_6], 1)

#cross
cross_entrop =tf.reduce_mean(-tf.reduce_sum(ys * tf.log(predict), reduction_indices=[1]))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entrop)

cnt, img, label = read_and_decode('train.tfrecords')
print(cnt)
print(img)
print(label)
cnt_batch, img_batch, label_batch = tf.train.shuffle_batch([cnt, img, label], batch_size=1,
                                capacity=500, min_after_dequeue=200, num_threads=2)
print('run1')
sess = tf.Session()
sess.run(tf.global_variables_initializer())

tf.train.start_queue_runners(sess=sess)

for i in range(100):
    cnt_val, img_val, label_val = sess.run([cnt_batch, img_batch, label_batch])
    print('run')
    sess.run(train_step, feed_dict={xs: img_val, ys: label_val, keep_prob: 1})
    print(sess.run(cross_entrop, feed_dict={xs: img_val, ys: label_val, keep_prob: 1}))

