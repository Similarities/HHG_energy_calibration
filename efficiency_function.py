__author__ = 'julia'

import numpy as np
import matplotlib.pyplot as plt
import os


import time

class Prepare_efficiency_binning:

    def __init__(self, binsize, file, x_min, x_max, accuracy):
        
        self.result_binsize = binsize
        
        self.filepath = file
        
        self.file_name = str
        
        self.calibration = np.array
        
        self.new_file_name = str

        self.interpolated = np.array
        
        self.ROI_on_interpolated = np.array

        self.min_x = x_min
        
        self.max_x = x_max
        
        self.accuracy = accuracy
        
        print(self.accuracy, 'prepare_efficiency')
        





    def open_file(self):

        from linear_interpolation_Python3 import Load_text_into_2D_array

        my_calibration = Load_text_into_2D_array(self.filepath)
        
        self.file_name = my_calibration.path_leaf()


        
        self.calibration = my_calibration.loadarray()
        
        
        return self.calibration
        

    def interpolate_linear(self):
       
        self.open_file()
        
        print(self.file_name, 'filename')
       
        from linear_interpolation_Python3 import Linear_interpolation

        interpolation = Linear_interpolation(self.result_binsize, self.calibration, self.file_name, self.accuracy)
        
        self.interpolated = interpolation.checkbinsize()



    def return_accuracy(self):
        

        print('accuracy in digit after 0', self.accuracy)


    def resize_range(self):


        index_up = np.amax(np.where(self.interpolated[:,0] < self.max_x))
        
        index_down = np.amin(np.where(self.interpolated[:,0] >= self.min_x))
        

        print(self.interpolated[index_up], self.interpolated[index_down])
        
        #print(index_up,' index up, corresponding to x_max')
        #print(index_down, " index down, corresponding to x_min'")
        #print(index_up-index_down, "number of entries after range")


        self.ROI_on_interpolated = self.interpolated[index_down:index_up]
        #print(self.ROI_on_interpolated)



        return self.ROI_on_interpolated



class calculate_efficiency_function:
    
    
    

    def __init__(self, min_x, max_x, result_binsize, accuracy):

        self.max_x = max_x
        self.min_x = min_x
        self.result_binsize = result_binsize
        self.accuracy = accuracy
        

        
        
    def return_accuracy(self):
        
        return self.accuracy
        
        
        

    def get_efficiency_function(self):

        
        
        

        camera = Prepare_efficiency_binning(self.result_binsize,'Andor_CCD_gain32.txt' , self.min_x, self.max_x, self.accuracy)
        counts_per_photon_path = camera.interpolate_linear()

        a = camera.resize_range()
        
        self.accuracy = camera.return_accuracy()




        grating = Prepare_efficiency_binning(self.result_binsize,'grating_efficiency_shimadzu.txt',self.min_x, self.max_x, self.accuracy)

        grating_efficiency_path = grating.interpolate_linear()

        b = grating.resize_range()
        
        

        np.savetxt("grating"+ "_"+"bin_size"+ repr(self.result_binsize)+".txt", b, fmt='%.3E', delimiter='\t')

        Al_filter = Prepare_efficiency_binning(self.result_binsize,'200nm_Al_filter.txt',self.min_x, self.max_x, self.accuracy)

        filter_efficiency_path = Al_filter.interpolate_linear()
        
        

        c = Al_filter.resize_range()


        print('compare amount of bins')
        print(len(a), " Camera", len(b), "grating", len(c), "Al_filter")
        
        
        # bad fix for overhang offset has to be improved!!!
        if len(a)+len(b) != 2* len(c):
            print('mismatch by overhang')
            
            c = c[:-1]
            b = b[: -1]
            
            print(len(a), " Camera", len(b), "grating", len(c), "Al_filter")
            self.effiency_function= a[::,1]/(b[::,1]*c[::,1])
            

        else:
            self.effiency_function= a[::,1]/(b[::,1]*c[::,1])
            


        # get out the x_ axis for comparison.

        #print(self.effiency_function, len(self.effiency_function))





        plt.figure(10)

        plt.scatter( a[::,0],self.effiency_function, color = "b", marker="x")
        plt.xlabel("nm")
        plt.ylabel("photons/counts")

        plt.show()






        return self.effiency_function




