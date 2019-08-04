import plotly
plotly.tools.set_credentials_file(username='raunit_X', api_key='Lzao5LzzVfmdHVSE6PSF')

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_csv('Flight_1516.csv')
df.head()

lat = df['GPS LATITUDE'].values
lon = df['GPS LONGITUDE'].values
altitude = df['GPS ALTITUDE'].values

trace = go.Scatter3d(
    x=lat, y=lon, z=altitude,
    marker=dict(
        size=3,
        color=z,
        colorscale='Viridis',
        opacity=0.5
    ),
    line=dict(
        color='#1f77b4',
        width=2
    )
)

data = [trace]

layout = dict(
    width=800,
    height=700,
    autosize=False,
    title='GPS 3D PLOT',
    scene=dict(
        xaxis=dict(
            title='Latitude(degree)',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        ),
        yaxis=dict(
            title='Longitude(degree)',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        ),
        zaxis=dict(
            title='Altitude(m)',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        ),
        camera=dict(
            up=dict(
                x=0,
                y=0,
                z=1
            ),
            eye=dict(
                x=-1.7428,
                y=1.0707,
                z=0.7100,
            )
        ),
        aspectratio = dict( x=1, y=1, z=0.7 ),
        aspectmode = 'manual'
    ),
)

fig = dict(data=data, layout=layout)

py.iplot(fig, filename='GPS PLOTS!', height=700)