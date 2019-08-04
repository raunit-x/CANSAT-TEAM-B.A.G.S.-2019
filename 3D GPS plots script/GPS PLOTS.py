#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[2]:


import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd


# In[3]:


import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
plt.figure(figsize=(10, 5))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='l')
m.drawcoastlines()
m.bluemarble()
df = pd.read_csv('FLIGHT_1516.csv')
lat = df['GPS LATITUDE'].values
lon = df['GPS LONGITUDE'].values
altitude = df['GPS ALTITUDE'].values

x, y = m(lon, lat)


# #create colorbar 
# plt.colorbar(label=r'Altitude')
# plt.clim(0, 1000)


m.plot(x, y, 'k-', markersize=8, alpha=0.8, linewidth=1)
m.plot(x, y, 'co', markersize=8, alpha=0.1)
plt.title('World Map!')
plt.show()


# In[5]:


from matplotlib.collections import PolyCollection
fig = plt.figure(figsize=(12, 8))
ax = fig.gca(projection='3d')
# Define lower left, uperright lontitude and lattitude respectively
extent = [-180, 180, -90, 90]
# Create a basemap instance that draws the Earth layer

bm = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[2],
             urcrnrlon=extent[1], urcrnrlat=extent[3],
             projection='cyl', resolution='l', fix_aspect=False, ax=ax)

# To fill the color in the continents
polys = []
for polygon in bm.landpolygons:
    polys.append(polygon.get_coords())

lc = PolyCollection(polys, edgecolor='none',
                    facecolor='#DDDDDD', closed=False)
lcs = ax.add_collection3d(lc, zs=0)  # set zero zs

# Create underlying blue color rectangle
# It's `zs` value is -0.003, so it is plotted below land polygons
bpgon = np.array([[-180., -90],
       [-180, 90],
       [180, 90],
       [180, -90]])
polys2 = []
polys2.append(bpgon)
lc2 = PolyCollection(polys2, edgecolor='none', linewidth=0.1,                     facecolor='#445599', alpha=1.0, closed=False)
lcs2 = ax.add_collection3d(lc2, zs=-0.003)  # set negative zs value

# Add Basemap to the figure
ax.add_collection3d(bm.drawcoastlines(linewidth=0.25))
ax.add_collection3d(bm.drawcountries(linewidth=0.35))
ax.view_init(azim=230, elev=50)
ax.set_xlabel('Longitude (°E)', labelpad=20)
ax.set_ylabel('Latitude (°N)', labelpad=20)
ax.set_zlabel('Altitude (m)', labelpad=20)
# Add meridian and parallel gridlines
lon_step = 30
lat_step = 30
meridians = np.arange(extent[0], extent[1] + lon_step, lon_step)
parallels = np.arange(extent[2], extent[3] + lat_step, lat_step)
ax.set_yticks(parallels)
ax.set_yticklabels(parallels)
ax.set_xticks(meridians)
ax.set_xticklabels(meridians)
ax.set_zlim(0, 1000)
lons = df['GPS LONGITUDE'].values
lats = df['GPS LATITUDE'].values
heights = heights = df['GPS ALTITUDE'].values

x, y = bm(lons, lats)


ax.bar3d(x, y, np.zeros(len(x)), 1, 1, heights, color= 'r')
plt.show()


# In[6]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PolyCollection
import numpy as np

fig = plt.figure(figsize=(6, 12))
map = Basemap(llcrnrlon=-20,llcrnrlat=0,urcrnrlon=15,urcrnrlat=50)

extent = [-20, 0, 15, 50]
ax = Axes3D(fig)

ax.set_axis_off()
ax.azim = 270
ax.dist = 7

polys = []
for polygon in map.landpolygons:
    polys.append(polygon.get_coords())


lc = PolyCollection(polys, edgecolor='black',
                    facecolor='#DDDDDD', closed=False)
bpgon = np.array([[-180., -90],
       [-180, 90],
       [180, 90],
       [180, -90]])
polys2 = []
polys2.append(bpgon)
lc2 = PolyCollection(polys2, edgecolor='none', linewidth=0.1,                     facecolor='#445599', alpha=1.0, closed=False)
lcs2 = ax.add_collection3d(lc2, zs=-0.003)  # set negative zs value

ax.add_collection3d(lc)
ax.add_collection3d(map.drawcoastlines(linewidth=0.25))
ax.add_collection3d(map.drawcountries(linewidth=0.35))
import pandas as pd
df = pd.read_csv('flight_1516.csv')
lons = np.array([-13.7, -10.8, -13.2, -96.8, -7.99, 7.5, -17.3, -3.7]) # lons = df['GPS LONGITUDE'].values
lats = np.array([9.6, 6.3, 8.5, 32.7, 12.5, 8.9, 14.7, 40.39]) # lats = df['GPS LATIUTUDE'].values
heights = np.array([1192, 2964, 1250, 1, 5, 8, 0, 0]) # heights = df['GPS ALTITUDE'].values

x, y = map(lons, lats)

ax.bar3d(x, y, np.zeros(len(x)), 2, 2, heights, color= 'r', alpha=0.8)

plt.show()


# In[ ]:




