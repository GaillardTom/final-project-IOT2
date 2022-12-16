#!/usr/bin/python3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as mqtt 
import time
import sensors
import mail
import config
from datetime import datetime
import json


global myMQTTClient



date= datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
print(f"Timestamp:{date}")

# user specified callback function
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


def ConnectAWS(): 
    global myMQTTClient
    # configure the MQTT client
    myMQTTClient= mqtt(config.CLIENT_ID)
    myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
    myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
    myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
    myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
    #Connect to MQTT Host
    if myMQTTClient.connect():
        print('AWS connection succeeded')
        return myMQTTClient
    else: 
        print('AWS connection failed')
        return False



def PublishAWS(payload):
    global myMQTTClient
    myMQTTClient.publish(config.TOPIC, payload, 1)


def setup(): 
    print('setup ...')
    sensors.setup()
    ans = ConnectAWS()
    if(ans): 
        print("AWS connection succeeded")
    else: 
        print("AWS connection failed")
    


def sendMail(): 
    print(f"sending mail to user {userEmail} ...")


def main():
    """
    It checks the status of the sensors and if any of them are out of range, it sends an email and
    activates the buzzer and LED
    """
    while True:
        #sensors.testUsersNotif()
        lightStatus = float(sensors.getLightStatus())
        gasStatus = float(sensors.getGasStatus())
        temp = float(sensors.Temperature())
        if(temp >= config.TEMP_LIMIT_MAX or temp <= config.TEMP_LIMIT_MIN or gasStatus >= config.GAS_LIMIT or lightStatus <= config.LIGHT_LIMIT):
            mail.sendEmail(f"temp: {temp} degrees, gas: {gasStatus}, light: {lightStatus}")
            sensors.Buzz(5)
            sensors.LightLED(5)
        print(f"Gas status: {gasStatus},\nLight Status: {lightStatus},\nTemperature: {temp}")
        payload = {"gas": gasStatus, "light": lightStatus, "temp": temp}
        PublishAWS(json.dumps(payload))
        time.sleep(5)
if __name__ == "__main__": 
    try: 
        setup()
        main() 
    except KeyboardInterrupt:
        print("exiting program")
        sensors.destroy() 
