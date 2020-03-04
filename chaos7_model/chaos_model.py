import numpy as np
from chaosmagpy import load_CHAOS_matfile
from chaosmagpy.model_utils import synth_values
from chaos.settings import FILEPATH_CHAOS
from astropy.time import Time


class CHAOS7():
    def __init__(self, swarm_set):
        self.swarm_set = swarm_set
        self.chaos7_mat_model = load_CHAOS_matfile(FILEPATH_CHAOS)

    def dt_unix_to_mjd(self, times):
        t = Time(times, format='iso', scale='utc')
        t.format = 'mjd'
        time_mjd_ad = np.array(t.value).astype(float) - 51544
        return time_mjd_ad

    def model(self):
        swarm_char, swarm_pos, swarm_date, swarm_time, swarm_response = self.swarm_set
        sw_n, sw_e, sw_c, sw_f = swarm_response[:, 0], swarm_response[:,
                                                                              1], swarm_response[:, 2], swarm_response[:, 3]
        # B_r = -Z; B_phi = Y; B_theta = -X
        theta = 90. - swarm_pos[:, 1]  # colat deg
        phi = swarm_pos[:, 0]  # deg
        radius = swarm_pos[:, 2]  # radius in km

        time = self.dt_unix_to_mjd(
            [str(a) + " " + str(b) for a, b in zip(swarm_date, swarm_time)])  # time in modified Julian date 2000

        # computing core field
        coeffs = self.chaos7_mat_model.synth_coeffs_tdep(time)  # SV max. degree 16
        B_radius, B_theta, B_phi = synth_values(coeffs, radius, theta, phi)
        # B_radius, B_theta, B_phi = self.chaos7_mat_model(time, radius, theta, phi)

        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(12, 7))
        plt.plot(swarm_pos[:, 1], B_theta, label='chaos theta', lw=0.8, color='r')
        plt.plot(swarm_pos[:, 1], B_phi, label='chaos phi', lw=0.8, color='g')

        plt.plot(swarm_pos[:, 1], (sw_n * -1), label='swarm theta', lw=0.8, color='b')
        plt.plot(swarm_pos[:, 1], sw_e, label='swarm phi', lw=0.8, color='orange')
        plt.xlabel('lat')
        plt.ylabel('nT')
        plt.grid(True)
        plt.legend(loc=2)
        plt.savefig(('plotall.png'), dpi=500)
        plt.close()

        return (sw_n * -1) - B_theta, sw_e - B_phi
