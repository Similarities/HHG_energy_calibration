import numpy as np
import matplotlib.pyplot as plt
import os


class EnergyToNphoton:
    def __init__(self, file_name, file_path):
        self.file_name = file_name[:-4]
        self.file = file_path + '/' + file_name
        self.energy_J, self.nm_axis = self.load_array()
        self.eV_axis = np.empty([len(self.energy_J)])
        self.convert_to_eV()
        self.nphoton = np.empty([len(self.energy_J)])
        self.nphoton_per_sr = np.empty([len(self.energy_J)])
        self.nphoton_per_sr_at_bw = np.empty([len(self.energy_J)])
        self.joule_to_eV = 6.2415E18

    def main(self):
        self.convert_to_nphoton()
        self.nphoton_per_sr1()
        self.nphoton_per_sr_at_bandwidth()
        self.save_data_single()
        return self.nphoton_per_sr_at_bw

    def load_array(self):
        energy_joule = np.loadtxt(self.file, skiprows=(6), usecols=(1,))
        nm_axis = np.loadtxt(self.file, skiprows=(6), usecols=(0,))
        return energy_joule[::] * 1E-6, nm_axis

    def convert_to_eV(self):
        planck_constant = 4.135667516 * 1E-15
        c = 299792458
        for i, value in enumerate(self.nm_axis):
            self.eV_axis[i] = planck_constant * c / (value * 1E-9)
        return self.eV_axis

    def convert_to_nphoton(self):
        for x in range(0, len(self.energy_J)):
            self.nphoton[x] = self.energy_J[x] * self.joule_to_eV / self.eV_axis[x]

        plt.figure(9)
        plt.plot(self.eV_axis, self.nphoton)
        plt.xlabel("nm")
        plt.ylabel("Nphoton")
        #plt.show()
        return self.nphoton

    def nphoton_per_sr1(self):
        rad = 0.0175 / 2048 * 1550  # evaluated ROI in x
        rad_v = 0.0014  # ROI height collection angle grating
        for i, value in enumerate(self.nphoton):
            self.nphoton_per_sr[i] = value / (rad * rad_v )
        print(rad*rad, "sr")
        return self.nphoton_per_sr

    def nphoton_per_sr_at_bandwidth(self):
        # print(correction, 'correction value for bw')
        # print('bw wanted', bw_wanted)
        # print('bw have', self.energy_range)
        for i in range(0, len(self.nphoton_per_sr)-1):
            bw_wanted = self.eV_axis[i] / 1000
            correction = (self.eV_axis[i]-self.eV_axis[i+1]) / bw_wanted
            self.nphoton_per_sr_at_bw[i] = self.nphoton_per_sr[i] / correction
        self.eV_axis, self.nphoton_per_sr_at_bw = self.eV_axis[:-1], self.nphoton_per_sr_at_bw[:-1]

        plt.figure(12)
        plt.plot(self.eV_axis[:],self.nphoton_per_sr_at_bw[:])
        plt.ylabel("Nphoton/shot * sr  @ 0.1 % bw")
        plt.xlabel("eV")
        return self.nphoton_per_sr_at_bw

    def prepare_header(self):
        result = np.column_stack((self.eV_axis,self.energy_J[:-1], self.nphoton[:-1], self.nphoton_per_sr[:-1], self.nphoton_per_sr_at_bw))
        header_names = (['eV x-axis', 'E [J]', 'Nphoton', 'Nphoton/sr', 'Nphoton/sr @ 0.1bw'])
        parameter_info = (
            [self.file_name[:-4], ' ',  'full spectra ', 'index number ', 'Nphoton via eV'])
        return np.vstack((parameter_info, header_names, result))

    def save_data_single(self):
        result = self.prepare_header()
        print('...saving:', self.file_name)
        np.savetxt(path+self.file_name + '_Nphoton' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


path = 'data/results20190117/'
file_list = []
counter = 0
for file in os.listdir(path):
    try:
        if file.endswith("cal.txt"):
            file_list.append(str(file))
            counter = counter + 1
        else:
            print("only other files found")
    except Exception as e:
        raise e
        print("not files found here")


def batch_files(file_list):
    for counter, value in enumerate(file_list):
        do_it = EnergyToNphoton(value, path)
        do_it.main()


batch_files(file_list)
plt.figure(12)
plt.savefig(path+"20190117_eV_Nphoton_per_sr_0.1pcbw"+".png", bbox_inches="tight", dpi=500)
plt.figure(9)
plt.savefig("data/"+"20190117_eV_Nphoton"+".png", bbox_inches="tight", dpi=500)

plt.show()
