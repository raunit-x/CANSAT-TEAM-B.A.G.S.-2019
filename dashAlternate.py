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


MAX_LENGTH = 20
X = deque(maxlen=MAX_LENGTH)
X.append(0)
Temperature = deque(maxlen=MAX_LENGTH)
Pressure = deque(maxlen=MAX_LENGTH)
Voltage = deque(maxlen=MAX_LENGTH)
Altitude = deque(maxlen=MAX_LENGTH)
Pitch = deque(maxlen=MAX_LENGTH)
Roll = deque(maxlen=MAX_LENGTH)
GpsSats = deque(maxlen=MAX_LENGTH)
BladeSpinRate = deque(maxlen=MAX_LENGTH)
BonusDirection = deque(maxlen=MAX_LENGTH)

# This dictionary maps a number to the deque of a field along with the min and max of the graphing window
# of the field. Index 1 is for min values and Index 2 for max values and index 3 is for the
# index of the field in the .csv header file
values = {'1': [Temperature, 0, 0, 5], '2': [Pressure, 0, 0, 4],
          '3': [Voltage, 0, 0, 6], '4': [Altitude, 0, 0, 3], '5': [Pitch, 0, 0, 12],
          '6': [Roll, 0, 0, 13], '7': [GpsSats, 0, 0, 11],
          '8': [BladeSpinRate, 0, 0, 14], '9': [BonusDirection, 0, 0, 16]
          }
SERIAL_PORT = '/dev/cu.usbserial-AL017DBE'
#  '/dev/tty.usbserial-AL017DBD'
BAUD_RATE = 9600
time_out = 0.99

HEADER_ROW = ['TEAM_ID', 'MISSION_TIME', 'PACKET COUNT', 'ALTITUDE', 'PRESSURE',
              'TEMPERATURE', 'VOLTAGE', 'GPS TIME', 'GPS LATITUDE', 'GPS LONGITUDE', 'GPS ALTITUDE',
              'GPS SATELLITES', 'PITCH', 'ROLL', 'BLADE SPIN RATE', 'SOFTWARE STATE', 'BONUS DIRECTION']


file_name = '/Users/raunitsingh/Desktop/cansat.csv'

df = pd.DataFrame(columns=HEADER_ROW)
# df.append(HEADER_ROW)

# if __name__ == '__main__':
#     ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=time_out)

