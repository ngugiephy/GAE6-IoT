import time
import network
import socket
from machine import Pin

led = Pin(0, Pin.OUT)
status=Pin("LED",Pin.OUT)
ledState = 'LED State Unknown'

ssid = 'Gearbox Staff'
password = 'Staff@Gearbox'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


html = """<!DOCTYPE html><html>
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
/* text-decoration: none;
font-size: 30px;
margin: 2px;
cursor: pointer; 
}*/
</style>
</head>
    <body>
        <center><h1>Control Panel</h1></center><br><br>
        <form><center>
        <center> <button class="buttonGreen" name="light" value="off" type="submit">LIGHT ON</button>
        <br><br>
        <center> <button class="buttonRed" name="light" value="on" type="submit">LIGHT OFF</button>
        </form>
        <br><br>
        <br><br>
        <p>%s</p>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# Listen for connections, serve client
while True:
    try:
        
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        light_on = request.find('light=on')
        light_off = request.find('light=off')
        
        print( 'light on = ' + str(light_on))
        print( 'light off = ' + str(light_off))
        
        if light_on == 8:
            print("led on")
            led.value(1)
        if light_off == 8:
            print("led off")
            led.value(0)
        
        ledState = "Light is ON" if led.value() == 0 else "Light is OFF" # a compact if-else statement

        stateis = ledState
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
