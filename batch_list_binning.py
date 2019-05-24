__author__ = 'similarities'


import numpy as np
import matplotlib.pyplot as plt
import os


path_picture = "rotated/"

save_path = "results/"

tif_files = []

counter = 0


for file in os.listdir(path_picture):

    try:

        if file.endswith(".tif"):


            tif_files.append(str(file))

            counter = counter + 1



        else:

            print("only other files found")

    except Exception as e:

        raise e

        print("not files found here")
    #print(counter)


print(tif_files)

print(len(tif_files), "number of files found")


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









batch1 = batch_images_to_txt(tif_files)

batch1.open_and_integrate()

