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


#print(tif_files)

print(len(tif_files), "number of files found")


class batch_images_to_txt:

    def __init__(self, file, binsize):

        self.file = file

        #self.number = len(liste)

        self.numerator = 0

        self.my_array = np.zeros([2048,2])

        self.filename = str

        self.result_binsize = binsize

        self.result_binned_array = np.array
        
        self.min_x = float
        
        self.max_x = float

        self.effiency_function = np.array

        self.calibrated = np.array
        
        self.plot_number = 1



    def test_on_single_picture(self, path_single):

        # umschreiben mit object ersetzen
        # like def open_and_integrate(self.filename = bestimmtes argument, dann muss man das nicht doppelt machen.)

        from grating_function_20190123 import Open_and_Plot_Picture

        my_picture_test = Open_and_Plot_Picture(path_picture+path_single, "nm", "counts")

        #print(path_picture+path_single, "filepath to be opened")

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




        from grating_function_20190123 import Open_and_Plot_Picture


        my_picture = Open_and_Plot_Picture(self.file, "nm", "counts")

        #print(self.file, "filepath to be opened")

        my_picture.open_file()

        my_picture.integrate_and_plot()

        my_picture.background()

        self.my_array = my_picture.grating_function()

        self.filename = str(self.file)[10:-4]





            #my_picture.plot_HHG_800nm()


            #np.savetxt(self.liste[self.numerator - x]+".txt", my_array, delimiter=' ', fmt='%1.4e')   # use exponential notation



        from resize_bin_py3_class import resize_bins

        my_binned_spectrum = resize_bins(self.my_array,self.result_binsize, self.filename )

        self.result_binsize = my_binned_spectrum.minimum_bin()



        self.result_binned_array = my_binned_spectrum.shrink_subarray()



        self.max_x, self.min_x = my_binned_spectrum.range_of_spectrum()

            #print(self.filename, self.max_x, self.min_x)

        #self.calibrate_my_spectrum(efficiency_as_array)
        
        return self.result_binned_array
            







    def calibrate_my_spectrum(self, efficiency_as_array):
        
        #print(self.result_binned_array)

        if len(self.result_binned_array) == len(efficiency_as_array):
            print(self.filename)
            
            #print(self.result_binned_array[10,1],'before')

            #self.calibrated = self.result_binned_array[:,1]*efficiency_as_array[:]
            
           # print(efficiency_as_array[-16], 'non empty calibration')

            #print("spectrum with filename", self.filename, " has been calibrated")

            #print(self.calibrated[10], 'calculated')
            
            #self.save_to_txt()


            self.result_binned_array[:,1]= self.result_binned_array[:,1]*efficiency_as_array[:]


            #self.plot_my_result()

            return self.result_binned_array





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







            #print("difference now", len(self.result_binned_array)-len(efficiency_as_array))

            self.calibrate_my_spectrum(efficiency_as_array)

            #self.save_to_txt()


           # print(efficiency_as_array[-1,0], "to", efficiency_as_array[1,0])



           
    def convert_to_energy(self):
        
        self.result_binned_array[:,1] = self.result_binned_array[:,1]*(19.8E-17/self.result_binned_array[:,0])
        
        self.plot_number = self.plot_number
        
        self.plot_number = self.plot_number +1
        self.plot_my_result()
        
        plt.show()
        
        
        
        
        

    def plot_my_result(self):
        
        
            plt.figure(self.plot_number)
            plt.plot(self.result_binned_array[:,0], self.result_binned_array[:,1], label=self.filename, marker = '.')
            plt.xlabel("nm - binsize: "+str(self.result_binsize)+'nm')
            plt.ylabel("photon number")
            #plt.ylim(0,5.0E8)
            plt.title(self.filename)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #plt.show()
            
           # plt.savefig(self.filename+ "binned" +".png",  bbox_inches="tight", dpi = 1000)

        
        



    def return_range_spectrum(self):

        return self.max_x, self.min_x


    def save_to_txt(self):
        
        np.savetxt(self.filename + "binned_spectrum"+ "_"+"bin_size"+ repr(self.result_binsize)+".txt", self.result_binned_array, fmt='%.3E', delimiter='\t')
        #print(self.result_binned_array[0:5], self.filename)
        
        
            
    def resulting_binsize(self):
        
        return self.result_binsize
        
        
        
        


