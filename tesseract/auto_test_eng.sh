#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata
export LD_LIBRARY_PATH=/home/cloud/cloud-git-master/practice/tesseract/imagemagick/c_demo:$LD_LIBRARY_PATH

if [ -f ./eng_jpg/result.txt ]; then
	rm -rf ./eng_jpg/result.txt
fi

for file in ./eng_jpg/*.jpg
#	do convert $file ${file%.*}.tif
#	echo $file
#	echo ${file%.*}.tif
#	./demo_tesseract ${file%.*}.tif ./eng_jpg/result.txt eng
	do ./demo_tesseract ${file} ./eng_jpg/result.txt eng 
done


