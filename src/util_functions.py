#!/usr/bin/env python
#util_functions.py. Written for 2018 Data Insight Engineering Challenge

#RMS Nov 2018

import os


def check_output_file(output_file):

    '''
    Check if output directory exists

    INPUT: Path to output file
    OUTPUT: Either an error or the output file name
    '''

    output_directory = '/'.join(output_file.split('/')[:-1])

    if not os.path.exists(output_directory):

        raise ValueError("Outut directory %s does not exist" %output_directory)

    return output_file

def check_input_file(input_file):

    '''
    Check if input file exists

    INPUT: Path to input file
    OUTPUT: Either an error or the input file name
    '''

    if not os.path.isfile(input_file):

        raise ValueError("Could not find input file %s" %input_file)

    return input_file


def get_column_headers(input_file,column_keywords):

    '''
    Look at the first line in the file and extract column names to use

    INPUT: filename, list of column keywords
    OUTPUT: file delimiter, list of column names to use from the file, list of their indices
    '''

    #Read the first line in the file
    with open(input_file) as f:
        first_line = f.readline()

    #Get the delimiter between the columns
    delim = first_line[0]

    #Print a warning if the delimiter is not a ';'
    if delim != ';':
        print("Warning: Found a delimiter of %s. The code will proceed, but expected \
        a delimiter of ;" %delim)

    #Determine the indices of the columns in the order of the keywords list
    first_line = first_line.split(delim)

    used_colnames = []
    used_colname_indices = []

    for name in column_keywords:
        for header in first_line:
            if name in header:
                used_colnames.append(header)
                used_colname_indices.append(first_line.index(header))

    return delim, used_colnames,used_colname_indices


