#!/usr/bin/env python
#DataObject.py. Written for 2018 Data Insight Engineering Challenge

#RMS Nov 2018

class H1BDataObject():

    '''
    Class for loaded H1BDataObject. This currenly only has one method,
    group_by_count, but could be easily extended to do other convenient 
    operations on the H1B data
    '''

    def __init__(self,input_data):

        self.alldata = input_data
        self.columns = list(input_data.keys())


    def group_by_count(self,column_header):

        '''
        Count the number of occurences in each group represented within column_header

        INPUT: A column header name 
        OUTPUT: A dictionary containing elements as keys and counts and entries
        '''

        if self.alldata == None:

            raise ValueError("No data loaded! Run loaddata() before reporting top occupations")

        groupcounts = {}

        for entry in self.alldata[column_header]:
            if (entry != None):
                if entry not in groupcounts:
                    groupcounts[entry] = 0
                groupcounts[entry] += 1

        return groupcounts


