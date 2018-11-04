#!/bin/bash


input=./input/h1b_input.csv
#input=./input/H1B_FY_2016.csv
output1=./output/top_10_occupations.txt
output2=./output/top_10_states.txt

./src/Driver.py $input $output1 $output2
