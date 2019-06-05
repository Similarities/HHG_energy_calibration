__author__ = 'similarities'


import numpy as np
import matplotlib.pyplot as plt
import os


import time


path_picture = "20190123/"

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

    def __init__(self, liste, binsize):

        self.liste = liste

        self.number = len(liste)

        self.numerator = 0

        self.my_array = np.zeros([2048,2])

        self.filename = str

        self.result_binsize = binsize

        self.result_binned_array = np.array
        
        self.min_x = float
        
        self.max_x = float

        self.effiency_function = np.array

        self.calibrated = np.array



    def test_on_single_picture(self, path_single):

        # umschreiben mit object ersetzen
        # like def open_and_integrate(self.filename = bestimmtes argument, dann muss man das nicht doppelt machen.)

        from grating_function_20190123 import Open_and_Plot_Picture

        my_picture_test = Open_and_Plot_Picture(path_picture+path_single, "nm", "counts")

        print(path_picture+path_single, "filepath to be opened")

        my_picture_test.open_file()

        my_picture_test.integrate_and_plot()

        my_picture_test.background()

        self.my_array = my_picture_test.grating_function()
        

        self.filename = str(path_single)[:-4]

        print(self.filename, path_single)



        from resize_bin_py3_class import resize_bins

        my_binned_spectrum_test = resize_bins(self.my_array, self.result_binsize, self.filename )



        self.result_binsize = my_binned_spectrum_test.minimum_bin()



        self.result_binned_array = my_binned_spectrum_test.shrink_subarray()



        self.max_x, self.min_x = my_binned_spectrum_test.range_of_spectrum()

        digit = my_binned_spectrum_test.find_digit_and_round(self.result_binsize)

        self.min_x = round(self.min_x,digit)

        self.max_x = round(self.max_x,digit)



        print(self.filename, self.max_x, self.min_x)

        # ausserhalb definieren.... muss als festes objekt da sein, nicht temporaer.







    def open_and_integrate(self):


        for x in range (0, self.number-1):

            from grating_function_20190123 import Open_and_Plot_Picture

            #print(self.number, x)
            my_picture = Open_and_Plot_Picture(path_picture+self.liste[x], "nm", "counts")

            print(path_picture+self.liste[x], "filepath to be opened")

            my_picture.open_file()

            my_picture.integrate_and_plot()

            my_picture.background()

            self.my_array = my_picture.grating_function()

            self.filename = str(self.liste[x])[:-4]

            #print(self.filename,x, self.liste[x])



            #my_picture.plot_HHG_800nm()


            #np.savetxt(self.liste[self.numerator - x]+".txt", my_array, delimiter=' ', fmt='%1.4e')   # use exponential notation



            from resize_bin_py3_class import resize_bins

            my_binned_spectrum = resize_bins(self.my_array,self.result_binsize, self.filename )

            self.result_binsize = my_binned_spectrum.minimum_bin()



            self.result_binned_array = my_binned_spectrum.shrink_subarray()



            #self.max_x, self.min_x = my_binned_spectrum.range_of_spectrum()

            #print(self.filename, self.max_x, self.min_x)

            self.calibrate_my_spectrum(efficiency_as_array)
            


        plt.show()




    def calibrate_my_spectrum(self, efficiency_as_array):
        
        #print(self.result_binned_array)

        if len(self.result_binned_array) == len(efficiency_as_array):

            self.calibrated = self.result_binned_array[:,1]*efficiency_as_array


            #print("spectrum with filename", self.filename, " has been calibrated")

            self.plot_my_result()



            return self.calibrated

        else:

            print("mismatch by overhang bin in length of array")
            print(len(self.result_binned_array), 'len my array')
            print(len(efficiency_as_array), 'len calibration array')


            #print("check accuracy: last entrys")
            #print(self.result_binned_array[-1,0], "to", self.result_binned_array[1,0])

            print("i will now delete last entry")

            if len(efficiency_as_array)> len(self.result_binned_array):

                efficiency_as_array = efficiency_as_array[0:-1]

            else:

                self.result_binned_array = self.result_binned_array[0:-1]


            self.calibrate_my_spectrum(efficiency_as_array)





            #print("difference now", len(self.result_binned_array)-len(efficiency_as_array))

            self.calibrate_my_spectrum(efficiency_as_array)

            #self.save_to_txt()


           # print(efficiency_as_array[-1,0], "to", efficiency_as_array[1,0])

    def plot_my_result(self):
        
        
            plt.figure(4)
            plt.plot(self.result_binned_array[:,0], self.result_binned_array[:,1])
            plt.xlabel("nm")
            plt.ylabel("photon number")
            plt.title(self.filename)
        
        



    def return_range_spectrum(self):

        return self.max_x, self.min_x


    def save_to_txt(self):
        
        np.savetxt("binned_spectrum"+ "_"+"bin_size"+ repr(self.result_binsize)+".txt", self.result_binned_array, fmt='%.3E', delimiter='\t')
        #print(self.result_binned_array[0:5], self.filename)
        
        
            
    def resulting_binsize(self):
        
        return self.result_binsize
        
        
        
        


class get_calibration:

    def __init__(self, wanted_binsize, max_x, min_x):

        self.result_binsize = wanted_binsize
        self.effiency_function = np.array
        self.max_x = max_x
        self.min_x = min_x




    def calc_calibration(self):



        from efficiency_function import calculate_efficiency_function

        function = calculate_efficiency_function(self.min_x, self.max_x, self.result_binsize)








        # bzw im gleichen Object... also oben erstmal umschreiben!
        self.effiency_function= function.get_efficiency_function()

        self.test_calculation()



        #print(self.result_binned_array[::,1]*self.effiency_function[::])
        #self.effiency_function = np.zeros([len(temp),1])
        #self.effiency_function[:] = temp[:]
        

        return self.effiency_function
    



    def test_calculation (self):

        if len(self.effiency_function) == 0:

            print("nothing was calculated")

        else:
            print("efficiency function was calculated")













        
        
# test and get x_max, x_min

#print(tif_files[7], ' bild nummer 1')

# batch_images_to_text(liste,binsize)
test1 = batch_images_to_txt(tif_files, 0.0001)
# test on single picture
test1.test_on_single_picture(tif_files[0])
minimum_binsize = test1.resulting_binsize()
x_max, x_min = test1.return_range_spectrum()
print(x_min, x_max, 'sprectral range rounded')


wanted_binsize = 0.06




calibration = get_calibration(wanted_binsize, x_max, x_min)
efficiency_as_array = calibration.calc_calibration()






print(wanted_binsize, "calibration binsize")


#print(len(efficiency_as_array))


batch1 = batch_images_to_txt(tif_files, wanted_binsize)

batch1.open_and_integrate()
binsize = batch1.resulting_binsize()

batch1.calibrate_my_spectrum(efficiency_as_array)
#fail muss allet in eine schleife!.
#batch1.save_to_txt()

