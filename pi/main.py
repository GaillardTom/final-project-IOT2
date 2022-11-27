from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as mqtt 
import time
import sensors
import mail

def setup(): 
    sensors.setup()
    print('setup')

def sendMail(): 
    print(f"sending mail to user {userEmail} ...")

def main():
    """
    It checks the status of the sensors and if any of them are out of range, it sends an email and
    activates the buzzer and LED
    """
    while True:
        #sensors.testUsersNotif()
        lightStatus = sensors.getLightStatus()
        gasStatus = sensors.getGasStatus()
        temp = sensors.Temperature()
        if(float(temp) >= 30 or float(temp) <= 15 or float(gasStatus) >= 100 or lightStatus <= 45):
            mail.sendEmail(f"temp: {temp} degrees, gas: {gasStatus}, light: {lightStatus}")
            sensors.Buzz(5)
            sensors.LightLED(5)
        print(f"Gas status: {gasStatus},\nLight Status: {lightStatus},\nTemperature: {temp}")
        time.sleep(1)
if __name__ == "__main__": 
    try: 
        setup()
        main() 
    except KeyboardInterrupt:
        print("exiting program")
        sensors.destroy() 
