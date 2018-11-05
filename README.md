# 2018_Insight_Data_Engineering_Challenge
Solution to the 2018 Insight Data Engineering challenge

## Problem  

Given an input file containing columns of visa applicant information, this problem asks us to count the number of certified applicants within two groups, occupation and state. Each occupation has a unique SOC code, which is associated with a unique name. I interpreted 'state' to mean the state inwhich the applicant will work. After counting the number of certified applicants in each category, the task is to report the top 10 and sort them alphabetically in the case of ties.   

## Approach 

In my approach, the program reads a single file in the format provided (although it may have any delimiter, so long as the delimiters are in the correct positions). It locates the column headers relevant to the problem and reads just that data into a precallocated dictionary structure. During reading there are checks to ensure that each field is in the correct format, the visa is certified and is of type H1B, H1B1 or E3 (specified in the problem). There are a small number of rows in each example file where the information appears to have been incorrectly or inconsistently entered (a city name in the state column, for example). The code will ignore these cases.   

Some of the data files (those for years prior to 2015) contain multiple states per applicant, listed under the headers 'WORKLOC1_STATE','WORKLOC2_STATE' etc. (I did not see more than two of such columns, but three or more work states are possible). Other files contain just state, listed under the header 'WORKSITE_STATE'. For simplicity, and because the vast majority of applicants have a job in just one state, I choose only to count the states in the 'WORKLOC1_STATE' in the case where multiple columns are available. In order to be read in, the state ID must match a list of known state abbreviations.  

Some of the data files also have inconsistent column headers (for example 'CLASS' vs. 'VISA_CLASS'). The program contains a check to ensure the correct columns are being read via a list of 'column keywords'. This could easily be added to.  

Once the data had been read, the dictionary containing it is passed into a H1BDataObject, which has a method called group_by_count. This counts the number of occurrences in some group and returns a dictionary. Future methods could easily be added to extent functionality of this class.  

Once the counts per group have been obtained, the top ten groups and their associated counts are then written to a file.  

## Run 

To run the code, place a file named h1b_input.csv (with columns in the correct format) into the input directory. Running run.sh will produce the desired output in the directory ./output. There is a flag in the code called 'verbose', currently set to True, which will print helpful messages.  

## Tests 

This package comes with four tests.  

- test_1: The test created by the insight team    
- test_2: Test on a file containing the column names of the 2014 data  
- test_3: Test on a file with the columns in a different order  
- test_4: Test on a file with a different delimiter   
