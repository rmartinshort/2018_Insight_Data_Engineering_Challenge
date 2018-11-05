#!/usr/bin/env python
#Driver.py. Written for 2018 Data Insight Engineering Challenge

#RMS Nov 2018
#Driver code for H1B data exercise

from H1BData_Analysis import H1Bdata
import sys

def main():

	input_file = sys.argv[1]
	output_occupations = sys.argv[2]
	output_states = sys.argv[3]

	indata = H1Bdata(input_file)

	indata.loaddata()

	indata.report_top_occupations(output_occupations)
	indata.report_top_states(output_states)

if __name__ == '__main__':

	main()