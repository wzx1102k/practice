#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata

if [ -f result.txt ]; then
	rm -rf result.txt
fi

for file in ./chi_jpg/*.jpg
	do convert $file ${file%.*}.tif
	echo $file
	echo ${file%.*}.tif
	./demo_tesseract ${file%.*}.tif ./chi_jpg/result.txt chi_sim
done


