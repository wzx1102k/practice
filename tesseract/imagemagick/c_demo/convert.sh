#! /bin/bash

make clean
make
rm -rf ocr1.tif
ldconfig /home/cloud/cloud-git-master/practice/tesseract/imagemagick/c_demo
./demo_conv ocr1.jpg ocr1.tif
