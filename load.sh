#!/bin/bash

for i in `seq 1 10`;
do
	http POST http://localhost:5000/add/ example=$i
done   
