import time
from tkinter import *
import paho.mqtt.client as mqtt
# Main Tkinter application
class Application(Frame):	
	
	# Create display elements
	def createWidgets(self):
		self.temperature = Label(self, textvariable=self.temp_data, font=('Verdana', 20, 'bold'))
		self.temp_data.set("Temperature SHTC3")
		self.temperature.pack()
		
		self.humidity = Label(self, textvariable=self.hum_data, font=('Verdana', 20, 'bold'))
		self.hum_data.set("Humidity SHTC3")
		self.humidity.pack()
		
		self.temperature2 = Label(self, textvariable=self.temp_data2, font=('Verdana', 20, 'bold'))
		self.temp_data2.set("Temperature TMP117")
		self.temperature2.pack()
		
	# Init the variables & start measurements
	def __init__(self, master=None):
		Frame.__init__(self, master)
		
		self.temp_data = StringVar()
		self.hum_data = StringVar()
		self.temp_data2 = StringVar()
		self.createWidgets()
		self.pack()

	def receiveData_t1(self, t_data):
		self.temp_data.set("Temperature SHTC3  : " + t_data)
		self.temperature.pack()
	def receiveData_h1(self, h_data):
		self.hum_data.set("Humidity SHTC          : " + h_data)
		self.humidity.pack()	
	def receiveData_t2(self, t_data):
		self.temp_data2.set("Temperature TMP117: " + t_data)
		self.temperature2.pack()	
#########################################################################
# MAIN 
# receive temperature and humidity from sensors through MQTT in real time
##########################################################################
app = Application()
# Our "on message" event
def messageFunction_t1 (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	app.receiveData_t1(message)

client_t1 = mqtt.Client("Client_SHTC3_t") 
client_t1.connect("test.mosquitto.org", 1883) 
client_t1.subscribe("NhanIOT/test/t_data_SHTC3/") 
client_t1.on_message = messageFunction_t1 # Attach the messageFunction to subscription
client_t1.loop_start() # Start the MQTT client

# Our "on message" event
def messageFunction_h1 (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	app.receiveData_h1(message)

client_h1 = mqtt.Client("Client_SHTC3_h") 
client_h1.connect("test.mosquitto.org", 1883) 
client_h1.subscribe("NhanIOT/test/h_data_SHTC3/") 
client_h1.on_message = messageFunction_h1 # Attach the messageFunction to subscription
client_h1.loop_start() # Start the MQTT client

# Our "on message" event
def messageFunction_t2 (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	app.receiveData_t2(message)

client_t2 = mqtt.Client("Client_TMP117") 
client_t2.connect("test.mosquitto.org", 1883) 
client_t2.subscribe("NhanIOT/test/t_data_TMP117/") 
client_t2.on_message = messageFunction_t2 # Attach the messageFunction to subscription
client_t2.loop_start() # Start the MQTT client

app.mainloop()