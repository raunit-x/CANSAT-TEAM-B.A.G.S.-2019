# Importing all the libraries and modules
import dash
import base64
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import dash_table
import serial
import csv

MAXLEN = 20
X = deque(maxlen=MAXLEN)
X.append(0)
Temperature = deque(maxlen=MAXLEN)
Pressure = deque(maxlen=MAXLEN)
Voltage = deque(maxlen=MAXLEN)
Altitude = deque(maxlen=MAXLEN)
Pitch = deque(maxlen=MAXLEN)
Roll = deque(maxlen=MAXLEN)

values = {'1': Temperature, '2': Pressure, '3': Voltage,
    '4': Altitude, '5': Pitch, '6': Roll
    }
min_temp = 0
max_temp = 0
max_pressure = 0
min_pressure = 0
min_volt = 0
max_volt = 0
min_altitude = 0
max_altitude = 0
min_pitch = 0
max_pitch = 0
min_roll = 0
max_roll = 0

SERIAL_PORT = '/dev/tty.usbserial-AL017DBD'
BAUD_RATE = 9600
time_out = 0.99

HEADER_ROW = ['TEAM_ID', 'MISSION_TIME', 'PACKET COUNT', 'ALTITUDE', 'PRESSURE',
              'TEMPERATURE', 'VOLTAGE', 'GPS TIME', 'GPS LATITUDE', 'GPS LONGITUDE', 'GPS ALTITUDE',
              'GPS SATELLITES', 'PITCH', 'ROLL', 'BLADE SPIN RATE', 'SOFTWARE STATE', 'BONUS DIRECTION']

file_name = '/Users/raunitsingh/Desktop/cansat.csv'

df = pd.DataFrame(columns=HEADER_ROW)
# df.append(HEADER_ROW)

if __name__ == '__main__':
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=time_out)

myFile = open(file_name, 'wb')  # open in binary
writer = csv.writer(myFile)
writer.writerow(HEADER_ROW)

app = dash.Dash(__name__)
# colors dictionary for all the colors which would be needed in styling
colors = {
    'background': '#111111',
    'text': '#7FD0FF',
    'Grey': '#D3D3D3',
    'GraphSpace': 'rgb(40,40,40)',
    'linecolors': ['FFFF00'],
    'axesColor': '#FFFF00'
}

# encoding all the images in base64
encoded_image_bags = base64.b64encode(open('/Users/raunitsingh/Desktop/CANSAT DIAGRAMS/logo.jpeg', 'rb').read())
encoded_image_flag = base64.b64encode(open('/Users/raunitsingh/Desktop/CANSAT DIAGRAMS/flag.png', 'rb').read())
encoded_image_cansat = base64.b64encode(
                                        open('/Users/raunitsingh/Desktop/CANSAT DIAGRAMS/CanSat Logo - Color.png', 'rb').read())
encoded_image_nsut = base64.b64encode(open('/Users/raunitsingh/Desktop/CANSAT DIAGRAMS/nsut_logo.png', 'rb').read())

