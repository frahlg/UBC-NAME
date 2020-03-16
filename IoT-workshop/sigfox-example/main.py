import time
from machine import Pin
from dth import DTH
import _thread

# Type 0 = dht11
# Type 1 = dht22

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
time.sleep(2)







from network import Sigfox; import binascii;



def send_env_data():
    while True:
        result = th.read()
        while not result.is_valid():
            time.sleep(.5)
            result = th.read()
        print('Temp:', result.temperature)
        print('RH:', result.humidity)
        time.sleep(30)

_thread.start_new_thread(send_env_data, ())
