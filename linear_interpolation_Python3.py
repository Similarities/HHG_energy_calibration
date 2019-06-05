# -*- coding: utf-8 -*-
"""
Spyder Editor
#, usecols=(2,0)
#delimiter='\t'  # for tab, default: whitespace
This is a temporary script file.
"""
import numpy as np
import ntpath
import matplotlib.pyplot as plt
#from tkinter import filedialog as fd
import os




import ntpath
import matplotlib.pyplot as plt





class Load_text_into_2D_array:


    def __init__(self, filepath):




        self.file_name = str

        self.file_path = filepath

        self.loaded_array = np.empty([], dtype=np.float32)




    def ask_file_dialog(self):


        self.file_path = fd.askopenfilename()

        return self.file_path




    def path_leaf(self):


        ntpath.basename("a/b/c")

        head, self.file_name = ntpath.split(self.file_path)

        self.file_name = self.file_name[0:-4]

        #print(head,  " header")

        print("filename:", self.file_name)

        return self.file_name or ntpath.basename(head)




    def loadarray(self):

        ## Test first - by integers... bla
    #   reads column1 from txt / skips first rows (3),
        liste1=np.loadtxt(self.file_path, skiprows=(1), usecols=(0,))

        #reads column2 from txt / skips first rows (3)

        liste=np.loadtxt(self.file_path, skiprows=(1), usecols=(1,))
        #converts loaded column1 to an numpy array:

        matrix_x = np.array((liste1))

        #converts loaded column2 to an numpy array:

        matrix_y= np.array((liste))


        #joins the arrays into a 2xN array

        self.loaded_array= np.column_stack((matrix_x, matrix_y))

        self.loaded_array.view('i8,i8').sort(order=['f0'], axis=0)




        #print(self.loaded_array)

        return self.loaded_array







def plot_xy(array,colour,name, marker):
    plt.figure(1)
    x = array[:,0]
    y = array[:,1]
    plt.scatter(x, y, color=colour,label=name, marker = marker)
    #plt.legend(handles=[plot])
    plt.ylabel("input")







