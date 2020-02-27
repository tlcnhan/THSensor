from tkinter import *
from tkinter.messagebox import *
import datetime as dt
import time
import paho.mqtt.client as mqtt
import os
import csv  

class SensorInterface( Frame ):
	max_temp = 24
	max_humid = 25
	
	def __init__( self ):    
		Frame.__init__( self )
		self.pack( expand = YES, fill = BOTH )
		self.master.title( "Sensors Data" )
		self.master.geometry( "450x160" )  # width x length
		self.time = StringVar() # used for widget text edit
		self.t_tmp117 = StringVar()
		self.t_shtc3 = StringVar()
		self.h_shtc3 = StringVar()
		# init at zero
		self.t_tmp117.set("N/A oC")
		self.t_shtc3.set("N/A oC")
		self.h_shtc3.set("N/A %")
		# create labels and entries
		self.titleLabel      = Label(self, text="Temperature & Humidity", font=('Verdana', 12, 'bold'))
		self.cur_time        = Label(self, textvariable = self.time, font=('Verdana', 12, 'bold'))
		self.tempTMP117Label = Label(self, text="Temperature TMP117")
		self.tempSHTC3Label  = Label(self, text="Temperature SHTC3")
		self.humidSHTC3Label = Label(self, text="Humidity SHTC3 ")
		
		self.tempTMP117Value = Label(self, textvariable = self.t_tmp117)
		self.tempSHTC3Value  = Label(self, textvariable = self.t_shtc3)
		self.humidSHTC3Value = Label(self, textvariable = self.h_shtc3)
		
		# organized with grid
		self.titleLabel.grid(row=0, column=1)
		self.cur_time.grid(row=1, column=1)
		self.tempTMP117Label.grid(row=2, column=0)
		self.tempTMP117Value.grid(row=2, column=1)
		self.tempSHTC3Label.grid(row=3, column=0)
		self.tempSHTC3Value.grid(row=3, column=1)
		self.humidSHTC3Label.grid(row=4, column=0)
		self.humidSHTC3Value.grid(row=4, column=1)	
			
		# timer
		self.timer()
	# check max value for temp and himidity	
	def checkTemp( self, t_data ):
		# show alarm msg if over max temp
		if t_data > float(SensorInterface.max_temp):
			showinfo("Alarm", "The temperature is now " + self.t_tmp117.get() 
			+ " !\n crossed max value " + str(SensorInterface.max_temp) + " oC" )
	def checkHumid( self, h_data ):
		# show alarm msg if over max temp
		if h_data > float(SensorInterface.max_humid):
			showinfo("Alarm", "The humidity is now " + self.h_shtc3.get() 
			+ " !\n crossed max value " + str(SensorInterface.max_humid) + " %" )		
	# show current time	
	def timer(self):
		self.time.set(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		# update time every second
		self.after(1000, self.timer)
		
	# update data received from MQTT broker	
	def receiveData_t1(self, t_data):
		self.t_shtc3.set(t_data + " oC")
	def receiveData_h1(self, h_data):
		self.h_shtc3.set(h_data + " %")
	def receiveData_t2(self, t_data):
		self.t_tmp117.set(t_data + " oC")	
	
	# write to csv file
	def write_csv_data(self, filename, data, time_data):
		with open(filename, mode = 'a') as f:
			f_writer = csv.writer(f, delimiter = ',')
			f_writer.writerow([data, time_data])

	def write_csv_header(self, filename, header1, header2):
		with open(filename, mode = 'a') as f:
			f_writer = csv.writer(f, delimiter = ',')
			f_writer.writerow([header1, header2])
###########################################################################		

app = SensorInterface()

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
	# check humid
	app.checkHumid(float(message))
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
	# check temp
	app.checkTemp(float(message))
	app.write_csv_data(csv_filename_t_tmp117, message, str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	
client_t2 = mqtt.Client("Client_TMP117") 
client_t2.connect("test.mosquitto.org", 1883) 
client_t2.subscribe("NhanIOT/test/t_data_TMP117/") 
client_t2.on_message = messageFunction_t2 # Attach the messageFunction to subscription
client_t2.loop_start() # Start the MQTT client


# loop
app.mainloop()
  
