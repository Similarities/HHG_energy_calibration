# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 12:10:06 2019

@author: sweedy
"""

import numpy as np


class Integrate_energy:

    def __init__(self, boundary_Low, boundary_high, spectral_array):
        self.boundary_Low = boundary_Low
        self.boundary_high = boundary_high
        self.spectral_array = spectral_array
        self.integrated_array = float
        self.spectrum_only = np.array

    def resize_to_boundary(self):
        # print(self.boundary_high,' index up, corresponding to x_max')

        index_up = np.amax(np.where(self.spectral_array[:, 0] <= self.boundary_Low))
        # print(index_up, 'long wavelength')

        index_down = np.amin(np.where(self.spectral_array[:, 0] >= self.boundary_high))

        # print(index_down)

        self.spectral_array = self.spectral_array[index_down:index_up]

        return self.spectral_array

    def integrate_resized_array(self):
        # print(self.spectral_array[:,1])

        # self.spectrum_only = np.zeros([len(self.spectral_array),1])

        self.spectrum_only = self.spectral_array[:, 1]

        # print(self.spectrum_only, 'divided')

        self.integrated_array = np.sum(self.spectrum_only[:], axis=0)

        # print(self.integrated_array, 'energy_content')

        return self.integrated_array

