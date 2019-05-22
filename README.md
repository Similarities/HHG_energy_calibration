# batch_lists
batch_list_all_pics_in_folder 


what it does:
opens all .tif files from given filepath. 
In a batchlist (going through the folder 1x time) - 
first the backgroundsubstraction, integration over one axis of the picture
and the renormalization of the x-Axis from px to nm (grating function) is done. 
The so converted picture became an array of DIM 2048x2 which due to the x-axis calibration
might now have non-equidistant bins (refering to the units of the x-axis and assuming
the grating function to not be constant with the px). 
Our converted array is now checked for resizing the binnings to a equidistant ones.
Prerequisite is, in order to avoid subsampling and by this alias or an increase of
resolution that is not there: the maximum bin-size in our array limits the resulting
binsize. The programm checks for this, and if the chosen binsize (called self.result_binsize)
is to small, it will be set to the maximum bin_size of our array (rounded on one digit accuracy).
After this the x-axis and accordingly the y-axis are redistributed to the new binning range.
(method description can be found in "2f-binning-III_nonlinear..."- repository. 
In the end, the converted - resized array is automatically saved (unfortunatly still in the
same folder).

Python 3.x 
import py in py
class orientated 
