#! /bin/bash

for file in $1/*
do
    python card.py $file $2/${file##*/}
done
