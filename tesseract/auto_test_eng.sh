#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata

if [ -f ./eng_jpg/result.txt ]; then
	rm -rf ./eng_jpg/result.txt
fi

for file in ./eng_jpg/*.jpg
#	do convert $file ${file%.*}.tif
#	echo $file
#	echo ${file%.*}.tif
#	./demo_tesseract ${file%.*}.tif ./eng_jpg/result.txt eng
	do ./ocr_static_demo ${file} ./eng_jpg/result.txt eng 
	   ./ocr_share_demo ${file} ./eng_jpg/result.txt eng
done


