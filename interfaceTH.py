from tkinter import *
from tkinter.messagebox import *
import csv
import smbus
import os
import time
import datetime as dt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from itertools import count
# values
csv_filename = 'temp_humidity.csv'
temp_header = 'temperature'
humid_header = 'humidity'
time_header = 'time'

max_temp  = 25
max_humid = 25

# sensor interface by Denis
class SensorInterface(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Sensor information")
        self.master.geometry("500x250")  # width x length
        
        # create labels, entries, buttons
        self.connectButton = Button(self, text=" Connect ", command=self.pressedConnect)
        
        self.tempLabel  = Label(self, text=" Temperature ")
        self.tempEntry  = Entry(self, name="temp", width = "5")
        
        self.humidLabel = Label(self, text=" Humidity ")
        self.humidEntry = Entry(self, name="humid", width = "5")
        
        self.tempAlert  = Label(self, text = "     ", bg="#d9d9d9" )
        self.humidAlert = Label(self, text = "     ", bg="#d9d9d9")
        
        self.tempStatButton   = Button(self, text = "STAT \n temperature", command=self.pressedTempStat)
        self.humidStatButton  = Button(self, text="STAT\n humidity", command=self.pressedHumidStat)

        grad = ["\N{DEGREE SIGN}C", "F"]
        i = 4
        self.chosenGrad = StringVar()
        self.chosenGrad.set(grad[0])
        for g in grad:
            aButton = Radiobutton(self, text=g, value=g, variable = self.chosenGrad)
            aButton.grid(row = 2, column =i, padx = 2, pady = 2)
            i += 1

        self.connectButton.grid(row =1, column =2, padx = 50, pady = 10) #side = CENTER
        self.tempLabel.grid( row=2, column=1)  # side = CENTER
        self.humidLabel.grid(row=3, column=1)  # side = CENTER
        
        self.tempEntry.grid(row=2, column=2)
        self.humidEntry.grid(row=3, column=2)
        
        self.tempAlert.grid(row =2, column = 6)
        self.humidAlert.grid(row=3, column=6)
        
        self.tempStatButton.grid(row=5, column=2)
        self.humidStatButton.grid(row=5, column=4)
        
    # when connect button pressed
    def pressedConnect(self):   
        self.measure()
    # when stat temp button pressed
    def pressedTempStat(self):   
        self.animationT()
    # when stat humid button pressed
    def pressedHumidStat(self):   
        self.animationH()
        
    # conversion C to F
    def CtoF(self, c_temp):
        return round(((c_temp * 9/5) + 32), 1)
        
    # write to csv file
    def write_csv_data(self, filename, time_data, t_data, h_data):
        with open(filename, mode = 'a') as f:
            f_writer = csv.writer(f, delimiter = ',')
            f_writer.writerow([time_data, t_data, h_data])

    def write_csv_header(self, filename, header1, header2, header3):
        with open(filename, mode = 'a') as f:
            f_writer = csv.writer(f, delimiter = ',')
            f_writer.writerow([header1, header2, header3])
            
    #measure
    init_count = 0
    def measure(self):
        # sensors
        h_sensor = SHTC3Sensor()
        t_sensor = TMP117Sensor()
        
        if SensorInterface.init_count == 0:
            t_sensor.init_tmp117()
            h_sensor.init_shtc3()
            SensorInterface.init_count += 1
            
        time_now = str(dt.datetime.now())
        
        temperature = round(t_sensor.read_temperature(),1)
        humidity = round(h_sensor.read_humidity(),1)
        # write to csv file
        self.write_csv_data(csv_filename, time_now, temperature, humidity)
        
        if self.checkTemp(temperature):
            self.tempAlert.config(bg="red")
        else:
            self.tempAlert.config(bg="#d9d9d9")
        
        # convert C to F if F was chosen
        if self.chosenGrad.get() == "F":
            temperature = self.CtoF(temperature)  
           
        self.tempEntry.delete(0, END)
        self.tempEntry.insert(0, str(temperature))  
        print("Temperature from TMP117 : ", temperature) 
        
        if self.checkHumid(humidity):
            self.humidAlert.config(bg="red")
        else:
            self.humidAlert.config(bg="#d9d9d9")
            
        self.humidEntry.delete(0, END)
        self.humidEntry.insert(0, str(humidity))
        print("Humidity from SHTC3     : ", humidity, "%")
        
        # wait for 1s
        self.after(1000,self.measure)
        
    # real-time animation for temperature and humidity from M'hamed
    def animationT(self):
        # sensors
        t_sensor = TMP117Sensor()
        if SensorInterface.init_count == 0:
            t_sensor.init_tmp117()
            h_sensor.init_shtc3()
            SensorInterface.init_count += 1
        
        def animate(i):
            time_axis.append(next(index))
            t_value = t_sensor.read_temperature()
            temp_val.append(t_value)

            plt.cla()
    
            color = 'tab:red'
            ax1.set_xlabel('time (s)')
            ax1.set_ylabel('Temperature \N{DEGREE SIGN}C', color=color)
            ax1.plot(time_axis, temp_val, color=color)
            ax1.tick_params(axis='y', labelcolor=color)
  
            plt.tight_layout()
        # anime    
        plt.style.use('fivethirtyeight')
        time_axis = []
        temp_val = []
     
        index = count()
        fig,ax1 = plt.subplots()    
        ani = FuncAnimation(plt.gcf(), animate, interval=500)

        plt.tight_layout()
        plt.show()
    # humidity    
    def animationH(self):
        # sensors
        h_sensor = SHTC3Sensor()
        if SensorInterface.init_count == 0:
            t_sensor.init_tmp117()
            h_sensor.init_shtc3()
            SensorInterface.init_count += 1
        
        def animate(i):
            time_axis.append(next(index))  
            h_value = h_sensor.read_humidity()
            hum_val.append(h_value)
            plt.cla()
    
            color = 'tab:blue'
            ax2.set_xlabel('time (s)')
            ax2.set_ylabel('Humidity %', color=color)
            ax2.plot(time_axis, hum_val, color=color)
            ax2.tick_params(axis='y', labelcolor=color)
  
            plt.tight_layout()
        # anime    
        plt.style.use('fivethirtyeight')
        time_axis = []
        hum_val = []
        index = count()
        fig,ax2 = plt.subplots()    
        ani = FuncAnimation(plt.gcf(), animate, interval=500)

        plt.tight_layout()
        plt.show()
        
    # check max value for temp and humidity	
    def checkTemp( self, t_data ):
	# change label color to red if cross over max values
        if t_data > float(max_temp):     
            return True
        
    def checkHumid( self, h_data ):      
        if h_data > float(max_humid):
            return True
###################################################################
# TMP117 sensor with temperature
##################################################################
class TMP117Sensor(object):
    
    i2c_ch = 1
    # TMP117 address on the I2C bus
    i2c_address = 0x48
    # Register addresses
    reg_temp = 0x00
    reg_config = 0x01
    # Initialize I2C (SMBus)
    bus = smbus.SMBus(i2c_ch)
    
    def init_tmp117(self):   
        # Read the CONFIG register (2 bytes)
        val = TMP117Sensor.bus.read_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_config, 2)
        #print("Old CONFIG:", val)
        #val2 = bus.read_i2c_block_data(i2c_address2, reg_config2, 2)
        # Set to 4 Hz sampling (CR1, CR0 = 0b10)
        val[1] = val[1] & 0b00111111
        val[1] = val[1] | (0b10 << 6)

        # Write 4 Hz sampling back to CONFIG
        TMP117Sensor.bus.write_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_config, val)

        # Read CONFIG to verify that we changed it
        val = TMP117Sensor.bus.read_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_config, 2)
        #print("New CONFIG:", val)
        print("TMP117 sensor init")
    # Read temperature registers and calculate Celsius from the TMP117 sensor
    def read_temperature(self):
        # Read temperature registers
        val = TMP117Sensor.bus.read_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_temp, 2)
        temp_c = (val[0] << 8) | (val[1] )
        # Convert registers value to temperature (C)
        temp_c = temp_c * 0.0078125

        return temp_c

