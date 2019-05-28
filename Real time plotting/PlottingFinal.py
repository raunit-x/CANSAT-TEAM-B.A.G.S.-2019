import serial
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

SERIAL_PORT = '/dev/tty.usbserial-AL017DBE'
BAUD_RATE = 9600
time_out = 0.99 
FILE_NAME = "cansat.csv"
HEADER_ROW = ['TEAM_ID','MISSION_TIME','PACKET COUNT','ALTITUDE','PRESSURE',
'TEMP','VOLTAGE','GPS TIME', 'GPS LATITUDE', 'GPS LONGITUDE', 'GPS ALTITUDE',
'GPS SATS', 'PITCH', 'ROLL', 'BLADE SPIN RATE', 'SOFTWARE STATE', 'BONUS DIRECTION']

fig = plt.figure()
axs = [[], [], [], [], [], [], [], []]
colors = 'rgbcmykw'
style.use('ggplot')

indices1 = [2, 3, 4, 5, 6, 12, 13, 14, 16]
for i in range(len(axs)):
    axs[i] = fig.add_subplot(4,2,i + 1)
    
    
plt.show()
fig.canvas.set_window_title('REALTIME DATA PLOTTING')
if __name__ == '__main__':
    ser = serial.Serial(SERIAL_PORT,BAUD_RATE, timeout = time_out)
myFile = open('/Users/raunitsingh/Desktop/cansat.csv','wb') # open in binary
writer = csv.writer(myFile)
writer.writerow(HEADER_ROW)
i = 0
xar = []
packet_count, altitude, pressure, temp, voltage, pitch, roll, blade_spin_rate, bonus_direction = [], [], [], [], [], [], [], [], []
array = []
array.append(packet_count)
array.append(altitude)
array.append(pressure)
array.append(temp)
array.append(voltage)
array.append(pitch)
array.append(roll)
array.append(blade_spin_rate)
array.append(bonus_direction)

def animate(I):
    global i, array, axs, colors
    message = ser.readline()
    message = message[:-2] #to remove '\r' and '\n' 
    data = list(message.split(','))
    if len(data) > 16:
        #data = data[:-2]
        print(data)
        indices = [2, 3, 4, 5, 6, 12, 13, 14, 16]
        writer.writerow(data)
        xar.append(int(i))
        for j in range(len(array)):
            array[j].append(data[indices[j]])
        i += 1
        
        for j in range(len(axs)):
            axs[j].title.set_text(HEADER_ROW[indices[j]])
            axs[j].plot(xar, array[j], color = colors[j], linewidth = 0.75)
            

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()





