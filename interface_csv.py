from tkinter import *
from tkinter.messagebox import *
import datetime as dt
import time
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
		self.time_t_tmp117 = StringVar()
		self.time_t_shtc3 = StringVar()
		self.time_h_shtc3 = StringVar()
		
		# init at zero
		self.t_tmp117.set("N/A oC")
		self.t_shtc3.set("N/A oC")
		self.h_shtc3.set("N/A %")
		self.time_t_tmp117.set("N/A")
		self.time_t_shtc3.set("N/A")
		self.time_h_shtc3.set("N/A")
		
		# create labels
		self.titleLabel      = Label(self, text="Temperature & Humidity", font=('Verdana', 12, 'bold'))
		self.cur_time        = Label(self, textvariable = self.time, font=('Verdana', 12, 'bold'))
		self.tempTMP117Label = Label(self, text="Temperature TMP117")
		self.tempSHTC3Label  = Label(self, text="Temperature SHTC3")
		self.humidSHTC3Label = Label(self, text="Humidity SHTC3 ")
		
		self.tempTMP117Value = Label(self, textvariable = self.t_tmp117)
		self.tempSHTC3Value  = Label(self, textvariable = self.t_shtc3)
		self.humidSHTC3Value = Label(self, textvariable = self.h_shtc3)
		
		self.tempTMP117Time = Label(self, textvariable = self.time_t_tmp117)
		self.tempSHTC3Time  = Label(self, textvariable = self.time_t_shtc3)
		self.humidSHTC3Time = Label(self, textvariable = self.time_h_shtc3)
		
		# organized with grid
		self.titleLabel.grid(row=0, column=1)
		self.cur_time.grid(row=1, column=1)
		
		self.tempTMP117Label.grid(row=2, column=0)
		self.tempTMP117Value.grid(row=2, column=1)
		self.tempTMP117Time.grid(row=2, column=2)
		
		self.tempSHTC3Label.grid(row=3, column=0)
		self.tempSHTC3Value.grid(row=3, column=1)
		self.tempSHTC3Time.grid(row=3, column=2)
		
		self.humidSHTC3Label.grid(row=4, column=0)
		self.humidSHTC3Value.grid(row=4, column=1)	
		self.humidSHTC3Time.grid(row=4, column=2)	
		
		# timer
		self.timer()
		
	# check max value for temp and humidity	
	def checkTemp( self, t_data ):
		# show alarm msg if over max temp
		if t_data > float(SensorInterface.max_temp):
			showinfo("Alert", "The temperature is now " + self.t_tmp117.get() 
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
		
	# update data read from csv files
	def receiveData_t1(self, t_data):
		self.t_shtc3.set(t_data + " oC")
	def receiveData_h1(self, h_data):
		self.h_shtc3.set(h_data + " %")
	def receiveData_t2(self, t_data):
		self.t_tmp117.set(t_data + " oC")
	def receiveData_t2_time(self, time_data):
		self.time_t_tmp117.set(time_data)	
	
	
###########################################################################	
n = 1
app = SensorInterface()
while True:
	with open("temperature_TMP117.csv") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
			
		for i in range(n):
			next(csv_reader)
		row = next(csv_reader)
		print(row[1])
			
		app.receiveData_t2(row[0])
		app.receiveData_t2_time(row[1])	
		n += 1	
		time.sleep(1)
			
# loop
app.mainloop()