#############################################################################
# SHTC3 sensor with temparature and humidity
# use sudo python3 xxx.py to execute the code
# can install lm-sensors to verifiy the temperator/humidity with this software
#############################################################################
class SHTC3Sensor(object):
    # SHTC3 system file to get temp and humidity
    DEV_REG = '/sys/bus/i2c/devices/i2c-1/new_device'
    DEV_REG_PARAM = 'shtc1 0x70'
    DEV_TMP = '/sys/class/hwmon/hwmon1/temp1_input'
    DEV_HUM = '/sys/class/hwmon/hwmon1/humidity1_input'
    
    # init SHTC3 sensor
    def init_shtc3(self):
        if os.path.isfile(SHTC3Sensor.DEV_TMP) and os.path.isfile(SHTC3Sensor.DEV_HUM):
            print("OK")
        else:
            with open(SHTC3Sensor.DEV_REG, 'w') as f:
                f.write(SHTC3Sensor.DEV_REG_PARAM)
        print("SHTC3 sensor init")
    # Read humidity values from SHTC3
    def read_humidity(self):
        with open(SHTC3Sensor.DEV_HUM, 'r') as f:
            val = f.read().strip()
            humidity = float(int(val)) / 1000
        return humidity
###########################################################################    
def main():
    
    interface = SensorInterface()   
    
    # prepare header for csv file
    if not(os.path.isfile(csv_filename)):
        interface.write_csv_header(csv_filename, time_header, temp_header, humid_header)
           
    interface.mainloop()    

if __name__ == "__main__":
    main()