myFile = open(file_name, 'wb')  # open in write in bytes
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
encoded_image_bags = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/logo.jpeg', 'rb').read())
encoded_image_flag = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/flag.png', 'rb').read())
encoded_image_cansat = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/CanSat Logo - Color.png', 'rb').read())
encoded_image_nsut = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/nsut_logo.png', 'rb').read())

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
        children='GROUND CONTROL STATION',
        style={
            'textAlign': 'center',
            'color': '#9b9999'  # dark grey
        }
    ),
    # All the images encapsulated under 'images'
    html.Div([
        html.Img(id='bags', src='data:image/png;base64,{}'.format(encoded_image_bags)),
        html.Img(id='flag', src='data:image/png;base64,{}'.format(encoded_image_flag)),
        html.Img(id='cansat', src='data:image/png;base64,{}'.format(encoded_image_cansat)),
        html.Img(id='nsut', src='data:image/png;base64,{}'.format(encoded_image_nsut))
    ], className='Images'),

    # Add a reset button
    html.Div([html.Button('RESET', id='button')]),
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
        dcc.Graph(
            id='gps-live',
            animate=True
        ),
        dcc.Graph(
            id='blade-live',
            animate=True
        ),
        dcc.Graph(
            id='bonus-live',
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


indices_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
indices_data = []
for index in range(len(indices_values)):
    indices_data.append(values[indices_values[index]][3])

#
# @app.callback([Output('button', 'n_clicks')],
#               [Input('button', 'n_clicks')])
# def reset_values(n_clicks):
#     global values, indices_values, df
#     for index in indices_values:
#         values[index][0].clear()
#     df = df.iloc[0:0]
#     return None


count = 0
dfCSV = pd.read_csv('/Users/raunitsingh/Desktop/cansat Stuff/Flight_1516_practice.csv')
numberOfClicks = 0

# The callback for updating all the graphs
@app.callback([Output('temperature-live', 'figure'),
               Output('pressure-live', 'figure'),
               Output('voltage-live', 'figure'),
               Output('altitude-live', 'figure'),
               Output('pitch-live', 'figure'),
               Output('roll-live', 'figure'),
               Output('gps-live', 'figure'),
               Output('blade-live', 'figure'),
               Output('bonus-live', 'figure'),
               Output('datatable-container', 'data')],
              [Input('interval-component', 'n_intervals'),
               Input('button', 'n_clicks')])
def update_graph(n, n_clicks):
    global values, df, X, indices_data, indices_values, count, dfCSV, numberOfClicks

    # Here the sensor updating code will be there
    # message = ser.readline()
    # print(message)
    # message = message[:-2]  # to remove '\r' and '\n'
    # Converting the message to a list
    # print(n_clicks)

    data = dfCSV.iloc[count % 32].values
    count += 1

    # Updating the deque by adding the corresponding values to the corresponding arrays
    #  and data[6] <= '5' and data[5] >= '0' and data[4] >= '75000' \
    #       and data[4] <= '110000' and data[3] >= '0' and data[3] <= '800'
    if data[0] == 1516:
        print(data)
        X.append(X[-1] + 1)
        for i, j in zip(indices_values, indices_data):
            values[i][0].append(float(data[j]))
        writer.writerow(data)
        # Use of so many variables for optimisation over using min(deque) and max(deque)
        if len(values['1']) == 1:
            for i, j in zip(indices_values, indices_data):
                values[i][1] = values[i][2] = data[j]
        # Calculating the min and max values for the graph windows
        for i, j in zip(indices_values, indices_data):
            values[i][1] = min(values[i][1], data[j])
            values[i][2] = max(values[i][2], data[j])

    data_temperature = go.Scatter(
        x=list(X),
        y=list(values['1'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_pressure = go.Scatter(
        x=list(X),
        y=list(values['2'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_voltage = go.Scatter(
        x=list(X),
        y=list(values['3'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_altitude = go.Scatter(
        x=list(X),
        y=list(values['4'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_pitch = go.Scatter(
        x=list(X),
        y=list(values['5'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_roll = go.Scatter(
        x=list(X),
        y=list(values['6'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_gps_sats = go.Scatter(
        x=list(X),
        y=list(values['7'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_blade_spin_rate = go.Scatter(
        x=list(X),
        y=list(values['8'][0]),
        name='Scatter',
        mode='lines+markers'
    )
    data_bonus_direction = go.Scatter(
        x=list(X),
        y=list(values['9'][0]),
        name='Scatter',
        mode='lines+markers'
    )

    min_x = X[0]
    max_x = X[-1]
    layout_temperature = {
        'title': 'TEMPERATURE(in Celcius)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Temperature')
    }
    layout_pressure = {
        'title': 'PRESSURE(in Pascals)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Pressure')
    }
    layout_voltage = {
        'title': 'Voltage(in Volts)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Voltage')
    }
    layout_altitude = {
        'title': 'ALTITUDE(in meters)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Altitude')
    }
    layout_pitch = {
        'title': 'PITCH(in Radians)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Pitch')
    }
    layout_roll = {
        'title': 'ROLL(in Radians)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Roll')
    }
    layout_gps_sats = {
        'title': 'GPS Satellites(integer value)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='GPS Satellites')
    }
    layout_blade_spin_rate = {
        'title': 'BLADE SPIN RATE(in radians/sec)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Blade Spin Rate')
    }
    layout_bonus_direction = {
        'title': 'BONUS DIRECTION(in Radians)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=[min_x, max_x]),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Bonus Direction')
    }

    temp = {'data': [data_temperature], 'layout': layout_temperature}
    pres = {'data': [data_pressure], 'layout': layout_pressure}
    volt = {'data': [data_voltage], 'layout': layout_voltage}
    alti = {'data': [data_altitude], 'layout': layout_altitude}
    pitc = {'data': [data_pitch], 'layout': layout_pitch}
    roll = {'data': [data_roll], 'layout': layout_roll}
    gps = {'data': [data_gps_sats], 'layout': layout_gps_sats}
    blade = {'data': [data_blade_spin_rate], 'layout': layout_blade_spin_rate}
    bonus = {'data': [data_bonus_direction], 'layout': layout_bonus_direction}
    # Implementing the DataFrame as a deque
    if df.shape[0] > 20:  # if the number of rows is > 20, then we pop the first row
        df = df.iloc[1:]  # Limiting the size of the DataFrame to 20 rows
    df = df.append(pd.Series(data, index=df.columns), ignore_index=True)

    if n_clicks is not None:
        if n_clicks > numberOfClicks:
            for j in indices_values:
                values[j][0].clear()
            X.clear()
            X.append(0)
            df = df.iloc[0:0]
            myFile.truncate(0)
            writer.writerow(HEADER_ROW)
        numberOfClicks = n_clicks

    return temp, pres, volt, alti, pitc, roll, gps, blade, bonus, df.to_dict('rows')


if __name__ == '__main__':
    app.run_server(port=8050)
