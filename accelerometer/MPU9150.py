# this file read data from MPU9150, parse and plot the data in realtime, and save data to a csv file
import serial
import sys
import time
import serial.tools.list_ports
import numpy as np
from prompter import yesno
import csv
import datetime
import collections
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
#auto determine the serial port
#ports = list(serial.tools.list_ports.comports())
port = '/dev/ttyUSB0'

#set port parameters
ser =serial. Serial(port,38400,timeout=1)

#open serial port
ser.close()
ser.open()
if ser.isOpen():
    print(ser.name +' is open')

# structure and print out data continously 
#choose whether to save data for later use. data will be stored in .csv format
flag_save = yesno('Save data in csv file? ')
if flag_save:
    fname = raw_input('Enter file name (default to current datetime):')
    if len(fname)<1:
        fname = str(datetime.datetime.now())
    fname = './data/'+fname+'.csv'


# plotly init
tls.set_credentials_file(username='pcg', api_key='xsdl3c6elu')
credentials=tls.get_credentials_file()
N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)

# Create a trace
trace = go.Scatter(
    x = random_x,
    y = random_y
)

data = [trace]

# Plot and embed in ipython notebook!
py.iplot(data, filename='basic-line')

# py.sign_in('PythonAPI','xsdl3c6elu')
# data_struct = np.zeros(1000, dtype=[('Ax',int),('Ay',int),('Az',int),('Gx',int),('Gy',int),('Gz',int),('Mx',int),('My',int),('Mz',int)])
data_list = collections.deque([None]*1000, maxlen=1000)
# data_list=list()                
data_dict = dict()
i=0
while True:
    out = ser.readline() 
    if out.startswith('a/g/m'):
       data_raw = out.split()
       if len(data_raw) == 10:          
               #print data_raw[1:]
               # data_struct[i]=tuple(map(int,data_raw[1:]))
               data_dict={'Ax':data_raw[1],'Ay':data_raw[2],'Az':data_raw[3],'Gx':data_raw[4],'Gy':data_raw[5],'Gz':data_raw[6],'Mx':data_raw[7],'My':data_raw[8],'Mz':data_raw[9]}
               data_list.append(data_dict)
               # print data_struct[i]
               print data_dict
               i=i+1
    if i>10:break
    
if flag_save:
    with open(fname, 'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=['Ax','Ay','Az','Gx','Gy','Gz','Mx','My','Mz'])
        writer.writeheader()
        writer.writerows(data_list)
#realtime plotting in time domain

#realtime plotting in frequency domain
