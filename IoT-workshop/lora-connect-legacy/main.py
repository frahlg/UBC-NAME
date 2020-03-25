import socket
import time
import ubinascii
from network import LoRa
from machine import Pin
from dth import DTH
import _thread
import CayenneLPP
import pycom

# Initialise LoRa in LORAWAN mode.s
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED002CAF4')
app_key = ubinascii.unhexlify('FDB54488C69B60A4FB878051B49C7666')


lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

#pycom.rgbled(0x7f7f00)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(5)
    print('Trying to join TTN Network!')

print('Network joined!')
#pycom.rgbled(0x007f00) #green


# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# configure data rate. 3 = US (not sure why)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

lpp = CayenneLPP.CayenneLPP(size = 100, sock = s)


# Type 0 = dht11
# Type 1 = dht22

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
time.sleep(2)

def send_env_data():
    while True:
        result = th.read()
        while not result.is_valid():
            time.sleep(1)
            result = th.read()
        print('Temp:', result.temperature)
        print('RH:', result.humidity)
        lpp.add_temperature(result.temperature)
        lpp.add_relative_humidity(result.humidity)
        lpp.send(reset_payload = True)
        time.sleep(30)


_thread.start_new_thread(send_env_data, ())
