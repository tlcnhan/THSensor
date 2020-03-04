## by Mhamed BenCherqui
########################
import os.path
import time
import datetime

import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from itertools import count

DEV_REG = '/sys/bus/i2c/devices/i2c-1/new_device'
DEV_REG_PARAM = 'shtc1 0x70'
DEV_TMP = '/sys/class/hwmon/hwmon1/temp1_input'
DEV_HUM = '/sys/class/hwmon/hwmon1/humidity1_input'

def init():
    if os.path.isfile(DEV_TMP) and os.path.isfile(DEV_HUM):
        print("...")
    else:
        with open(DEV_REG, 'wb') as f:
            f.write(DEV_REG_PARAM)
def read():
   

    try:
        with open(DEV_TMP, 'rb') as f:
            val = f.read().strip()
            temperature = float(int(val)) / 1000

        with open(DEV_HUM, 'rb') as f:
            val = f.read().strip()
            humidity = float(int(val)) / 1000
                
        return [temperature,humidity]
        
    except:
        print("bus error")
    
init()


def write_csv():
    with open('temp_humidity.csv', 'a') as file:

        values=read()
        data=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+","+str(round(values[0],2))+","+str(round(values[1],2))
        file.write(data)
        file.write('\n')


plt.style.use('fivethirtyeight')
time_axis = []
temp_val = []
hum_val = []
index = count()
fig,ax1 = plt.subplots()

def animate(i):

    time_axis.append(next(index))
    values=read()
    temp_val.append(values[0])
    hum_val.append(values[1])
    plt.cla()
    
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Temperature', color=color)
    ax1.plot(time_axis, temp_val, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Humidity', color=color)
    ax2.plot(time_axis, hum_val, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
  
    plt.tight_layout()
    
ani = FuncAnimation(plt.gcf(), animate, interval=500)
# 
plt.tight_layout()
plt.show()




class Sensors(Frame):

    def __init__(self,master):

        Frame.__init__(self)
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Sensors Connectivity")
        self.master.geometry("600x600")  # width x length
        self.frame1 = Frame(self)
        self.frame1.pack()
        
        self.label1 = Label(self, text="Temperature")
        self.label1.place(x=5, y=10)
        #print(self.label1.cget("background"))
        
        self.label2 = Label(self, text="Humidity")
        self.label2.place(x=5, y=130)
        

        
        self.text1 = Entry(self.frame1, name="temp")
        self.text1.pack(padx=20, pady=10)
        self.chosenUnit=IntVar()
        self.chosenUnit.set(0)
        self.radiob1 = Radiobutton(self.frame1, variable=self.chosenUnit, text="Cel",  value=0)
        self.radiob1.pack(padx=35, pady=5)
        self.radiob2 = Radiobutton(self.frame1, variable=self.chosenUnit,text="Fah",  value=1)
        self.radiob2.pack(padx=20, pady=10)
        self.text2 = Entry(self.frame1, name="hum")
        self.text2.pack(padx=20, pady=10)
        self.btnmean=Button(self,text="T_mean")
        self.btnmean.pack()
        with open('temp_humidity.csv', 'a') as file:
            header = str(('Time_Stamp, Temperature, Humidity'))
            file.write(header)
            file.write('\n')
      
        self.ReadTemp()
        
        

    def ReadTemp(self):
        write_csv()
        unit=self.chosenUnit.get()
        try:
            self.text1.delete(0, 'end')
            self.text2.delete(0, 'end')
            t=read()
            if unit==0:
                self.text1.insert(INSERT, round(t[0],2))
                if t[0]>32:
                    self.label1.configure(bg="red")
                else:
                    self.label1.configure(bg="#d9d9d9")
            else:
                self.text1.insert(INSERT, round((t[0]*9/5)+32,2))
            self.text2.insert(INSERT, round(t[1],2))
            if t[1]>50:
                self.label2.configure(bg="red")
            else:
                self.label2.configure(bg="#d9d9d9")
            self.after(2000, self.ReadTemp)
            
        except:
            print("Error")


root = tk.Tk()
Sensors(root)
root.mainloop()
