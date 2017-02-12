import numpy as np
import cv2


if __name__ == "__main__":
  #0: gray ,  >0 return rgb
  img = cv2.imread("samples/lena.tif", cv2.IMREAD_GRAYSCALE)
  #hegith * width
  print img.shape[:]
  rows, cols = img.shape[:2]
  vis0 = np.zeros((rows, cols), np.float32)
  vis0[:rows, :cols] = img
  vis1 = np.zeros((rows, cols), np.float32)
  #dct for 8*8 block
  for i in range(0, rows, 8):
    for j in range(0, cols, 8):
      vis1[i:i+1, j:j+1] = cv2.dct(vis0[i:i+1, j:j+1])
  print vis1[7,7]
#  vis1 = cv2.dct(vis0)
#  img_dct = cv.CreateMat(vis1.shape[0], vis1.shape[1], cv.CV_32FC3)
#  cv.CvtColor(cv.fromarray(vis1), img_dct, cv.CV_GRAY2BGR)
  cv2.imshow('', vis1)  
  cv2.waitKey()
  cv2.imwrite('saved.jpg', vis1)
 # cv2.imshow('lena', img)
 # cv2.waitKey()
