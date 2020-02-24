import time
import datetime as dt
from tkinter import *
import paho.mqtt.client as mqtt
import os
import csv
# Main Tkinter application
class Application(Frame):	
	
	# Create display elements
	def createWidgets(self):
		self.cur_time = Label(self, textvariable=self.time, font=('Verdana', 20, 'bold'))
		self.time.set("Time")
		self.cur_time.pack() # organize in block
		
		self.temperature1 = Label(self, textvariable=self.temp_data1, font=('Verdana', 20, 'bold'))
		self.temp_data1.set("Temperature SHTC3")
		self.temperature1.pack() # organize in block
		
		self.humidity1 = Label(self, textvariable=self.hum_data1, font=('Verdana', 20, 'bold'))
		self.hum_data1.set("Humidity SHTC3")
		self.humidity1.pack()
		
		self.temperature2 = Label(self, textvariable=self.temp_data2, font=('Verdana', 20, 'bold'))
		self.temp_data2.set("Temperature TMP117")
		self.temperature2.pack()
		
	# Init the variables & start measurements
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.time = StringVar() # used for widget text edit
		self.temp_data1 = StringVar()
		self.hum_data1 = StringVar()
		self.temp_data2 = StringVar()
		self.createWidgets()
		self.pack()
		self.timer()
		
	# show current time	
	def timer(self):
		self.time.set(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		self.cur_time.pack()
		# update time every second
		self.after(1000, self.timer)
		
	# update data received from MQTT broker	
	def receiveData_t1(self, t_data):
		self.temp_data1.set("Temperature SHTC3  : " + t_data+ " oC")
		self.temperature1.pack()
	def receiveData_h1(self, h_data):
		self.hum_data1.set("Humidity SHTC3         : " + h_data+ " %")
		self.humidity1.pack()	
	def receiveData_t2(self, t_data):
		self.temp_data2.set("Temperature TMP117: " + t_data + " oC")
		self.temperature2.pack()	
	
	# write to csv file
	def write_csv_data(self, filename, data, time_data):
		with open(filename, mode = 'a') as f:
			f_writer = csv.writer(f, delimiter = ',')
			f_writer.writerow([data, time_data])

	def write_csv_header(self, filename, header1, header2):
		with open(filename, mode = 'a') as f:
			f_writer = csv.writer(f, delimiter = ',')
			f_writer.writerow([header1, header2])
#########################################################################
# MAIN 
# receive temperature and humidity from sensors through MQTT in real time
##########################################################################
app = Application()

csv_filename_t_tmp117 = "temperature_TMP117.csv"
csv_filename_t_shtc3 = "temperature_SHTC3.csv"
csv_filename_h_shtc3 = "humidity_SHTC3.csv"
header1 = 'temperature'
header2 = 'humidity'
header3 = 'time'

# prepare header for csv file for temperature TMP117
if not(os.path.isfile(csv_filename_t_tmp117)):
    app.write_csv_header(csv_filename_t_tmp117, header1, header3)
# prepare header for csv file for temperature SHTC3
if not(os.path.isfile(csv_filename_t_shtc3)):
    app.write_csv_header(csv_filename_t_shtc3, header1, header3)
# prepare header for csv file for himidity SHTC3	
if not(os.path.isfile(csv_filename_h_shtc3)):
	app.write_csv_header(csv_filename_h_shtc3, header2, header3)	
	
# receive data from MQTT broker and update these values
def messageFunction_t1 (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	app.receiveData_t1(message)
	app.write_csv_data(csv_filename_t_shtc3, message, str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	
client_t1 = mqtt.Client("Client_SHTC3_t") 
client_t1.connect("test.mosquitto.org", 1883) 
client_t1.subscribe("NhanIOT/test/t_data_SHTC3/") 
client_t1.on_message = messageFunction_t1 # Attach the messageFunction to subscription
client_t1.loop_start() # Start the MQTT client

# receive data from MQTT broker and update these values
def messageFunction_h1 (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	app.receiveData_h1(message)
	app.write_csv_data(csv_filename_h_shtc3, message, str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	
client_h1 = mqtt.Client("Client_SHTC3_h") 
client_h1.connect("test.mosquitto.org", 1883) 
client_h1.subscribe("NhanIOT/test/h_data_SHTC3/") 
client_h1.on_message = messageFunction_h1 # Attach the messageFunction to subscription
client_h1.loop_start() # Start the MQTT client

# receive data from MQTT broker and update these values
def messageFunction_t2 (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	app.receiveData_t2(message)
	app.write_csv_data(csv_filename_t_tmp117, message, str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	
client_t2 = mqtt.Client("Client_TMP117") 
client_t2.connect("test.mosquitto.org", 1883) 
client_t2.subscribe("NhanIOT/test/t_data_TMP117/") 
client_t2.on_message = messageFunction_t2 # Attach the messageFunction to subscription
client_t2.loop_start() # Start the MQTT client

app.mainloop()