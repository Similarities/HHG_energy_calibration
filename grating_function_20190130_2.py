#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:54:54 2019

@author: similarities
"""

import matplotlib.pyplot as plt
import numpy as np


class GratingCalculationOnPicture:

    def __init__(self, filename, xlabel, ylabel):

        self.filename = filename
        self.filedescription = self.filename
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.picture = np.empty([])
        self.integrated = np.empty([])
        self.x_backsubstracted = np.empty([2048, 2048])
        self.x_axis_in_nm = np.empty([2048, 1])
        self.result_array = np.zeros([2048, 2])

    def open_file(self):

        self.picture = plt.imread(self.filename)
        return self.picture

    def integrate_and_background(self):

        self.integrated = np.sum(self.x_backsubstracted[::, 50:1600], axis=1)
        self.second_background()
        return self.integrated

    def second_background(self):
        print(len(self.integrated))
        for counter, value in enumerate(self.integrated):
            self.integrated[counter] = value  # +150000
        return self.integrated

    def background(self):
        back_mean = np.mean(self.picture[:, 1700:1800], axis=1)
        for counter, value in enumerate(self.x_backsubstracted[::, 0]):
            self.x_backsubstracted[::, counter] = self.picture[::, counter] - (back_mean[counter])
        self.integrate_and_background()
        print(np.amin(self.integrated[50:-50]), 'minimum .... after sum')
        return self.integrated

    def grating_function(self):
        N = len(self.integrated)
        i = 0
        while i <= N - 1:
            self.x_axis_in_nm[i] = 1.27877896e-06 * i ** 2 - 1.37081526e-02 * i + 3.46785380e+01
            i = i + 1
        self.array_of_spectrum()
        return self.result_array


    def array_of_spectrum(self):
        for x in range(0, len(self.x_axis_in_nm)):
            self.result_array[x, 0] = self.x_axis_in_nm[x]
            self.result_array[x, 1] = self.integrated[x]