# definition of the app
app.layout = html.Div(style={'backgroundColor': colors['background'], 'text-align': 'center'}, children=[
                                                                                                         # The header 1
                                                                                                         html.H1(
                                                                                                                 id='heading',
                                                                                                                 children='TEAM B.A.G.S. NSUT',
                                                                                                                 style={
                                                                                                                 'textAlign': 'center',
                                                                                                                 'color': colors['Grey']
                                                                                                                 }
                                                                                                                 ),
                                                                                                         # The header 2
                                                                                                         html.H2(
                                                                                                                 id='gcs',
                                                                                                                 children='Ground Control Station',
                                                                                                                 style={
                                                                                                                 'textAlign': 'center',
                                                                                                                 'color': '#f0b629'
                                                                                                                 }
                                                                                                                 ),
                                                                                                         # All the images encapsulated under 'images'
                                                                                                         html.Div([
                                                                                                                   html.Img(id='bags', src='data:image/png;base64,{}'.format(encoded_image_bags)),
                                                                                                                   html.Img(id='flag', src='data:image/png;base64,{}'.format(encoded_image_flag)),
                                                                                                                   html.Img(id='cansat', src='data:image/png;base64,{}'.format(encoded_image_cansat)),
                                                                                                                   html.Img(id='nsut', src='data:image/png;base64,{}'.format(encoded_image_nsut))
                                                                                                                   ], className='Images'),
                                                                                                         
                                                                                                         # All the graphs which would be updated using a callback
                                                                                                         html.Div([
                                                                                                                   dcc.Graph(
                                                                                                                             id='temperature-live',
                                                                                                                             animate=True
                                                                                                                             ),
                                                                                                                   dcc.Graph(
                                                                                                                             id='pressure-live',
                                                                                                                             animate=True
                                                                                                                             ),
                                                                                                                   dcc.Graph(
                                                                                                                             id='voltage-live',
                                                                                                                             animate=True
                                                                                                                             ),
                                                                                                                   dcc.Graph(
                                                                                                                             id='altitude-live',
                                                                                                                             animate=True
                                                                                                                             ),
                                                                                                                   dcc.Graph(
                                                                                                                             id='pitch-live',
                                                                                                                             animate=True
                                                                                                                             ),
                                                                                                                   dcc.Graph(
                                                                                                                             id='roll-live',
                                                                                                                             animate=True
                                                                                                                             ),
                                                                                                                   dcc.Interval(
                                                                                                                                id='interval-component',
                                                                                                                                interval=1000,
                                                                                                                                n_intervals=0
                                                                                                                                )
                                                                                                                   
                                                                                                                   ], className='Graphs'),
                                                                                                         
                                                                                                         # Showing the .csv file using dashTable
                                                                                                         dash_table.DataTable(
                                                                                                                              id='datatable-container',
                                                                                                                              columns=[{"name": i, "id": i} for i in df.columns],
                                                                                                                              n_fixed_rows=1,
                                                                                                                              style_table={
                                                                                                                              'align': 'center',
                                                                                                                              'maxWidth': '1800px',
                                                                                                                              'maxHeight': '400px',
                                                                                                                              'overflowY': 'scroll',
                                                                                                                              'overflowX': 'scroll'
                                                                                                                              },
                                                                                                                              style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                                                                                                                              style_cell={
                                                                                                                              'textAlign': 'left',
                                                                                                                              'backgroundColor': 'rgb(40, 40, 40)',
                                                                                                                              'color': 'white',
                                                                                                                              'minWidth': '275px',
                                                                                                                              'width': '275px',
                                                                                                                              'maxWidth': '275px',
                                                                                                                              'whiteSpace': 'normal'
                                                                                                                              },
                                                                                                                              css=[{
                                                                                                                                   'selector': '.dash-cell div.dash-cell-value',
                                                                                                                                   'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                                                                                                                   }]
                                                                                                                              )
                                                                                                         
                                                                                                         ])


# The callback for updating all the graphs
@app.callback([Output('temperature-live', 'figure'),
               Output('pressure-live', 'figure'),
               Output('voltage-live', 'figure'),
               Output('altitude-live', 'figure'),
               Output('pitch-live', 'figure'),
               Output('roll-live', 'figure'),
               Output('datatable-container', 'data')],
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    global values, min_temp, max_temp, min_altitude, min_pitch, max_altitude, max_pitch, min_pressure,\
        max_pressure, min_volt, max_volt, min_roll, max_roll, df
    X.append(X[-1] + 1)
    # Here the sensor updating code will be there
    message = ser.readline()
    message = message[:-2]  # to remove '\r' and '\n'
    data = list(message.split(','))
    indices_values = ['1', '2', '3', '4', '5', '6']
    indices_data = [5, 4, 6, 3, 12, 13]
    if len(data) > 16:
        # data = data[:-2]
        print(data)
        for index in indices_data:
            for j in indices_values:
                values[j].append(float(data[index]))
        writer.writerow(data)
    
    # Use of so many variables for optimisation over using min(deque) and max(deque)
    if len(values['1']) == 1:
        min_temp = Temperature[0]
        max_temp = Temperature[0]
        min_pressure = Pressure[0]
        max_pressure = Pressure[0]
        min_volt = Voltage[0]
        max_volt = Voltage[0]
        min_altitude = Altitude[0]
        max_altitude = Altitude[0]
        min_pitch = Pitch[0]
        max_pitch = Pitch[0]
        min_roll = Roll[0]
        max_roll = Roll[0]

    min_temp = min(float(data[5]), min_temp)
    max_temp = max(float(data[5]), max_temp)
    min_pressure = min(float(data[4]), min_pressure)
    max_pressure = max(float(data[4]), max_pressure)
    min_volt = min(float(data[6]), min_volt)
    max_volt = max(float(data[6]), max_volt)
    min_altitude = min(float(data[3]), min_altitude)
    max_altitude = max(float(data[3]), max_altitude)
    min_pitch = min(float(data[12]), min_pitch)
    max_pitch = max(float(data[12]), max_pitch)
    min_roll = min(float(data[13]), min_roll)
    max_roll = max(float(data[13]), max_roll)

data_temperature = go.Scatter(
                              x=list(X),
                              y=list(values['1']),
                              name='Scatter',
                              mode='lines+markers'
                              )
    data_pressure = go.Scatter(
                               x=list(X),
                               y=list(values['2']),
                               name='Scatter',
                               mode='lines+markers'
                               )
                               data_voltage = go.Scatter(
                                                         x=list(X),
                                                         y=list(values['3']),
                                                         name='Scatter',
                                                         mode='lines+markers'
                                                         )
                               data_altitude = go.Scatter(
                                                          x=list(X),
                                                          y=list(values['4']),
                                                          name='Scatter',
                                                          mode='lines+markers'
                                                          )
                               data_pitch = go.Scatter(
                                                       x=list(X),
                                                       y=list(values['5']),
                                                       name='Scatter',
                                                       mode='lines+markers'
                                                       )
                               data_roll = go.Scatter(
                                                      x=list(X),
                                                      y=list(values['6']),
                                                      name='Scatter',
                                                      mode='lines+markers'
                                                      )
                               min_x = min(X)
                               max_x = max(X)
                               layout_temperature = {
                                   'title': 'TEMPERATURE(in Celcius)',
                                       'plot_bgcolor': colors['GraphSpace'],
                                       'paper_bgcolor': colors['background'],
                                       'font': {'color': '#669999'},
                                           'colorway': ['#FFFF00'],
                                           'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
                                           'yaxis': dict(linecolor='#669999', linewidth=2, title='Temperature',
                                                         range=[min_temp - 0.03, max_temp + 0.03])
                                       }
layout_pressure = {
    'title': 'PRESSURE(in Pascals)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Pressure',
                      range=[min_pressure - 0.03, max_pressure + 0.03])
    }
    layout_voltage = {
        'title': 'Voltage(in Volts)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Voltage',
                      range=[min_volt - 0.03, max_volt + 0.03])
}
    layout_altitude = {
        'title': 'ALTITUDE(in meters)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Altitude',
                      range=[min_altitude - 0.03, max_altitude + 0.03])
}
    layout_pitch = {
        'title': 'PITCH(in Radians)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Pitch',
                      range=[min_pitch - 0.03, max_pitch + 0.03])
}
    layout_roll = {
        'title': 'ROLL(in Radians)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Roll',
                      range=[min_roll - 0.03, max_roll + 0.03])
}
    
    temp = {'data': [data_temperature], 'layout': layout_temperature}
    pres = {'data': [data_pressure], 'layout': layout_pressure}
    volt = {'data': [data_voltage], 'layout': layout_voltage}
    alti = {'data': [data_altitude], 'layout': layout_altitude}
    pitc = {'data': [data_pitch], 'layout': layout_pitch}
    roll = {'data': [data_roll], 'layout': layout_roll}
    
    # Implementing the DataFrame as a deque
    if df.shape[0] > 20:  # if the number of rows is > 20, then we pop the first row
        df = df.iloc[1:]   # Limiting the size of the DataFrame to 20 rows
    df = df.append(pd.Series(data, index=df.columns), ignore_index=True)

return temp, pres, volt, alti, pitc, roll, df.to_dict('rows')


if __name__ == '__main__':
    app.run_server(port=8050)

