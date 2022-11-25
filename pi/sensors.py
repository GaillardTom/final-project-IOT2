import RPi.GPIO as gpio
import time 
import os 
import ADC0832_tmp as adc


# Code for the sensors used in the rasperry pi 

def readSensorForTemperature(id):
    """
    It opens the sensor file, reads the text file, closes the file, gets the second line of the file,
    gets the temperature data, converts the temperature to celsius, formats the temperature to 3 decimal
    places, and returns the temperature.
    
    :param id: The ID of the sensor you want to read
    :return: The temperature in Celsius
    """
    tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")  # open the sensor file

    text = tfile.read()  # read the text file

    tfile.close()  # close the file

    secondline = text.split("\n")[1]  # get the second line of the file

    temperaturedata = secondline.split(" ")[9]  # get the temperature data

    # get the temperature from the sensor
    temperature = float(temperaturedata[2:])

    temperature = temperature / 1000  # convert the temperature to celsius
    print("Sensor: " + id + " . Current temperature: %0.3f (" % temperature)

    temperature = "%0.3f" % temperature  # format the temperature to 3 decimal places

    return temperature  # return the temperature


def Temperature():
    """
    It reads the temperature from the sensor and returns the temperature.
    :return: The temperature of the sensor
    """

    try:
        global temperature
        count = 0
        sensor = ""
        for file in os.listdir("/sys/bus/w1/devices"):
            if file.startswith("28-"):
                count = count + 1  # increment the count by 1
                # read the temperature of the sensor
                temp = readSensorForTemperature(file)
                time.sleep(1)  # wait for 1 second
                return temp  # return the temperature
        if (count == 0):
            print("No sensors found")
            return False  # Display that there is no sensor found
    except KeyboardInterrupt:
        destroy()
def getLightStatus(): 
    res = adc.getResult(0)
    vol = 3.3/255*res
    print(f"res light: {res}")
    return res


def getGasStatus(): 
    res = adc.getResult1()
    vol = 3.3/255*res
    print(f"res gas: {res}")
    return res


def setup(): 
    gpio.setmode(gpio.BCM)
    adc.setup()

def main(): 
    setup() 
    while True:  
        Temperature()
        lightStatus = getLightStatus()
        gasStatus = getGasStatus()
        print(f"Gas status: {gasStatus}")
        print(f"Light Status: {lightStatus}")
        print("Temperature: " + str(Temperature()))
        time.sleep(1)



def destroy(): 
    adc.destroy()
    gpio.cleanup()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program...")
        adc.destroy()

