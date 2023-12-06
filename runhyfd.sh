#!/bin/bash
for FILE in dataset/*.csv; do
	echo "$FILE\n"
	python hyfd/hyfd.py -i $FILE
done