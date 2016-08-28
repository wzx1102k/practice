#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata
echo $TESSDATA_PREFIX

java -Djava.library.path=. com.ocr_java eng_jpg/ocr1.tif eng_jpg/result.txt

