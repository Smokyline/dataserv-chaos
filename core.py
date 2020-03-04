import time

from chaos7_model.chaos_model import CHAOS7
from data_tools import *
from chaos.settings import STATIC_ROOT

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs


class SWARM:
    def __init__(self, char, dt_from, dt_to, delta):
        self.led = int(round(time.time() * 1000))
        self.sw_char, self.dt_from, self.dt_to, self.delta = char, dt_from, dt_to, delta
        self.swarm_set = self.get_data_from_sql()

    def get_data_from_sql(self):
        """getting data from intermagnet SQL table"""
        from_date = ut_dt_to_unix(self.dt_from, out_type='str')
        to_date = ut_dt_to_unix(self.dt_to, out_type='str')

        respond = get_data_from_sqldb('SW' + self.sw_char.upper(), from_date, to_date)
        respond = data_reduction(np.array(respond), self.delta)

        swarm_date = []
        swarm_time = []
        swarm_position = []

        swarm_dt_unix, Y, X, R, N, E, C, F = respond.T
        for i, dt in enumerate(swarm_dt_unix):
            sw_date, sw_time = str(unix_to_ut_dt(int(dt))).split(' ')
            swarm_date.append(sw_date)
            swarm_time.append(sw_time)
            swarm_position.append([X[i], Y[i], (R[i] / 1000)])  # km => r/1000
        swarm_resp = np.empty((len(swarm_date), 0))
        for v in [N, E, C, F]:
            swarm_resp = np.append(swarm_resp, np.array([v]).T, axis=1)

        print(
            'render will use data from swarm-%s dt from %s to %s' % (self.sw_char, swarm_date[0] + ' ' + swarm_time[0],
                                                                     swarm_date[-1] + ' ' + swarm_time[-1]))
        return [self.sw_char, np.array(swarm_position), swarm_date, swarm_time, swarm_resp]

    def chaos_model(self):
        chaos = CHAOS7(self.swarm_set)
        return chaos.model()

    def plot_map(self):
        X, Y = self.swarm_set[1][:, 0], self.swarm_set[1][:, 1]
        theta, phi = self.chaos_model()

        idx_merc = np.logical_and(Y <= 70, Y >= -70)
        idx_polar_n = np.where(Y > 55)[0]
        idx_polar_s = np.where(Y < -55)[0]

        fig = plt.figure(figsize=(17, 9))  # x, y
        gs = gridspec.GridSpec(6, 7)  # y, x
        ax1 = plt.subplot(gs[:3, 5:], projection=ccrs.Orthographic(central_latitude=90.,
                                                                   central_longitude=0))
        ax2 = plt.subplot(gs[:, :5], projection=ccrs.Mercator(
            min_latitude=-65.0, max_latitude=75.0))
        ax3 = plt.subplot(gs[3:, 5:], projection=ccrs.Orthographic(central_latitude=-90.,
                                                                   central_longitude=0))
        for ax in [ax1, ax2, ax3]:
            ax.coastlines(resolution='110m', color='k', zorder=7)
            ax.add_feature(cfeature.LAND, facecolor='0.75', zorder=0)
            ax.gridlines()
            ax.plot(X, Y, 'k--', zorder=1,
                    lw=0.75, alpha=0.35, transform=ccrs.Geodetic())

        # polar north
        q1 = ax1.quiver(X[idx_polar_n], Y[idx_polar_n], theta[idx_polar_n], phi[idx_polar_n],
                        transform=ccrs.PlateCarree(), headwidth=2, units='xy', color='blue')
        qk1 = ax1.quiverkey(q1, 0.9, 0.95, 3000, r'$3000 nT$', labelpos='N', coordinates='axes',
                            fontproperties={'weight': 'bold'})
        # mercator
        q2 = ax2.quiver(X[idx_merc], Y[idx_merc], theta[idx_merc], phi[idx_merc],
                        transform=ccrs.PlateCarree(), scale=q1.scale, scale_units='inches', color='blue')
        qk2 = ax2.quiverkey(q2, 0.9, 1.05, 3000, r'$3000 nT$', labelpos='N', coordinates='axes',
                            fontproperties={'weight': 'bold'})
        ax2.set_title('%s - %s' % (str(self.dt_from), str(self.dt_to)))
        # polar south
        q3 = ax3.quiver(X[idx_polar_s], Y[idx_polar_s], theta[idx_polar_s], phi[idx_polar_s],
                        transform=ccrs.PlateCarree(), headwidth=2, units='xy', color='blue')
        qk3 = ax3.quiverkey(q3, 0.9, 0.95, 3000, r'$3000 nT$', labelpos='N', coordinates='axes',
                            fontproperties={'weight': 'bold'})

        plt.savefig((STATIC_ROOT + 'images/' + str(self.led) + '.png'), dpi=600)
        plt.close()
        return self.led
