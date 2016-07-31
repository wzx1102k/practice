#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata

if [ -f result.txt ]; then
	rm -rf result.txt
fi

for file in ./eng_jpg/*.jpg
#	do convert $file ${file%.*}.tif
#	echo $file
#	echo ${file%.*}.tif
#	./demo_tesseract ${file%.*}.tif ./eng_jpg/result.txt eng
	do ./demo_tesseract ${file} ./eng_jpg/result.txt eng 
done


