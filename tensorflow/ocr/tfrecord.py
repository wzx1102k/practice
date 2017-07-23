import tensorflow as tf
import cv2
import os

IMAGE_DIR = './png/train/'
LABEL_FILE = './label.txt'


writer = tf.python_io.TFRecordWriter("train.tfrecords")

for line in open(LABEL_FILE, 'r'):
    cnt, label = line.split(': ')
    label = label[:-1]
    IMAGE_NAME = IMAGE_DIR + cnt + '.png'
    print(IMAGE_NAME)
    img = cv2.imread(IMAGE_NAME)
    train = tf.train.Example(features=tf.train.Features(feature={
        "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
        'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img]))
    }))
    writer.write(train.SerializeToString())  # 序列化为字符串
writer.close()