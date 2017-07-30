import tensorflow as tf
import numpy as np

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
    img = tf.reshape(img, [1, 10000])  #reshape image
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5 #throw img tensor
    cnt = features['cnt'] #throw label tensor
    label = tf.decode_raw(features['label'], tf.uint8)
    label = tf.reshape(label, [1, 324])
    label = tf.cast(label, tf.float32)
    return cnt, img, label

cnt, img, label = read_and_decode('train.tfrecords')

#use shuffle batch to get data  [x,y,z] -> output [batch_size, x, y, z]
# shuffle = true: random get batch  shuffle = false: step by step(0->1->2...)
# capacity: An integer. The maximum number of elements in the queue.
# batch_size: The new batch size pulled from the queue.
# min_after_dequeue: Minimum number elements in the queue after a dequeue, used to ensure a level of mixing of elements.
# num_threads: The number of threads enqueuing tensor_list.
cnt_batch, img_batch, label_batch = tf.train.shuffle_batch([cnt, img, label], batch_size=1,
                                capacity=500, min_after_dequeue=200, num_threads=2)
sess = tf.Session()
sess.run(tf.global_variables_initializer())

tf.train.start_queue_runners(sess=sess)
cnt_val, img_val, label_val = sess.run([cnt_batch, img_batch, label_batch])
print ('first batch:')
print(cnt_val)
print(label_val)
cnt_val, img_val, label_val = sess.run([cnt_batch, img_batch, label_batch])
print ('seconde batch:')
print(cnt_val)
print(label_val)
cnt_val, img_val, label_val = sess.run([cnt_batch, img_batch, label_batch])
print ('third batch:')
print(cnt_val)
print(label_val)

