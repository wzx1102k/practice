#! /bin/bash

if [ -d lib ]; then
	rm -rf lib
fi

chmod 777 ocr_tesseract.tar.gz
tar -zxvf ocr_tesseract.tar.gz

make clean; make lib

cd ./lib
for file in *.a
	do ar x ${file} 
done

mv ../*.o ./tmp
mv *.o ./tmp
cd ./tmp
ar csru libocr_tesseract.a *.o
mv libocr_tesseract.a ../../
cd ../..
rm -rf lib

make
rm -rf *.o

