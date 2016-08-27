#! /bin/bash

cd ./lib
for file in *.a
	do ar x ${file} 
done

mv *.o ./tmp
cd ./tmp
ar cru libocr_tesseract.a *.o
mv libocr_tesseract.a ../
rm -rf *
cd ..


