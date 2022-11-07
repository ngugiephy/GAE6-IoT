import network
import time
from machine import Pin
from umqttsimple import MQTTClient

wlan=network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect("Gearbox Staff","Staff@Gearbox")
time.sleep(5)
print(wlan.isconnected())

lock=Pin(0,Pin.OUT)
status=Pin(1,Pin.OUT)

mqtt_server='192.168.0.212'
client_id='PicoW'
topic_sub='door'

def message(topic,msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg=msg.decode('utf-8')
    print(msg)
    if msg=="open":
        lock.on()    
        time.sleep(3)
        lock.off()
       
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
    
    

