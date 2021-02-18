import numpy as np
import matplotlib.pyplot as plt
import os


class EnergyToNphoton:
    def __init__(self, file_name, file_path):
        self.file_name = file_name[:-4]
        self.file = file_path + '/' + file_name
        self.energy_J = self.load_array()
        self.nphoton = np.empty([len(self.energy_J)])
        self.nphoton_per_sr = np.empty([len(self.energy_J)])
        self.nphoton_per_sr_at_bw = np.empty([len(self.energy_J)])
        self.joule_to_eV = 6.2415E18
        self.energy_at_eV = 38.75  # 800/N25
        self.energy_range = 39.5194 - 37.9702  # N25+0.5N - N25-0.25N  in eV

    def main(self):
        self.convert_to_nphoton()
        self.nphoton_per_sr()
        self.nphoton_per_sr_at_bw()
        self.save_data_single()
        return self.nphoton_per_sr_at_bw

    def load_array(self):
        energy_joule = np.loadtxt(self.file, skiprows=(0), usecols=(0,))
        return energy_joule[::] * 1E-6

    def convert_to_nphoton(self):
        for i, value in enumerate(self.energy_J):
            self.nphoton[i] = value * self.joule_to_eV / self.energy_at_eV
        return self.nphoton

    def nphoton_per_sr(self):
        mrad = 17.5 / 2048 * 1550  # evaluated ROI in x
        mrad_v = 0.0014  # ROI height collection angle grating
        for counter, value in enumerate(self.nphoton):
            self.nphoton_per_sr[counter] = value / (mrad * mrad_v * 1E-6)
        return self.nphoton_per_sr

    def nphoton_per_sr_at_bw(self):
        bw_wanted = self.energy_at_eV / 1000
        correction = self.energy_range / bw_wanted
        # print(correction, 'correction value for bw')
        # print('bw wanted', bw_wanted)
        # print('bw have', self.energy_range)
        for i, value in enumerate(self.nphoton_per_sr):
            self.nphoton_per_sr_at_bw[i] = value / correction

        return self.nphoton_per_sr_at_bw

    def prepare_header(self):
        result = np.column_stack((self.energy_J, self.nphoton, self.nphoton_per_sr, self.nphoton_per_sr_at_bw))
        header_names = (['E [J]', 'Nphoton', 'Nphoton/sr', 'Nphoton/sr @ 0.1bw'])
        parameter_info = (
            [self.file_name[:-4], 'N25 +/- 0.5N ', 'index number ', 'Nphoton via eV'])
        return np.vstack((parameter_info, header_names, result))

    def save_data_single(self):

        print('...saving:', self.file_name)
        np.savetxt(self.file_name + '_Nphoton_only' + ".txt", self.nphoton_per_sr_at_bw, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


path = 'results'
file_list = []
counter = 0
for file in os.listdir(path):
    try:
        if file.endswith("0.5N25.txt"):
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
