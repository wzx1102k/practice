import numpy as np
import cv2
import os,sys

def dct_encode(srcImg):
  rows, cols = srcImg.shape[:2]
  vis0 = np.zeros((rows, cols), np.float32)
  vis0[:rows, :cols] = srcImg
  vis1 = np.zeros((rows, cols), np.float32)
  #dct for 8*8 block
  for i in range(0, rows, 8):
    for j in range(0, cols, 8):
      vis1[i:i+8, j:j+8] = cv2.dct(vis0[i:i+8, j:j+8])
  return vis1.astype(int)

def dct_decode(srcImg):
  rows, cols = srcImg.shape[:2]
  vis0 = np.zeros((rows, cols), np.float32)
  vis0[:rows, :cols] = srcImg
  vis1 = np.zeros((rows, cols), np.float32)
  #idct for 8*8 block
  for i in range(0, rows, 8):
    for j in range(0, cols, 8):
      vis1[i:i+8, j:j+8] = cv2.idct(vis0[i:i+8, j:j+8])
  return vis1

def rgb2ycbcr(srcImg):
  #3*3 rgb to ycbcr matrix
  trans = [[0.097906, 0.504129, 0.256789], [0.439215, -0.290992, -0.148223], [-0.071426, -0.367789, 0.439215]]
  return np.dot(srcImg, np.transpose(trans)) + [16, 128, 128]

def ycbcr2rgb(srcImg):
  delta = [-16, -128, -128]
  trans = [[1.164383, 2.017230, 0], [1.164383, -0.391762, -0.812969], [1.163483, 0, 1.596027]]
  return np.uint8(np.dot(srcImg - [16, 128, 128], np.transpose(trans)))

if __name__ == "__main__":
  #0: gray ,  >0 return rgb
  image_path = sys.argv[1]
  img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  #hegith * width
  print img.shape[:]
  if img.shape[2] == 3:
    print "rgb type"
    #3*3 rgb to ycbcr matrix
    img_conv = rgb2ycbcr(img)
    img_iconv = ycbcr2rgb(img_conv)

    y = img_conv[:,:,0]
    cb = img_conv[:,:,1]
    cr = img_conv[:,:,2]
    rows, cols, channels = img.shape[:3]
    eImg = np.zeros((rows, cols, channels), np.float32)
    dImg = np.zeros((rows, cols, channels), np.float32)
    error = np.zeros((rows,cols, channels), np.float32)
    for i in range(0,3,1):
      eImg[:,:,i] = dct_encode(img_conv[:,:,i])
    for i in range(0,3,1):
      dImg[:,:,i] = dct_decode(eImg[:,:,i])
    print eImg[0:8, 0:8, 2].astype(int)
    #print dImg.itemsize
  else:
    print "gray type"
  #cv2.imshow('', np.uint8(img_conv[:,:,1]))  
  #cv2.waitKey()
  #cv2.imwrite('saved.jpg', eImg)
 # cv2.imshow('lena', img)
 # cv2.waitKey()
