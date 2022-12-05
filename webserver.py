import os
import socket
import paho.mqtt.client as paho
from threading import Thread
os.system('kill -9 $(lsof -t -i:8000)') # this command is used to kill port 8000 if

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
server="192.168.1.4"
paho=paho.Client()

#connect to MQTT Broker
if paho.connect(server,1883,60)!=0:
        print("Could not connect to the MQTT Broker")
        syys.exit(-1)
else:        
        print("Connected to MQTT Broker")
        #print(paho.connect())
# Create socket create
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

def mqtt_publish(payload,a):
     while a:
         paho.publish("bench/light",payload)
         print("Published")
         #paho.disconnect()
         a=False
def host():
    while True:    
        client,addr = server.accept()

        request = client.recv(1024).decode()
        #print(request)
        req=request.find("light=on")
        reqst=request.find("light=off")
        if req==6:
            print("Light on")
            payload="on"
        elif reqst==6:
            print("Light Off")
            payload="off"
        else:
            payload="wait"

        # Send HTTP response
        response = 'HTTP/1.0 200 OK\n\n'
        html="""<!DOCTYPE html><html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>html {
        font-family: Helvetica;
        display: inline-block;
        margin: 0px auto; 
        text-align: center;
    }
.buttonGreen {
    background-color: #4CAF50;
    border: 2px solid #000000;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px; 
    margin: 4px 2px;
    cursor: pointer;
     }
.buttonRed {
    background-color: #D11D53;
    border: 2px solid #000000;;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
 }

</style>
</head>
    <body>
        <center><h1>Control Panel</h1></center><br><br>
        <form><center>
        <center> <button class="buttonGreen" name="light" value="on" type="subm>
        <br><br>
        <center> <button class="buttonRed" name="light" value="off" type="submi>
        </form>
        <br><br>
        <br><br>
        <p>%s<p></p> </body></html>"""
        client.sendall(response.encode())
        client.sendall(html.encode())
        #client.sendall("Hello world".encode())
        a=True
        thread1=Thread(target=mqtt_publish,args=(payload,a))
        print("Thread started")
        thread1.start()

        client.close()

host()

# Close socket
server.close()
