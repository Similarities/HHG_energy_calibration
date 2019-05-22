# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:59:57 2017

@author: similarities
"""

import numpy as np
from tkinter import filedialog as fd
import os




import ntpath
import matplotlib.pyplot as plt





class Load_text_into_2D_array:


    def __init__(self):




        self.file_name = str

        self.file_path = str

        self.loaded_array = np.empty([], dtype=np.float32)




    def ask_file_dialog(self):


        self.file_path = fd.askopenfilename()

        return self.file_path




    def path_leaf(self):


        ntpath.basename("a/b/c")

        head, self.file_name = ntpath.split(self.file_path)

        print(head,  " header")

        print("filename:", self.file_name)

        return self.file_name or ntpath.basename(head)




    def loadarray(self):

        ## Test first - by integers... bla
    #   reads column1 from txt / skips first rows (3),
        liste1=np.loadtxt(self.file_path, skiprows=(4), usecols=(0,))

        #reads column2 from txt / skips first rows (3)

        liste=np.loadtxt(self.file_path, skiprows=(4), usecols=(1,))
        #converts loaded column1 to an numpy array:

        matrix_x = np.array((liste1))
        #converts loaded column2 to an numpy array:

        matrix_y= np.array((liste))


        #joins the arrays into a 2xN array
        self.loaded_array= np.column_stack((matrix_x, matrix_y))

        self.loaded_array.view('i8,i8').sort(order=['f0'], axis=0)


        # Testcase: not empty, no strings or else.... bit number size

        print(self.loaded_array)

        return self.loaded_array






class resize_bins:



    def __init__(self, initial_array, result_binsize, filename):

        self.result_binsize = result_binsize # increment in old version
        self.initial_array = initial_array
        self.copy_initial = np.copy(self.initial_array)
        self.delta_bin = float
        self.case = bool
        self.test = np.zeros([len(self.initial_array),1])
       # print(self.test)
        self.error_switch = True
        self.restmatrix = np.array
        self.result_matrix = np.array
        self.filename = filename



    def minimum_bin(self):


        #N = len(self.initial_array)

        minsize = self.result_binsize

        i = 0
        while i < len(self.initial_array)-2:

            self.test[i] = self.initial_array[i+1,0]-self.initial_array[i,0]

            i = i + 1



        for x in range (0, len(self.test)-1):

            if self.test[x] >   self.result_binsize:
                error_switch = True

                print ("binsize too small")


            else:
                error_switch = False





        possible_binsize = np.amax(self.test, axis = 0)
        #print(np.amin(test, axis=0), 'minimum')

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

        print(x, "davor")

        x = len(str(x).split(".")[1])

        print(x, "watn das?")

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

                restx = old-self.initial_array[i,0]

                rest2 = (restx/self.result_binsize)*self.initial_array[i,1]

                #print "rest 2 x und y", restx, rest2
                #matrix[i,1]=(1-restx)*matrix[i,1]

                self.initial_array[i,1] = self.initial_array[i,1]-rest2

                self.initial_array[i+1,1] = self.initial_array[i+1,1]+rest2

                self.initial_array[i+1,0] = self.initial_array[i+1,0]+restx

                #print "corrected bin point i+1", matrix[i+1]
                #print "corrected bin point i", matrix[i]

                i=i+1




            elif self.case == 1 and len(self.initial_array)-i>=2:
                # macht weiter
                #wahlweise low=matrix[i-1,0]
                 # arr2 = matrix[i]+matrix[i+1] - matrix[i,0]

                sum_value=self.initial_array[i,1]+self.initial_array[i+1,1]

                 #print (matrix[i,1],"+",matrix[i+1,1], "=",sum_value)
                self.initial_array[i,1]=sum_value

                shrinked_y=self.initial_array[i+1,0]

                self.initial_array[i,0]=shrinked_y

                #print "deleted:", matrix[i+1,]
                self.initial_array=np.delete(self.initial_array,i+1, 0)


                #print ("i", i)

            else:

                print ("stopp")

                print ("letztes bin:", self.delta_bin)

                rest = len(self.initial_array)-i

                self.restmatrix = self.extract_subarray(i,N)



                print (self.restmatrix, "rest matrix")

                restmatrix = self.sum_extracted()

                endbin = len(self.initial_array)-rest

                self.result_matrix = self.initial_array[0:endbin,0:endbin]

                self.result_matrix = np.concatenate((self.result_matrix,restmatrix))

               # print_to_file(matrix,self.initial_array)

                #print "size of new matrix", len(matrix)

                #print (matrix)


                #self.plot_xy("c")

                i=N

                return self.result_matrix

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





    def print_to_file(self):
        #print ("now to file")
        np.savetxt(filename +"_"+ repr(self.result_binsize)+".txt", self.result_matrix[:], fmt='%.3E', delimiter='\t')



    


    

        

    

    
        




#Test1 = Load_text_into_2D_array()
#Test1.ask_file_dialog()
#filename = Test1.path_leaf()
#intial_array = Test1.loadarray()

#resize_me = resize_bins(intial_array, 1.2, filename)
#resize_me.minimum_bin()
#resize_me.shrink_subarray()
#resize_me.plot_array()
#resize_me.print_to_file()




