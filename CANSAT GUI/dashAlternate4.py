# Import all the packages
import dash
import base64
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_table
import serial
import csv
import time
import os


# All the lists for plotting
X = list([])
X.append(0)
Temperature = list([])
Pressure = list([])
Voltage = list([])
Altitude = list([])
Pitch = list([])
Roll = list([])
GpsSats = list([])
BladeSpinRate = list([])
BonusDirection = list([])

# This dictionary maps a number to the deque of a field along with the min and max of the graphing window
# of the field. Index 1 is for min values and Index 2 for max values and index 3 is for the
# index of the field in the .csv header file
values = {
    '1': [Temperature, 0, 0, 5], '2': [Pressure, 0, 0, 4],
    '3': [Voltage, 0, 0, 6], '4': [Altitude, 0, 0, 3], '5': [Pitch, 0, 0, 12],
    '6': [Roll, 0, 0, 13], '7': [GpsSats, 0, 0, 11],
    '8': [BladeSpinRate, 0, 0, 14], '9': [BonusDirection, 0, 0, 16]
}

# This dictionary is for all the particulars of the serial port connection
my_settings = {'PORT': '/dev/cu.usbserial-AL017DBE', 'BAUD_RATE': 9600, 'TIME_OUT': 0.99}

# The header row of the .csv file
HEADER_ROW = ['TEAM_ID', 'MISSION_TIME', 'PACKET COUNT', 'ALTITUDE', 'PRESSURE',
              'TEMPERATURE', 'VOLTAGE', 'GPS TIME', 'GPS LATITUDE', 'GPS LONGITUDE', 'GPS ALTITUDE',
              'GPS SATELLITES', 'PITCH', 'ROLL', 'BLADE SPIN RATE', 'SOFTWARE STATE', 'BONUS DIRECTION']


# The local path to the new .csv file
file_path = '/Users/raunitsingh/Desktop/Flight_1516.csv'

# A dynamic data frame to see the packets received in real time
df = pd.DataFrame(columns=HEADER_ROW)


# The class to access the pySerial port safely
class Controller:
    # The constructor
    def __init__(self, settings):
        self.ser = None
        self.settings = settings

    # This function connects if there is no established connection and vice versa
    def connect_disconnect(self):
        try:
            if self.ser is None:  # Connecting for the first time
                self.ser = serial.Serial(port=self.settings['PORT'],
                                         baudrate=self.settings['BAUD_RATE'], timeout=self.settings['TIME_OUT'])
                print('Here')
                print "Successfully connected to port %r." % self.ser.port
                return True
            else:
                if self.ser.isOpen():  # If the port is open, close it
                    self.ser.close()
                    print "Disconnected."
                    return False
                else:
                    # If the port is closed, reconnect it
                    self.ser = serial.Serial(port=self.settings['PORT'],
                                             baudrate=self.settings['BAUD_RATE'], timeout=self.settings['TIME_OUT'])
                    print "Connected."
                    return True
        except serial.SerialException:
            return False


# Make an object of the serial port class to safely access the port
my_connector = Controller(my_settings)

# Establish the connection for the first time
if __name__ == '__main__':
    my_connector.connect_disconnect()

myFile = open(file_path, 'a')  # open in write in bytes in append mode
writer = csv.writer(myFile)

# If the file is empty, write the header row
if not os.stat(file_path).st_size:
    writer.writerow(HEADER_ROW)

# Create an instance of the dash app
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

# encoding all the images in base64 stored in the local machine
encoded_image_bags = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/logo.jpeg', 'rb').read())
encoded_image_flag = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/flag.png', 'rb').read())
encoded_image_cansat = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/'
                                             'CanSat Logo - Color.png', 'rb').read())
encoded_image_nsut = base64.b64encode(open('/Users/raunitsingh/Desktop/Cansat Stuff/CANSAT GUI/'
                                           'nsut_logo.png', 'rb').read())

