# -*- coding: utf-8 -*-
"""
Created on 22 May 09:59:57 2019

@author: similarities
"""

import numpy as np
from tkinter import filedialog as fd
import os




import ntpath
import matplotlib.pyplot as plt





class resize_bins:



    def __init__(self, initial_array, result_binsize, filename):

        self.result_binsize = result_binsize # increment in old version
        
        self.initial_array = initial_array
        
        
       # print('initial array', self.initial_array.dtype)
        self.copy_initial = np.copy(self.initial_array)
        self.delta_bin = float
        self.case = bool
        self.test = np.zeros([len(self.initial_array),1])

        self.error_switch = True
        self.restmatrix = np.array
        self.result_matrix = np.array
        self.filename = filename

        self.rest2 = float
        self.restx = float
        self.order_ascending()

        self.accuracy = int
        
        self.max_x = float
        self.min_x = float
        
        self.ROI_on_result = np.array



    def order_ascending(self):

        self.initial_array.view('i8,i8').sort(order=['f0'], axis=0)

        self.copy_initial.view('i8,i8').sort(order=['f0'], axis=0)

        return self.initial_array




    def find_digit_and_round(self, number):

        x = 0
        first_digit = number
        if first_digit >1:
            print("first digit 0.", x, "times" )
            return None

        else:

            while first_digit <1:

                first_digit = first_digit*10
                x = x+1
        return x








    def minimum_bin(self):


        #N = len(self.initial_array)



        i = 0

        error_switch = True
        
        while i < len(self.initial_array)-2:

            self.test[i] = self.initial_array[i+1,0]-self.initial_array[i,0]

            i = i + 1




        for x in range (0, len(self.test)-1):

            if self.test[x] >   self.result_binsize:

                error_switch = False

                #print ("binsize too small")






            else:

                self.result_binsize = self.result_binsize


        if error_switch == False:

                print("resulting binsize must be > than maximum binsize in array")

                print("resulting binsize is set to minimum possible value with")
                print("accuracy of 1 digit")


                possible_binsize = np.amax(self.test, axis = 0)

                digit = self.find_digit_and_round(float(possible_binsize))

                self.result_binsize = round(float(possible_binsize),digit)*1.5

                print('set result_binsize.... to: ', self.result_binsize)




        else:
            self.result_binsize = self.result_binsize

        #print(self.result_binsize, "resulting binsize")

        return self.result_binsize






        if error_switch == True:

            print(possible_binsize, "possible minimum binsize = biggest binsize in dataset")

        else:

           print("minimum do-able binsize (= biggest bin in initial array):", possible_binsize)
           print("start resizing, with resulting binsize of:", self.result_binsize)




    def distance_to_next_bin(self):

            case1 = self.delta_bin

            if case1 > self.result_binsize:

           #print "over bin - case switch"
                return 0


            else:

             # print "shrink"
                return 1






    def shrink_subarray(self):

        x = repr(self.result_binsize)

        #print(x, "davor")

        x = len(str(x).split(".")[1])



        
        first_element=self.initial_array[0,0]

        self.initial_array[0,0]=round(first_element,x)

