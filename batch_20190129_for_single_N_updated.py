

__author__ = 'similarities'


import numpy as np
import matplotlib.pyplot as plt
import os




class batch_images_to_txt:
    def __init__(self, file, binsize, description):
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
        self.xlabel = str
        self.ylabel = str
        self.plot_legend = str
        self.description = description
        self.energy_content = float

    def integration_unit_conversion(self):
        from grating_function_20190129 import GratingCalculationOnPicture
        self.xlabel = "nm"
        self.ylabel = "integrated counts"
        my_picture = GratingCalculationOnPicture(self.file, self.xlabel, self.ylabel)
        #print(self.file, "filepath to be opened")
        my_picture.open_file()
        my_picture.integrate_and_background()
        my_picture.background()
        self.my_array = my_picture.grating_function()
        self.filename = str(self.file)[17:-4]
        self.my_array = self.my_array[10:-20]
        plt.figure(10)
        plt.title("integrated and spectral calibrated")
        plt.plot(self.my_array[::,0], self.my_array[::,1])
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        return self.my_array


    def resize_my_bins(self):
        # call plot -- might be summarized via the plot call below... 2x!!!!
        #my_picture.plot_HHG_800nm()
        #np.savetxt(self.filename[self.numerator - x]+'_binned'+".txt", my_array, delimiter=' ', fmt='%1.4e')   # use exponential notation
        from resize_bin_py3_class import resize_bins
        my_binned_spectrum = resize_bins(self.my_array,self.result_binsize, self.filename )
        self.result_binsize = my_binned_spectrum.minimum_bin()
        self.result_binned_array = my_binned_spectrum.shrink_subarray()
        self.max_x, self.min_x = my_binned_spectrum.range_of_spectrum()
        my_binned_spectrum.plot_array()
        #print(self.filename, self.max_x, self.min_x)
        return self.result_binned_array


    def calibrate_my_spectrum(self, efficiency_as_array):
        #print(self.result_binned_array)
        if len(self.result_binned_array) == len(efficiency_as_array):
            #print(self.filename)
            self.xlabel = "nm with binsize: "+str(self.result_binsize) + "nm"
            self.ylabel = "Nphoton"
            self.result_binned_array[:,1]= self.result_binned_array[:,1]*efficiency_as_array[:]
            #self.plot_my_result()
            return self.result_binned_array

        else:
            #print("mismatch by overhang bin in length of array")
            #print(len(self.result_binned_array), 'len my array')
            #print(len(efficiency_as_array), 'len calibration array')
           # print("i will now delete last entry")
            if len(efficiency_as_array)> len(self.result_binned_array):
                efficiency_as_array = efficiency_as_array[0:-1]
            else:
                self.result_binned_array = self.result_binned_array[0:-1]
            #print("difference now", len(self.result_binned_array)-len(efficiency_as_array))
            self.calibrate_my_spectrum(efficiency_as_array)
            #self.save_to_txt()
           # print(efficiency_as_array[-1,0], "to", efficiency_as_array[1,0])
            return self.result_binned_array

           
    def convert_to_energy(self):
        self.result_binned_array[:,1] = self.result_binned_array[:,1]*(19.8E-11/self.result_binned_array[:,0])
        self.plot_number = self.plot_number
        self.plot_number = self.plot_number +1
        self.xlabel = 'nm with binning: '+str(self.result_binsize) +"nm"
        self.ylabel = "energy [uJ]"
        self.save_to_txt()
        return self.result_binned_array

    def plot_my_result(self, array):
            plt.figure(self.plot_number)
            plt.plot(array[:,0], array[:,1], label=self.description, marker = '.')
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            #plt.ylim(0,5.0E11S)
            plt.title(self.filename)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #plt.show()
            #plt.savefig(self.filename+ self.ylabel +".png",  bbox_inches="tight", dpi = 1000)
            #print(self.filename, "saved picture")

    def return_range_spectrum(self):
        return self.max_x, self.min_x

    def prepare_header(self):
        # insert header line and change index
        header_names = (['nm', 'muJ'])
        names = (['converted file:' + str(self.filename[20:]), "binning:" + str(self.result_binsize)])
        parameter_info = (
            ["integrated and resized binned spectra", "ROIsize spatial in px" + str(50) + ":" + str( 1600)])
    #result binned_array [x,y]
        return np.vstack((parameter_info, names, header_names, self.result_binned_array))

    def save_to_txt(self):
        result = self.prepare_header()
        #print(result)
        np.savetxt( "data/"+"20190129" + self.filename[20:-4] + "cal" + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')




    def resulting_binsize(self):
        return self.result_binsize
    
    def integrate_over_energy(self, boundary_Low, boundary_high):
        if boundary_Low == 0 or boundary_high == 0:
            print('no boundary range given: full range of spectra')
            boundary_Low, boundary_high = self.return_range_spectrum()
           # print ('spectral range to be integrated long to short', boundary_Low, boundary_high)

        from integrate_spectra import Integrate_energy
        print ('spectral range to be integrated', boundary_Low, boundary_high)
        #print(self.result_binned_array)
        integration = Integrate_energy(boundary_Low, boundary_high, self.result_binned_array)
        integration.resize_to_boundary()
        self.energy_content = integration.integrate_resized_array()
        return self.energy_content

class get_calibration:
    def __init__(self, wanted_binsize, max_x, min_x, accuracy, file_path_list):
        self.file_path_list = file_path_list
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
        self.length = (self.max_x - self.min_x)/self.result_binsize
        self.length = round(self.length,0)
        #print('amount of bins in range', self.length)
        self.test_calculation()
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
        self.file_name = file

    def minimum_binsize_possible(self):
        test_bin = batch_images_to_txt(file, wanted_binsize, "testfile")
        test_bin.integration_unit_conversion()
        test_bin.resize_my_bins()
        plt.close()
        self.resulting_binsize = test_bin.resulting_binsize()
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
    
    
    
    
    def check_calibration_files(self, file, bool):
        self.file_name = file[:-4]
        from efficiency_function import Prepare_efficiency_binning
        test_file = Prepare_efficiency_binning(self.resulting_binsize, file, self.min_x, self.max_x, self.accuracy)
        temp = test_file.open_file()
        # optional conversion from [eV] into [nm] by bool == False
        if bool == True:
            None
        else:
            print("convert from eV into nm for file: ", self.file_name)
            temp = test_file.eV_to_nm()
            header = np.zeros([1,2])
            new_calibration_file = np.concatenate((temp, header), axis=0)
            new_calibration_file.view('i8,i8').sort(order=['f0'], axis=0)
            #save calibration file
            np.savetxt(self.file_name+ "_"+" nm"+ ".txt", new_calibration_file, fmt='%.3E', delimiter='\t')
            self.file_name = self.file_name+ "_"+" nm"+ ".txt"

        minimum = temp[0,0]
        maximum = temp[-1,0]
        
        if minimum > self.min_x:
            print('range of file starts with too high value')
        elif maximum < self.max_x:
            print('range of file ends at too low value')
        else:
            print('filerange sufficient for file', file)

    def return_file_path(self):
        return self.file_name


def file_list_creater(liste_files_by_number, file_name_list):
    first_entry = liste_files_by_number[0]
    last_entry = liste_files_by_number[-1]
    file_name_list = file_name_list[first_entry-1:last_entry]
    #print("first_entry", file_name_list[0])
    for x in range (len(liste_files_by_number)-1):
        delete_neighbors = liste_files_by_number[x+1]-liste_files_by_number[x]
        #print(delete_neighbors, "delete -1 entries")
        next = x + delete_neighbors
        #print (next,"up to", x, "x")
        #print (len(liste_files_by_number), "len liste number")
        #print(len(file_name_list))
        if delete_neighbors == 1:
            file_name_list = file_name_list
            #print(file_name_list[x], "x entry")
        else:
            del file_name_list[x+1:next]
        #print(file_name_list)

    return file_name_list





plt.close()
path_picture = "data/rotated_20190129/"
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


print(len(tif_files), "number of files found")
#np.savetxt("Files"+".txt",tif_files, delimiter='\t')

        
        


file = path_picture + tif_files[10]

wanted_binsize = 0.1
Test = Test_data_sets(wanted_binsize, file)
wanted_binsize = Test.minimum_binsize_possible()
accuracy_decimal = Test.find_digit_and_round()
print("accuracy", accuracy_decimal)
x_max, x_min = Test.return_spectral_range()
print('range of spectrum ', x_min, ' to ', x_max)

cam_file = 'Andor_CCD_gain32.txt'
grating_file = 'grating_efficiency_shimadzu.txt'
filter_file = '200nm_Al_filter.txt'

Test.check_calibration_files(cam_file, False)
cam_file = Test.return_file_path()

print("new cam_file", cam_file)

Test.check_calibration_files(grating_file, True)
Test.check_calibration_files(filter_file, True)
file_path_list = [cam_file, grating_file, filter_file]
print(file_path_list, "liste")
print(wanted_binsize, "resulting binsize is now")
calibration = get_calibration(wanted_binsize, x_max, x_min, accuracy_decimal, file_path_list)
efficiency_as_array = calibration.calc_calibration()


#print(wanted_binsize, "calibration binsize")
print(len(efficiency_as_array))
#my_picture_list_numbers = (4,6, 24, 33, 43)
my_picture_list_numbers = list(range(1,len(tif_files)+1))
print(my_picture_list_numbers,'alle?')

my_picture_list = file_list_creater(my_picture_list_numbers, tif_files)
print(my_picture_list)

#my_file_description = ("#4 z = 0   RL", "#6 z = 3.2 RL", "#24 z = 4.8 RL", "#33 z = 5.6 RL", "#43 z = 6.4 RL", )
my_file_description = list( range(1, len(tif_files)+1))
how_many_files = len(my_picture_list)


print(how_many_files, 'how many files')
#energy range for N=25 evaluation (here +/-0.5 N)
boundary_high = 31.373
boundary_Low = 32.653
integrated_energy_list = []



for x in range (0, how_many_files):
    file = path_picture + my_picture_list[x]
    print(my_picture_list[x], 'iterator',x)
    description = my_file_description[x]
    batch1 = batch_images_to_txt(file, wanted_binsize, description)
    batch1.integration_unit_conversion()
    batch1.resize_my_bins()
    binsize = batch1.resulting_binsize()
    temp = batch1.calibrate_my_spectrum(efficiency_as_array)
    temp2= batch1.convert_to_energy()
    #integrated_energy_list.append(my_picture_list[x] + description + str(boundary_high) + str(boundary_Low) + ' :  ')
    #integrated_energy_list.append(batch1.integrate_over_energy(boundary_Low, boundary_high))
    #single harmonic number evaluation over the stack... resulting index is shotnumber
    integrated_energy_list.append(batch1.integrate_over_energy(boundary_Low, boundary_high))
    batch1.plot_my_result(temp2)

print(integrated_energy_list)    
np.savetxt("Energy_content_uJ"+'20190129_0.5N25'+".txt",integrated_energy_list, fmt='%.3E', delimiter='\t')
plt.show()




    
    
    
    

           