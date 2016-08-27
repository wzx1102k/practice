#! /bin/bash

if [ -d lib ]; then
	rm -rf lib
fi

chmod 777 ocr_tesseract_static.tar.gz
tar -zxvf ocr_tesseract_static.tar.gz

cd ./lib
for file in *.a
	do ar x ${file} 
done

mv *.o ./tmp
cd ./tmp
ar csru libocr_tesseract.a *.o
mv libocr_tesseract.a ../../
cd ../..
rm -rf lib

