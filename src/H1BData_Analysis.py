#!/usr/bin/env python
#H1BData_Analysis.py. Written for 2019 Data Insight Engineering Challenge

#RMS Nov 2018

import time
import util_functions as util
from DataObject import H1BDataObject

class H1Bdata():

	'''
	Base class for H1B data exercice 
	This is used to load the data and calculate the metrics specific to the exercise
	'''

	def __init__(self,inputfilepath,verbose=True):

		self.inputfile = inputfilepath

		#Check that the input file exists
		self.allfileslist = util.check_input_file(self.inputfile)
		self.verbose = verbose

		#List of keywords in the columns we want to preserve. All of the files 
		#we might load contain the same information, but the column headers may 
		#be different or in different locations. This list enables the code to 
		#select the appropriate columns
		self.colnames = ['STATUS','VISA_CLASS','SOC_CODE','SOC_NAME',\
		'WORKLOC1_STATE','WORKSITE_STATE']

		#List of valid state identifiers
		self.states = ['HI','AK','WA','OR','CA','ID','NV','AZ','UT','WY','MT'\
		,'CO','NM','TX','OK','KS','NE','SD','ND','MN','IA','MO','AR','LA','MS'\
		,'TN','KY','IL','WI','MI','IN','OH','AL','FL','GA','SC','NC','VA','WV'\
		,'DC','MD','NJ','CT','RI','MA','PA','NY','VT','NH','ME','DE']

		#List of valid visa classes (from the problem description)
		self.visa_classes = ['H-1B','H-1B1','E-3']


	def loaddata(self):

		'''
		Read the input file and load relevant data into a dictiionary
		'''

		delim, self.column_headers, self.column_header_indices \
		= util.get_column_headers(self.inputfile,self.colnames)


		if self.verbose == True:
			print('-------------------------------------------')
			print('Target col names: %s' %self.column_headers)
			print('Target col indices: %s' %self.column_header_indices)
			print('-------------------------------------------')

		#Read all data from input file into memory
		infile = open(self.inputfile)
		all_lines = infile.readlines()
		infile.close()

		#Preallocate dictionary containing all the data
		#This is done for efficiency and to ensure that the rows get read in
		#in the correct order
		alldata = {}
		for name in self.column_headers:
			alldata[name] = [None]*(len(all_lines)-1)

		#Load just the data we need into the dictiionary structure that we just made
		if self.verbose == True:
			t1 = time.time()
			print("Loading data from file %s" %self.inputfile) 

        #This counter keeps track of the number of entries read in so that
        #the preallocated list can be filled

		i = 0
		#Keep track of the total number of certified visa holders
		self.total_certified = 0

		for line in all_lines[1:]:
		    vals = line.split(delim)
		    status = vals[self.column_header_indices[0]]
		    visa_class = vals[self.column_header_indices[1]].split(' ')[0]
		    soc_code = vals[self.column_header_indices[2]]
		    soc_name = vals[self.column_header_indices[3]]
		    workstate = vals[self.column_header_indices[4]].strip()

		    #This conditional is included to ensure that only clean data is read into the dictionary structure
		    #The advantage of this is that it makes later processing stages more straightforward. However, a small
		    #number of entries might be missed if their rows are not in this format 
		    if (status == "CERTIFIED") and (len(soc_code)==7) and (visa_class in self.visa_classes) and (workstate in self.states):
		            alldata[self.column_headers[0]][i] = status
		            alldata[self.column_headers[1]][i] = visa_class
		            alldata[self.column_headers[2]][i] = soc_code
		            alldata[self.column_headers[3]][i] = soc_name.replace('"','')
		            alldata[self.column_headers[4]][i] = workstate
		            self.total_certified += 1 
		    i += 1

		if self.verbose == True:
			#Rough estimate of the data load time
			t2 = time.time()
			print("Load time: %.1fs" %(t2-t1))

		#Generate a H1BDataObject, which is a container for this data structure 

		self.loaded_H1Bdata = H1BDataObject(alldata)

	def report_top_occupations(self,outfile):

		'''
		Write a file of the top 10 occupations in the format specified

		INPUT: path to the file to be written

		'''

		if self.loaded_H1Bdata is None:

			raise ValueError("No data loaded! Run loaddata() before reporting top occupations")

		if self.verbose == True:
			print("Writing file of top occupations")

		outfile = util.check_output_file(outfile)

		#Count the number of instances for each SOC code
		counts_by_SOC_code = self.loaded_H1Bdata.group_by_count(self.column_headers[2])

		#Because we need to handle ties correctly, we first generate lists of occupations
		#and their associated counts. Note the use of the negative value of count to ensure 
		#that the final order is preserved. Occupations and counts will be lists of length 10

		occupations = []
		counts = []

		for code in list(sorted(counts_by_SOC_code, key=counts_by_SOC_code.get, reverse=True))[:10]:

			code_index = self.loaded_H1Bdata.alldata[self.column_headers[2]].index(code)
			occupation_name = self.loaded_H1Bdata.alldata[self.column_headers[3]][code_index]
			count_current = counts_by_SOC_code[code]
			occupations.append(occupation_name)
			counts.append(-count_current)

		#Open the output file and write headers

		top_occupations_file = open(outfile,'w')
		top_occupations_file.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')

		#Sort the lists so that they can be output to file in the correct order
		
		for occupation_name,count in sorted(zip(occupations,counts),key=lambda x: (x[1],x[0]),reverse=False):
			#print(occupation_name,count)
			top_occupations_file.write('%s;%i;%.1f%%\n' %(occupation_name,-count,\
				-100*count/self.total_certified))

		top_occupations_file.close()

	def report_top_states(self,outfile):

		'''
		Write a file of the top 10 states in the format specified

		INPUT: path to the file to be written

		'''

		if self.loaded_H1Bdata is None:

			raise ValueError("No data loaded! Run loaddata() before reporting top occupations")

		if self.verbose == True:
			print("Writing file of top states")

		outfile = util.check_output_file(outfile)

        #Count the number of instances for each state
		counts_by_state= self.loaded_H1Bdata.group_by_count(self.column_headers[4])

		#Because we need to handle ties correctly, we first generate lists of occupations
		#and their associated counts. Note the use of the negative value of count to ensure 
		#that the final order is preserved. States and counts will be lists of length 10.

		states = []
		counts = []

		for state in list(sorted(counts_by_state, key=counts_by_state.get, reverse=True))[:10]:

			states.append(state)
			counts.append(-counts_by_state[state])

		#Open the output file and write headers

		top_states_file = open(outfile,'w')
		top_states_file.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')

		#Sort the lists so that they can be output to file in the correct order

		for state,count in sorted(zip(states,counts),key=lambda x: (x[1],x[0]),reverse=False):
			top_states_file.write('%s;%i;%.1f%%\n' %(state,-count,\
				-100*count/self.total_certified))

		top_states_file.close()









