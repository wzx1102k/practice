#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata

if [ -f result.txt ]; then
	rm -rf result.txt
fi

for file in *.jpg
	do convert $file ${file%%.*}.tif
	./demo_tesseract ${file%%.*}.tif result.txt
done


