#! /bin/bash

export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata
export LD_LIBRARY_PATH=/home/cloud/cloud-git-master/practice/tesseract/imagemagick/c_demo:$LD_LIBRARY_PATH
if [ -f ./chi_jpg/result.txt ]; then
	rm -rf ./chi_jpg/result.txt
fi

for file in ./chi_jpg/*.jpg
#	do convert $file ${file%.*}.tif
#	echo $file
#	echo ${file%.*}.tif
#	./demo_tesseract ${file%.*}.tif ./chi_jpg/result.txt chi_sim
	do ./demo_tesseract $file ./chi_jpg/result.txt chi_sim
done