class Linear_interpolation:

    def __init__(self, resulting_binsize, array, filename, accuracy):

        self.resulting_binsize = resulting_binsize

        self.initial_array = array

        self.filename = filename

        self.delta_x = float(0.)

        self.temporal_array = np.zeros([1,2])

        self.sub_array = np.zeros([1,2])

        self.last_entry = np.zeros([1, 2])

        self.bin_number = int(0)

        self.smallstep = float(0)

        self.upper_bin = int(0)

        self.x = True

        self.accuracy = accuracy


        self.temp_test = float







    def checkbinsize(self):

        i=0

        N=len(self.initial_array)
        
        for x in range(0, len(self.initial_array)-1):
            
            temp = self.initial_array[x,0]

            
            self.initial_array[x,0] = round(temp,self.accuracy)
            

            
        #print(self.initial_array)



        while i < N-1:

            self.delta_x = self.initial_array[i+1]-self.initial_array[i]

            #print(self.delta_x[0,])

            #print(self.resulting_binsize, 'binsize')

            if self.delta_x[0,] <= self.resulting_binsize:
                
                #print(self.delta_x[0,])
                #print(self.resulting_binsize)

                i = i #None



            elif self.delta_x[0,] > self.resulting_binsize:



                # number of subbins - make integer/ round

                ratio = self.delta_x[0,]/self.resulting_binsize


                self.bin_number = int(round(ratio))
                #print(ratio, self.bin_number)

                # smallstep, value increase per sub bin // norm

                self.smallstep = self.delta_x[1,]/ratio


                # small shift for mismatch of initial points and resulting binsize
                # otherwise leads to small shifts by rounding at each initial point.
                self.temp_test = self.initial_array[i+1,0]-(self.initial_array[i,0]+self.bin_number*self.resulting_binsize)
                self.temp_test = round(self.temp_test, self.accuracy)
                self.initial_array[i+1,0] = (self.initial_array[i,0]+self.bin_number*self.resulting_binsize)








                #extract submatrix (upper point)

                self.upper_bin = self.initial_array[i]




                #print( "subarray", i, "between bin", self.upper_bin, "how many", self.bin_number)

                # overhang test:
                #print("initial bin +1 to theoretical", self.initial_array[i+1,0]-(self.initial_array[i,0]+self.bin_number*self.resulting_binsize))


                # calls "subbarray" - that gives a new subarray with number "ratio"

                  # elements, values are increasing per "increment" with "smallstep"

                self.sub_array = self.sub_arraying()

                #joins new subbarrays (and these include the original points)

                self.temporal_array = np.concatenate((self.sub_array, self.temporal_array))

                self.temporal_array.view('i8,i8').sort(order=['f0'], axis=0)



            else:

                if self.x is True:

                    self.sub_array.view('i8,i8').sort(order=['f0'], axis=0)

                    self.x = False

                    i = 0

                elif self.x is False:

                    print ("ERROR !!!! resulting_ binsize bigger than input binsize")

                    self.error_message()

                    i = N-1

                    return None


            i = i + 1

        #print(self.temporal_array, "result before last entry")




        #last entry (missing otherwise)


        self.last_entry_array()


        #print(self.temporal_array[len(self.temporal_array)-1,], "hezy ho last eintrag")

        #print(self.temporal_array, 'result')



        plot_xy(self.temporal_array,"c",str(self.resulting_binsize), marker = "+",)

        plot_xy(self.initial_array, "r", "input_data", marker = ".")

        plt.title(self.filename)

        plt.legend()

        
        #plt.savefig(self.filename+ "binned" +".png",  bbox_inches="tight", dpi = 1000)

        plt.show()

        return self.temporal_array
    
    
    

    def error_message(self): ##?
        self.resulting_array = np.zeros([1,2])

        return self.temporal_array


    def last_entry_array(self):

        self.last_entry [0,0] = self.initial_array[-1,0]

        self.last_entry [0,1] = self.initial_array[-1,1]

        #print(self.last_entry, "last entry", self.temporal_array[-1,0])




        self.delta_x = self.last_entry[0,] - self.temporal_array[-1,]

        #print(self.delta_x, "abstand zum letzten bin", self.last_entry[0,] , self.temporal_array[-1,0])

        ratio = self.delta_x[0,]/self.resulting_binsize

        self.bin_number = int(round(ratio))+1


        self.smallstep = self.delta_x[1,]/ratio

        # test
        #print(self.bin_number, ratio, self.smallstep, self.bin_number*self.resulting_binsize+self.temporal_array[-1,0])


        self.upper_bin = self.temporal_array[-1,]


        self.sub_array = self.sub_arraying()

        #joins new subbarrays (and these include the original points)

        self.temporal_array = np.concatenate((self.sub_array, self.temporal_array))

        self.temporal_array.view('i8,i8').sort(order=['f0'], axis=0)

        self.temporal_array = np.delete(self.temporal_array,0, axis=0)

        self.temporal_array = np.delete(self.temporal_array,-2, axis=0)




        return self.temporal_array








    def sub_arraying(self):

    #ratio = int, increment = float (binsize that should be reached),

    #excerpt= matrixelement  to be started (lower limit), 2D



        zwischen = np.zeros([self.bin_number, 2])

        x=self.upper_bin[0,]



        v=self.upper_bin[1,]


        for i in range(0, self.bin_number):

            zwischen[i,0]=x + i* self.resulting_binsize

            zwischen[i,1]=v + i* self.smallstep


        #print(zwischen)

        return zwischen



    def save_result(self):

        np.savetxt(self.filename + "_interpolation_binsize"+"_"+ repr(self.resulting_binsize) +".txt", self.temporal_array,fmt='%.3E', delimiter='\t')

        print ("length of old array", len(self.initial_array))

        print ("length of new array", len(self.temporal_array))

        return str(self.filename + "_interpolation_binsize"+"_"+ repr(self.resulting_binsize) +".txt")






#Test1 = Load_text_into_2D_array()
#Test1.ask_file_dialog()
#filename = Test1.path_leaf()
#initial_array = Test1.loadarray()

#resulting_binsize = 0.6


#interpolate_2 = Linear_interpolation(resulting_binsize, initial_array, filename)
#interpolate_2.checkbinsize()
#interpolate_2.save_result()

        