#       print "first bin", matrix[0]

        i=1

        N=len(self.initial_array)

        while i<=N:


            low=self.initial_array[i-1,0]

            high = self.initial_array[i,0]

            self.delta_bin = high-low

            #print ("delta_bin", self.delta_bin)

            #print ("neighbor borders", high,low)

           # METHOD CALL in class

            self.case = self.distance_to_next_bin()

            #print(self.case, "case")



            # case == 0 corresponds to delta_bin > result_bin
            # case == 1 corresponds to delta_bin < result_bin (will be added to next bin)
            # IN DETAIL, quite tricky... if 0 subdivides bigger binsizes
            # *possible overhang bin range*


            if self.case == 0 and len(self.initial_array)-i >= 2:

                old = self.initial_array[i,0]

                self.initial_array[i,0] = self.initial_array[i-1,0] + self.result_binsize

                self.restx = old-self.initial_array[i,0]


                self.rest2 = (self.restx/self.result_binsize) *self.initial_array[i,1]


                #print "rest 2 x und y", restx, rest2
                #matrix[i,1]=(1-restx)*matrix[i,1]

                self.initial_array[i,1] = self.initial_array[i,1]-self.rest2

                self.initial_array[i+1,1] = self.initial_array[i+1,1]+self.rest2

                self.initial_array[i+1,0] = self.initial_array[i+1,0]+self.restx

                #print "corrected bin point i+1", matrix[i+1]
                #print "corrected bin point i", matrix[i]

                i=i+1




            elif self.case == 1 and len(self.initial_array)-i>=2:



                sum_value=self.initial_array[i,1]+self.initial_array[i+1,1]

                #print (matrix[i,1],"+",matrix[i+1,1], "=",sum_value)
                self.initial_array[i,1]=sum_value

                shrinked_y = self.initial_array[i+1,0]

                self.initial_array[i,0]=shrinked_y

                #print "deleted:", matrix[i+1,]
                self.initial_array=np.delete(self.initial_array,i+1, 0)


                #print ("i", i)

            else:

                #print ("stopp")

                #print ("last bin:", self.delta_bin)

                rest = len(self.initial_array)-i

                self.restmatrix = self.extract_subarray(i,N)



                #print (self.restmatrix, "rest matrix")

                restmatrix = self.sum_extracted()

                endbin = len(self.initial_array)-rest

                self.result_matrix = self.initial_array[0:endbin,0:endbin]

                #self.result_matrix = np.concatenate((self.result_matrix,restmatrix))

                self.round_x_axis()

               # print_to_file(matrix,self.initial_array)

                #print "size of new matrix", len(matrix)

                #print (matrix)


                #self.plot_xy("c")

                i = N

                #print(self.result_matrix)
                
                self.range_of_spectrum()


                self.resize_range()
                
                #print(len(self.result_matrix), len(self.ROI_on_result))



                return self.ROI_on_result




    def extract_subarray(self, low, high):

        sub1x=low

        sub2x=high

        extracted = self.initial_array[sub1x:sub2x]

        return extracted



    def sum_extracted(self):

        N=len(self.restmatrix)

        i=0

        while i < N-1:


            self.restmatrix[i,1] = self.restmatrix[i,1] + self.restmatrix[i+1,1]

            self.restmatrix[i,0] = self.restmatrix[i+1,0]

            self.restmatrix = np.delete(self.restmatrix,i+1, 0)

            N = len(self.restmatrix)


        else:
            #print (self.restmatrix)

            return self.restmatrix


    # can be deleted... in superclass...

    def plot_xy(self, array, colour, marker, label):

        x = array[:,0]

        y = array[:,1]


        plt.figure(1)

        plt.scatter(x, y, color=colour, label = label, marker = marker)



        plt.ylabel(label)





    def plot_array(self):

        self.plot_xy( self.copy_initial, "b", ".", 'initial binning')


        self.plot_xy(self.result_matrix, "r",  "+", "bin size:"+str(self.result_binsize))

        plt.legend()

        plt.show()





    def print_to_file(self, filename):
        #print ("now to file")
        np.savetxt(filename +"_"+"bin_size"+ repr(self.result_binsize)+".txt", self.result_matrix, fmt='%.3E', delimiter='\t')




    def range_of_spectrum(self):

        a = self.result_binsize
        self.accuracy = self.find_digit_and_round(a)

        self.max_x = round(np.amax(self.result_matrix[:,0]), self.accuracy)

        self.min_x = round(np.amin(self.result_matrix[:,0]), self.accuracy)
        
        if self.min_x < 17:
            self.min_x = 17.5
            
        else:
            
            self.min_x = self.min_x



        #print('spectral range', self.max_x, 'to', self.min_x)

        return self.max_x, self.min_x
    
    
    
    
    
    
    
    def resize_range(self):


        index_up = np.amax(np.where(self.result_matrix[:,0] <= self.max_x))
        
        index_down = np.amin(np.where(self.result_matrix[:,0] >= self.min_x))
        

        
        
        #print(index_up,' index up, corresponding to x_max')
        #print(index_down, " index down, corresponding to x_min'")
        #print(index_up-index_down, "number of entries after range")


        self.ROI_on_result = self.result_matrix[index_down:index_up]
        #print(self.ROI_on_interpolated)




    def round_x_axis(self):

        for x in range(0,len(self.result_matrix-1)):

            a = self.result_binsize

            self.accuracy = self.find_digit_and_round(a)

            print(self.accuracy, self.result_matrix[x,0])

            temp = self.result_matrix[x,0]

            self.result_matrix[x,0] = round(temp, self.accuracy)

            return self.result_matrix

    


    

        

    

    