class get_calibration:

    def __init__(self, wanted_binsize, max_x, min_x, accuracy):

        self.result_binsize = wanted_binsize
        self.effiency_function = np.array
        self.max_x = max_x
        self.min_x = min_x
        self.lenght = float
        self.accuracy = accuracy




    def calc_calibration(self):



        from efficiency_function import calculate_efficiency_function

        function = calculate_efficiency_function(self.min_x, self.max_x, self.result_binsize, self.accuracy)
        



        self.effiency_function= function.get_efficiency_function()
        
       # self.accuracy = function.return_accuracy()
       # print(self.accuracy)

        self.length = (self.max_x - self.min_x)/self.result_binsize
        self.length = round(self.length,0)
        
        print('amount of bins in range', self.length)

        self.test_calculation()



        #print(self.result_binned_array[::,1]*self.effiency_function[::])
        #self.effiency_function = np.zeros([len(temp),1])
        #self.effiency_function[:] = temp[:]
        

        return self.effiency_function
    



    def test_calculation (self):

        if len(self.effiency_function) == 0:

            print("nothing was calculated")
            
            
        elif len(self.effiency_function) != self.length:
            print('mismatch of amounts of bins',self.length - len(self.effiency_function))
            print('compared to', self.min_x, self.max_x)

        else:
            print("efficiency function was calculated")




class Test_data_sets:
    
    def __init__(self, wanted_binsize, file):
        
        self.resulting_binsize = wanted_binsize
        self.min_x = float
        self.max_x = float
        self.file = file
        self.accuracy = int
        
        
    def minimum_binsize_possible(self):
        
        test_bin = batch_images_to_txt(file, wanted_binsize)
        test_bin.open_and_integrate()
        self.resulting_binsize = test_bin.resulting_binsize()
        #
        
        print(self.resulting_binsize, 'binsize used')
        
        self.min_x, self.max_x = test_bin.return_range_spectrum()

        print(self.min_x, 'self.min_x')
        
        return self.resulting_binsize
        

        
        
        
        
    def find_digit_and_round(self):

        x = 0
        first_digit = self.resulting_binsize
        if first_digit >1:

            print("first digit 0.", x, "times" )
            return None

        else:

            while first_digit <1:

                first_digit = first_digit*10
                x = x+1
                
            self.accuracy = x
            
        return self.accuracy
    




    def return_spectral_range(self):

        print(self.accuracy, "digit... here")
        
        self.max_x = round(self.max_x,self.accuracy)
        self.min_x = round(self.min_x, self.accuracy)
        
        return self.min_x, self.max_x
    
    
    
    
    def check_calibration_files(self, file):
        
        from efficiency_function import Prepare_efficiency_binning

        test_file = Prepare_efficiency_binning(self.resulting_binsize, file, self.min_x, self.max_x, self.accuracy)
        
        temp = test_file.open_file()


        
        minimum = temp[0,0]
        
        maximum = temp[-1,0]
        
        
        
        if minimum > self.min_x:
            
            print('range of file starts with too high value')
            
            
            
        elif maximum < self.max_x:
            
            print('range of file ends at too low value')
            
            
            
        else:
            
            print('filerange sufficient for file', file)
        
        
        
        #test_file.
        
        
        









        
        
# test and get x_max, x_min

#print(tif_files[7], ' bild nummer 1')

# batch_images_to_text(liste,binsize)


file = path_picture + tif_files[0]

wanted_binsize = 0.2



Test = Test_data_sets(wanted_binsize, file)
wanted_binsize = Test.minimum_binsize_possible()
accuracy_decimal = Test.find_digit_and_round()
print("accuracy", accuracy_decimal)

x_max, x_min = Test.return_spectral_range()


print('range of spectrum ', x_min, ' to ', x_max)

cam_file = 'Andor_CCD_gain32.txt'
grating_file = 'grating_efficiency_shimadzu.txt'
filter_file = '200nm_Al_filter.txt'

Test.check_calibration_files(cam_file)
Test.check_calibration_files(grating_file)
Test.check_calibration_files(filter_file)





print(wanted_binsize, "resulting binsiye is now")



calibration = get_calibration(wanted_binsize, x_max, x_min, accuracy_decimal)


efficiency_as_array = calibration.calc_calibration()







#print(wanted_binsize, "calibration binsize")


print(len(efficiency_as_array))
my_picture_list=tif_files[58:61]
my_picture_list =tif_files[33:36]
how_many_files = len(my_picture_list)

#print(how_many_files, 'how many files')


for x in range (0, how_many_files):
    
    
    file = path_picture+my_picture_list[x]
    
    #print(my_picture_list[x], 'iterator',x)
    
    
    batch1 = batch_images_to_txt(file, wanted_binsize)
    batch1.open_and_integrate()
    binsize = batch1.resulting_binsize()

    batch1.calibrate_my_spectrum(efficiency_as_array)
    
    batch1.plot_my_result()
    

    batch1.convert_to_energy()
    batch1.plot_my_result()
    
plt.show()



    
    
    
    

           