__author__ = 'similarities'


import numpy as np
from tkinter import filedialog as fd
import ntpath
import matplotlib.pyplot as plt
import os
import glob

path_picture = "rotated/"
save_path = "results/"
tif_files = []
counter = 0


for file in os.listdir(path_picture):
    try:

        if file.endswith(".tif"):
            #print ("picture found:", file)
            tif_files.append(str(file))
            counter = counter + 1

        else:
            print("only other files found")

    except Exception as e:
        raise e
        print("not files found here")
    #print(counter)


print(tif_files)
print(len(tif_files))

class batch_images_to_txt:

    def __init__(self, liste):
        self.liste = liste
        self.number = len(liste)
        self.numerator = 0
        self.my_array = np.zeros([2048,2])
        self.filename = str
        self.result_binsize = 0.00001
        self.result_binned_array = np.array

    def open_and_integrate(self):
        for x in range (0, self.number-1):

            from grating_function_20190118 import Open_and_Plot_Picture
            my_picture = Open_and_Plot_Picture(path_picture+self.liste[self.numerator - x], "nm", "counts")
            my_picture.open_file()
            my_picture.integrate_and_plot()
            my_picture.background()
            self.my_array = my_picture.grating_function()

            self.filename = str(self.liste[self.numerator - x])[:-4]
            print(self.filename)

            #my_picture.plot_HHG_800nm()


            #np.savetxt(self.liste[self.numerator - x]+".txt", my_array, delimiter=' ', fmt='%1.4e')   # use exponential notation
            from resize_bin_py3_class import resize_bins

            my_binned_spectrum = resize_bins(self.my_array,self.result_binsize, self.filename )
            self.result_binsize = my_binned_spectrum.minimum_bin()
            my_binned_spectrum.minimum_bin()
            self.result_binned_array = my_binned_spectrum.shrink_subarray()

            #resize_me.plot_array()
            my_binned_spectrum.print_to_file(self.filename)
            #np.savetxt(self.filename +"_"+ str(self.result_binsize)+".txt", self.result_binned_array, fmt='%.3E', delimiter='\t')





           # self.integrated[i,0] = f(x)*self.integrated[i,0]
           # create new x array: make 2D array






batch1 = batch_images_to_txt(tif_files)
batch1.open_and_integrate()

from resize_bin_py3_class import resize_bins
#obj = resize_bins(intial_array, 1.2, filename)

#resize_me = resize_bins(intial_array, 1.2, filename)
#resize_me.minimum_bin()
#resize_me.shrink_subarray()
#resize_me.plot_array()
#resize_me.print_to_file()

#from grating_function_20190118 import Open_and_Plot_Picture

#Picture1=Open_and_Plot_Picture('rotated/spectro1__Fri Jan 18 2019_16.56.49_97.tif', 'nm', 'counts')
#Picture1.open_file()
#Picture1.integrate_and_plot()
#Picture1.background()
#Picture1.grating_function()
#Picture1.plot_HHG_800nm()
#Picture1.plot_HHG_8xxnm()
#Picture1.saving_to_txt("test_test")