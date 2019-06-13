# batch_lists
batch_list_all_pics_in_folder 

This project is a further development of the so called 2-frequency binning project. This 
project now summarizes upsampling and downsampling for non-linear axis scaling. 
This proceedere is commmonly needed
when e.g. integrated pictures (spectra) have to be calibrated. Usually the spectra has 
a non-linear x-scaling, which is a consequence of the grating function. The calibration 
data set (e.g. measuring the sensitivity of a camera at different photon energies) usually
contains of less data points with a variable distance (binning) in the x-axis. As long
as the distance between these data points are much bigger than the binning size we 
want to achieve in the result: here the linear interpolation helps. 
In other words, the calibration should be taken place on the basis of array calculation
instead of fitted analytical functions. The reason lies in the complexity of the calibration
functions and needed accuracy, for which a fitting routine might lead into sector splitting... or
polynoms with too high which
is not what you want to do. So: the exercise is, to bring the calibration array (Nx2) to the
same dimension as the array that has to be calibrated (Nx2). Here the binning (distance between
adherent neighbour entry in the x-column) becomes the tricky part.



what it can do:

- opens and further calculates all .tif files from given filepath (16 bit, 2048x2048) 
- integrates picture over one dimension
- takes at the right side of the picture a background, substracts mean value
- rescales the x- axis according a function (spectrometer function)
- resizes the x-binning to equi-distant binning (down sampling)
- needs now 3 calibration files (2 colummn. txt) (e.g. camera, filter, grating)
- can transfer the calibration x-axis from eV to nm
- linearly interpolates the calibration files to the same binning as chosem for the picture (upsampling)
- calculates maximum range (spectrally) from the picture and resizes the calibration range accordingly
- multiplys the calibration to the integrated picture (spectrum)
- delivers the option to save separatly each file
- plots....
- has some earlier test routine if the sizes of e.g. calibration range is not sufficient
- has some test routiene if the binning size was chosen too small


what it cannot do:
- stops working if the input binning of the calibration files is smaller than the wanted one
... here a switch from  upsampling to downsampling would be needed
- it has no file dialog
- more testing - in case of alias-boarders
- a more accurate handling of overhang bins (at the moment just delets and by this shifts one or two)
- implementation for various file formats 

First the programm takes one (the first) picture from the batchlist and
assuming the others to be similar in all parameters: tries to evulate the "wanted binsize" and
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
