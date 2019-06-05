# batch_lists
batch_list_all_pics_in_folder 


what it does:
opens all .tif files from given filepath. 
(here in this example the array size is fixed to 2048x2048, 16bit pictures, implementation for
various file formats is still missing)
our batchlist, treats all pictures in the given folder.

The main programm, tries to evulate the wanted binsize and
in one picture found possible minimum binsize.
It tests the given calibration files for their spectral range, if 
sufficient for the range determined in one picture.

The efficiency is calculated from the given 3 calibration files 
- using a linear interpolation on the wanted binsize. If in 
the calibration files the binsize is already smaller then the 
wanted binsize: the programm can not (yet) proceed.
The range of the efficiency array is resized to the spectral
range of the picture.

with the pictures in the folder (or list) 
 some background substraction is done from a mean value calculation 
(Right side in the picture, found in the grating function...py in the def background_substration), 
.. then:
integrates over one axis (x) of the picture - result: list
creates from the integer (px) an x-axis with a non constant scaling
via the grating function.

The so converted picture became an array of DIM 2048x2 which due to the x-axis scaling
it might now have non-equidistant bins.
Our converted array is now checked for resizing the binnings to a equidistant ones.
Prerequisite is, in order to avoid subsampling and by this alias or an increase of
resolution that is not there: the maximum bin-size*1.5* in our array limits the resulting
binsize. The programm checks for this, and if the chosen binsize (called self.result_binsize)
is to small, it will be set automatically to the maximum bin_size of our array (rounded on one digit accuracy).
After this the x-axis and accordingly the y-axis are redistributed to the new binning range.
(method description can be found in "2f-binning-III_nonlinear..."- repository. 

The programm further checks now the dimensions of the efficiency array 
and the integrated spectrum, since the starting value could possibly be
shifted by 0.5 binsize and hence has one more bin then the efficiency 
function. (Same accounts for the three different calibration functions, 
and here some improvement is needed)
- After all of this the integrated spectrum is multiplied with the 
efficiency array, plots generated.


Python 3.x //
import py in py //
...still in progress...
