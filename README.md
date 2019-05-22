# batch_lists
batch_list_all_pics_in_folder 


what it does:
opens all .tif files from given filepath. 
(here in this example the array size is fixed to 2048x2048, 16bit pictures, implementation for
various file formats is still missing)
our batchlist (going through the folder 1x time) - 
first does some background substraction from a mean value calculation at a fixed range in picture 
(Right side in the picture, found in the grating function...py in the def background_substration), 
.. then:
integrates over one axis (x) of the picture - result: list
creates from the integer (px) an x-axis with a non constant scaling
via the grating function.

The so converted picture became an array of DIM 2048x2 which due to the x-axis scaling
it might now have non-equidistant bins.
Our converted array is now checked for resizing the binnings to a equidistant ones.
Prerequisite is, in order to avoid subsampling and by this alias or an increase of
resolution that is not there: the maximum bin-size in our array limits the resulting
binsize. The programm checks for this, and if the chosen binsize (called self.result_binsize)
is to small, it will be set automatically to the maximum bin_size of our array (rounded on one digit accuracy).
After this the x-axis and accordingly the y-axis are redistributed to the new binning range.
(method description can be found in "2f-binning-III_nonlinear..."- repository. 
In the end, the converted - resized array is automatically saved (unfortunatly still in the
same folder).


Python 3.x //
import py in py //
class orientated //
