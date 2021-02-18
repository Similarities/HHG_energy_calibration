# HHG energy calibration
- batch calibration for images in a folder
- 2D background substraction (mean value of either x or y in image)
- spectral evaluation for y-axis of image according grating function
- integration of different calibration data (CCD, filter, grating)
- linear interpolation of calibration data
- 1/i dependency for spectral energy range to be integrated
- integration over spatial ROI
- resampling spectral bin ranges from non-linear to linear
- batch process for images in one folder, over certain energy ranges in one image
- approximation of Nphoton/sr @ 0.01 band width for picked energy-ranges over batch list

#2-f Binning 'resample'
This project is an application of the so called 2-frequency binning method.
2f binning is commmonly needed
when e.g. integrated pictures (spectra) have to be calibrated. Usually the spectra has 
a non-linear x-scaling, which is a consequence of the grating function. The calibration 
data set (e.g. measuring the sensitivity of a camera at different photon energies) usually
contains of less data points with a variable distance (binning) in the x-axis. 
In order to do the calibration via broadcasting of arrays, the spectral binning has to be
same. Hence, calibration data is linearly interpolated, the measured spectra is linearized - 
in order to achieve the same bin-size width.

what it can do:

- opens and further calculates all .tif files from given filepath (16 bit, 2048x2048) 
- integrates picture over one dimension (space)
- takes at the right side of the picture a background, substracts mean value
- rescales the x- axis according a function (spectrometer function)
- resizes the x-binning to equi-distant binning (re- sampling)
- needs now 3 calibration files (2 colummn. txt) (e.g. camera, filter, grating)
- can transfer the calibration x-axis from eV to nm
- linearly interpolates the calibration files to the same binning as chosen for the picture (upsampling)
- calculates maximum range (spectrally) from the picture and resizes the calibration range accordingly
- multiplies the calibration to the integrated picture (spectrum)
- delivers the option to save separatly each file
- plots....


what is still not catched:
- stops working if the input binning of the calibration files is smaller than the wanted one
- it has no file dialog
- a more accurate handling of overhang bins (at the moment just delets and by this shifts one or two)
- code needs some cleaning


The so converted picture became an array of DIM 2048x2 which due to the x-axis scaling
it might now have non-equidistant bins.
Our converted array is now checked for resizing the binnings to a equidistant ones.
Prerequisite is, in order to avoid subsampling and by this alias or an increase of
resolution that is not there: the maximum bin-size*1.5* in our array limits the resulting
binsize. The programm checks for this, and if the chosen binsize (called self.result_binsize)
is to small, it will be set automatically to the maximum bin_size of our array (rounded on one digit accuracy).
After this the x-axis and accordingly the y-axis are redistributed to the new binning range.
(method description can be found in "2f-binning-III_nonlinear..."- repository. 



Python 3.7
