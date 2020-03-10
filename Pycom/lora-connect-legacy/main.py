import socket
import time
import ubinascii
from network import LoRa
from machine import Pin
from dth import DTH
import _thread
import cayenneLPP



# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0029290')
app_key = ubinascii.unhexlify('C02FBAC4EFFB5C230CED81EEC502F969')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

i = 1
# wait until the module has joined the network
while not lora.has_joined():
    i = i +1
    print(i)
    time.sleep(3)
    print('Not yet joined...')


print('Joined !!!')





# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# configure data rate. 3 = US (not sure why)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)


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
        lpp.add_temperature(result.humidity)
        lpp.send(reset_payload = True)

        time.sleep(30)


_thread.start_new_thread(send_env_data, ())
