#!/bin/bash

#Note: This code was tested mainly with python3, although it will also work with python2

input=./input/h1b_input.csv
output1=./output/top_10_occupations.txt
output2=./output/top_10_states.txt

./src/Driver.py $input $output1 $output2
