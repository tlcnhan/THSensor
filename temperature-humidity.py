import os
import time
import csv
import datetime as dt
import smbus
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

###################################################################
# TMP117 sensor with temperature
##################################################################
class TMP117Sensor(object):
    tmp117_temp_max_value = 25
    
    i2c_ch = 1
    # TMP117 address on the I2C bus
    i2c_address = 0x48
    # Register addresses
    reg_temp = 0x00
    reg_config = 0x01
    # Initialize I2C (SMBus)
    bus = smbus.SMBus(i2c_ch)
    
    def init_i2c_smbus(self):   
        # Read the CONFIG register (2 bytes)
        val = TMP117Sensor.bus.read_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_config, 2)
        print("Old CONFIG:", val)
        #val2 = bus.read_i2c_block_data(i2c_address2, reg_config2, 2)
        # Set to 4 Hz sampling (CR1, CR0 = 0b10)
        val[1] = val[1] & 0b00111111
        val[1] = val[1] | (0b10 << 6)

        # Write 4 Hz sampling back to CONFIG
        TMP117Sensor.bus.write_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_config, val)

        # Read CONFIG to verify that we changed it
        val = TMP117Sensor.bus.read_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_config, 2)
        print("New CONFIG:", val)
        
    # Read temperature registers and calculate Celsius from the TMP117 sensor
    def read_temp(self):
        # Read temperature registers
        val = TMP117Sensor.bus.read_i2c_block_data(TMP117Sensor.i2c_address, TMP117Sensor.reg_temp, 2)
        temp_c = (val[0] << 8) | (val[1] )
        # Convert registers value to temperature (C)
        temp_c = temp_c * 0.0078125

        return temp_c
    # write header to csv file
    def write_csv_header(self, filename, header1, header2):
        with open(filename, mode = 'a') as f:
            f_writer = csv.writer(f, delimiter = ',')
            f_writer.writerow([header1, header2])
     
    # write data to csv file
    def write_csv_data(self, filename, t_data, time_data):
        with open(filename, mode = 'a') as f:
            f_writer = csv.writer(f, delimiter = ',')
            f_writer.writerow([t_data, time_data])
    
    # check if temperature cross max value
    def check_cross_max(self):
        if self.read_temp() > TMP117Sensor.tmp117_temp_max_value :
            return True
        else:
            return False

#############################################################################
# SHTC3 sensor with temparature and humidity
# OS shell commands to register the SHTC3 sensor at 0x70
#os.system("sudo su")
#os.system("echo shtc1 0x70 > /sys/bus/i2c/devices/i2c-1/new_device")
#os.system("exit")
# can install lm-sensors to verfiy the temperator/humidity with this software
#############################################################################
class SHTC3Sensor(object):
    temperature_data_path = "/sys/class/hwmon/hwmon1/temp1_input"
    humidity_data_path = "/sys/class/hwmon/hwmon1/humidity1_input"
    
    shtc3_temp_max_value = 24
    shtc3_humid_max_value = 20
    
    #read humidity value and temperature from the SHTC3 sensor
    def read_humidity(self):
        humidity = open(SHTC3Sensor.humidity_data_path,'r')
        h_data = int(humidity.read())/1000   
        return h_data

    def read_temperature(self):
        temperature = open(SHTC3Sensor.temperature_data_path,'r')
        t_data = int(temperature.read())/1000  
        return t_data

    # write to csv file
    def write_csv_data(self, filename, t_data, h_data, time_data):
        with open(filename, mode = 'a') as f:
            f_writer = csv.writer(f, delimiter = ',')
            f_writer.writerow([t_data, h_data, time_data])

    def write_csv_header(self, filename, header1, header2, header3):
        with open(filename, mode = 'a') as f:
            f_writer = csv.writer(f, delimiter = ',')
            f_writer.writerow([header1, header2, header3])
    
   # check if temperature cross max value
    def check_cross_max_temp(self):
        if self.read_temperature() > SHTC3Sensor.shtc3_temp_max_value :
            return True
        else:
            return False
    # check if humidity cross max value
    def check_cross_max_humid(self):
        if self.read_humidity() > SHTC3Sensor.shtc3_humid_max_value :
            return True
        else:
            return False
        
    # send MQTT message to the broker
    def sendMQTT(self,temperature, humidity, time):
        topic_name = "NhanIOT/test/"
        mqtt_host = "test.mosquitto.org"
        
        data_dict = {"Temperature": temperature, "Humidity": humidity,"time": str(dt.datetime.now())}
        data_out = json.dumps(data_dict)
        publish.single(topic_name, data_out, hostname = mqtt_host)
        
    def sendMQTT_alarm(self, temperature):
        topic_name = "NhanIOT/test/alarm"
        mqtt_host = "test.mosquitto.org"
        
        data_dict = {"Temperature": temperature, "Humidity": humidity,"time": str(dt.datetime.now())}
        data_out = json.dumps(data_dict)
        publish.single(topic_name, data_out, hostname = mqtt_host)
        msg = "Temperature cross max value " + str(SHTC3Sensor.shtc3_temp_max_value)
        publish.single(topic_name, msg, hostname = mqtt_host)

###################################################
        
###################################################
# MAIN
##################################################
csv_filename1 = 'temp-humid.csv'
csv_filename2 = 'temp.csv'
header1 = 'temperature'
header2 = 'humidity'
header3 = 'time'
#register SHTC3 sensor to the system, must run in su mode
#os.system("echo shtc1 0x70 > /sys/bus/i2c/devices/i2c-1/new_device")

sensor1 = SHTC3Sensor()
sensor2 = TMP117Sensor()
sensor2.init_i2c_smbus()
# prepare header for csv file
if not(os.path.isfile(csv_filename1)):
    sensor1.write_csv_header(csv_filename1, header1, header2, header3)
if not(os.path.isfile(csv_filename2)):
    sensor2.write_csv_header(csv_filename2,header1, header3)

while True:
    temperature2 = round(sensor2.read_temp(),1)
    print("Temperature from TMP117 : ", temperature2, "C")
    
    temperature1 = round(sensor1.read_temperature(),1)
    print("Temperature from SHTC3  : ", temperature1, "C")
    
    humidity = round(sensor1.read_humidity(),1)
    print("Humidity from SHTC3     : ", humidity, "%")
    
    time_now = str(dt.datetime.now())
    
    sensor1.write_csv_data(csv_filename1, temperature1, humidity, time_now)
    sensor2.write_csv_data(csv_filename2, temperature2, time_now)
    
    sensor1.sendMQTT(temperature1, humidity, time_now)
    if sensor1.check_cross_max_temp():
        print ("Temperature now %s cross max value %s!" % (round(temperature1,1), SHTC3Sensor.shtc3_temp_max_value))
        sensor1.sendMQTT_alarm(temperature1)
    else:
        print("Temperature is still under max value!")
    
    time.sleep(1)
