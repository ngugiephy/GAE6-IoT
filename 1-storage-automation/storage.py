import network
import time
from machine import Pin
from umqttsimple import MQTTClient

wlan=network.WLAN(network.STA_IF)
wlan.active(True)


wlan.connect("Raspberry(Cloud & IOT","abraham123")
time.sleep(5)
print(wlan.isconnected())

locker1=Pin(0,Pin.OUT)
locker2=Pin(1,Pin.OUT)
locker3=Pin(2,Pin.OUT)
locker4=Pin(3,Pin.OUT)
status=Pin(1,Pin.OUT)


mqtt_server='192.168.1.4'
client_id='Pico_locker'
topic_sub='bench/locker'

def message(topic,msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg=msg.decode('utf-8')
    print(msg)
    if msg=="1":
        locker1.on()   
        time.sleep(1)
        locker1.off() 
    if msg=="2":
        locker2.on()   
        time.sleep(1)
        locker2.off() 
    if msg=="3":
        locker3.on()   
        time.sleep(1)
        locker3.off() 
    if msg=="4":
        locker4.on()   
        time.sleep(1)
        locker4.off() 
        
       
def mqtt_connect():
        client=MQTTClient(client_id,mqtt_server)
        client.set_callback(message)
        client.connect()
        print('Connected to %s MQTT Broker'%(mqtt_server))
        return client
   
def recconect():
        print('Failed to connect to MQTT Broker. Reconnecting...')
        time.sleep(5)
        machine.reset()


try:
    client=mqtt_connect()
except OSError as e:
    recconect()
while True:
    client.subscribe(topic_sub)
    status.off() 
    time.sleep(5)
    status.on()
    
    


