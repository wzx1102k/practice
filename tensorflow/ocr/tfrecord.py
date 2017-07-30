import tensorflow as tf
import numpy as np
import cv2
import os

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

writer = tf.python_io.TFRecordWriter("train.tfrecords")

for line in open(LABEL_FILE, 'r'):
    cnt, label = line.split(': ')
    label = label[:-1]
    IMAGE_NAME = IMAGE_DIR + cnt + '.png'
    #print(IMAGE_NAME)
    img = cv2.imread(IMAGE_NAME, cv2.IMREAD_GRAYSCALE)
    img_raw = img.tobytes()
    label_raw = np.zeros(54*6)
    #must astype, maybe size is not algined with conv to string size
    label_raw = label_raw.astype(np.uint8)
    offset = 0
    for i in label:
        label_raw[sample_list.index(i) + offset] = 1
        offset += 54
    label_raw = np.reshape(label_raw, [1, 324])
    label_raw = label_raw.tostring()  # 这里是把ｃ换了一种格式存储
    train = tf.train.Example(features=tf.train.Features(feature={
        'cnt': tf.train.Feature(int64_list=tf.train.Int64List(value=[int(cnt)])),
        'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
        'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[label_raw]))
    }))
    writer.write(train.SerializeToString())  # 序列化为字符串
writer.close()