# definition of the app
app.layout = html.Div(style={'backgroundColor': colors['background'], 'text-align': 'center'}, children=[
    # The header 1
    html.H1(
        id='heading',
        children='TEAM B.A.G.S. NSUT',
        style={
            'textAlign': 'center',
        }
    ),
    # The header 2
    html.H2(
        id='gcs',
        children='GROUND CONTROL STATION',
        style={
            'textAlign': 'center',
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
    html.Br(),
    html.Br(),
    # Add an input box to write to serial
    html.Div([
        html.Button(id='connect-disconnect', type='submit', value=None, children='DISCONNECT'),
    ]),

    html.Div([html.P(id='terminal_output')]),

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


# This array is to iterate over the main dictionary 'Values' easily
indices_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
indices_data = []  # This list is the indices of the corresponding fields of the packet received
for index in range(len(indices_values)):
    indices_data.append(values[indices_values[index]][3])


resetClickCount = 0  # Global variable to store the click count of the reset button
connectClickCount = 0  # Global variable to store  the click count of the connect/disconnect button
firstTime = True
button_name = 'DISCONNECT'  # Button name: Connect/Disconnect


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
               Output('datatable-container', 'data'),
               Output('connect-disconnect', 'children')],
              [Input('interval-component', 'n_intervals'),
               Input('button', 'n_clicks'),
               Input('connect-disconnect', 'n_clicks')]
              )
def update_graph(n, n_clicks, n_clicks_connector):
    print('N : {}'.format(n))
    global values, df, X, indices_data, indices_values, resetClickCount, firstTime, connectClickCount, my_connector,\
        button_name
    # Here the sensor updating code will be there
    message = ''
    port_not_open = False
    try:
        if my_connector.ser.isOpen():
            message = my_connector.ser.readline()
    except:
        print('Exception: Port not found')
        my_connector.ser = None
        message = 'Port not open!'
        port_not_open = True

    while port_not_open:  # This while loop is in case the device gets ejected!
        try:
            print('Waiting....')
            time.sleep(1)
            if my_connector.connect_disconnect():  # would return true only if the port is reconnected successfully
                port_not_open = False
        except:
            continue

    print(message)
    message = message[:-2]  # to remove '\r' and '\n'
    data = list(message.split(','))  # Converting the message to a list

    # To stabilize the click count of the buttons
    if firstTime:
        if n_clicks is not None:
            resetClickCount = n_clicks
        if n_clicks_connector is not None:
            connectClickCount = n_clicks_connector
        firstTime = False

    # The length of the data should be 17 and the first value should be 1516 which is the team_id
    if len(data) == 17 and data[0] == '1516':
        print('DATA : {}'.format(data))
        for i, j in zip(indices_values, indices_data):
            values[i][0].append(float(data[j]))
        if float(data[values['7'][3]]) > 12:  # If the number of satellites detected is > 12, rewrite the last value
            if len(values['1'][0]) > 1:
                values['7'][0][-1] = values['7'][0][-2]
            else:
                values['7'][0][0] = 12  # Add a 12 if there is no previous value
            data[values['7'][3]] = values['7'][0][-1]

        writer.writerow(data)  # Write the packet received to the .csv file
        X.append(X[-1] + 1)  # Update the x-axis list
        if df.shape[0] > 20:  # if the number of rows is > 20, then we pop the first row
            df = df.iloc[1:]  # Limiting the size of the DataFrame to 20 rows
        df = df.append(pd.Series(data, index=df.columns), ignore_index=True)  # Append the new row

    # Add the data received to the corresponding graphs
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

    # To set the window size
    window_size = 50
    min_x = max(0, X[-1] - window_size)
    max_x = min(X[-1], min_x + window_size)
    range_x = [min_x, max_x]

    # All the layouts of the graphs
    layout_temperature = {
        'title': 'TEMPERATURE(in Celcius)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Temperature')
    }
    layout_pressure = {
        'title': 'PRESSURE(in Pascals)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Pressure')
    }
    layout_voltage = {
        'title': 'Voltage(in Volts)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Voltage')
    }
    layout_altitude = {
        'title': 'ALTITUDE(in meters)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Altitude')
    }
    layout_pitch = {
        'title': 'PITCH(in Degrees)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Pitch')
    }
    layout_roll = {
        'title': 'ROLL(in Degrees)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Roll')
    }
    layout_gps_sats = {
        'title': 'GPS Satellites(integer value)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway':                 ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='GPS Satellites')
    }
    layout_blade_spin_rate = {
        'title': 'BLADE SPIN RATE(in Degrees/sec)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
        'yaxis': dict(linecolor='#669999', linewidth=2, title='Blade Spin Rate')
    }
    layout_bonus_direction = {
        'title': 'BONUS DIRECTION(in Degrees)',
        'plot_bgcolor': colors['GraphSpace'],
        'paper_bgcolor': colors['background'],
        'font': {'color': '#669999'},
        'colorway': ['#FFFF00'],
        'height': '60%',
        'xaxis': dict(linecolor='#669999', linewidth=2, title='Mission Time', range=range_x),
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

    # Reset button logic
    if n_clicks is not None and n_clicks > resetClickCount:
        for j in indices_values:
            values[j][0] = []  # Clear all the deques
        X = list([])
        X.append(0)
        df = df.iloc[0:0]
        resetClickCount = n_clicks  # update the count of the reset clicks
        print('RESET!')

    # Connect/disconnect button logic
    if n_clicks_connector is not None and n_clicks_connector > connectClickCount:
        print('Button Clicked!')
        is_connected = my_connector.connect_disconnect()  # True is returned if the connection is established
        if is_connected:
            button_name = 'DISCONNECT'
        else:
            button_name = 'RECONNECT'
        connectClickCount = n_clicks_connector

    # Return all the fields in order
    return temp, pres, volt, alti, pitc, roll, gps, blade, bonus, df.to_dict('rows'), button_name


# Initialise the app!
if __name__ == '__main__':
    app.run_server(port=8030)

