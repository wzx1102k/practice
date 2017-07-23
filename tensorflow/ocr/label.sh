#! /bin/bash

i=1
for file in ./png/org/*.png
	do
		cp ${file} ./png/train/$i.png
		i=`expr $i + 1`
	done
