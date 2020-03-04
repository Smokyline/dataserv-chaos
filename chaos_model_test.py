from core import SWARM
from datetime import datetime


swarm_type = ['SWA', 'SWB', 'SWC']
from_date = datetime(2015, 3, 15, 00, 00, 00)
to_date = datetime(2015, 3, 19, 23, 59, 59)

swarm = SWARM(char='A', dt_from=from_date, dt_to=to_date, delta=240)

swarm.plot_map()

"""
import matplotlib.pyplot as plt
fig= plt.figure(figsize=(12,7))
plt.plot(sw_coords[:, 1], theta, label='theta', lw=0.8)
plt.plot(sw_coords[:, 1], phi, label='phi', lw=0.8)
plt.xlabel('lat')
plt.ylabel('v_swarm - v_chaos')
plt.grid(True)
plt.legend(loc=2)
plt.savefig(('plot.png'), dpi=500)
plt.close()

"""


