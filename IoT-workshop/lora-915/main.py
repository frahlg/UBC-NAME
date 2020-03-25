from network import LoRa
import socket
import ubinascii
import struct
import time

# Initialise LoRa in LORAWAN mode.

#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

lora = LoRa(mode=LoRa.LORAWAN, region = LoRa.US915)
#
# for index in range(0, 7):
#     lora.remove_channel(index)
#
# for index in range(16, 72):
#     lora.remove_channel(index)
#
# lora.add_channel(8, frequency=903900000, dr_min=0, dr_max=3)
# lora.add_channel(9, frequency=904100000, dr_min=0, dr_max=3)
# lora.add_channel(10, frequency=904300000, dr_min=0, dr_max=3)
# lora.add_channel(11, frequency=904500000, dr_min=0, dr_max=3)
# lora.add_channel(12, frequency=904700000, dr_min=0, dr_max=3)
# lora.add_channel(13, frequency=904900000, dr_min=0, dr_max=3)
# lora.add_channel(14, frequency=905100000, dr_min=0, dr_max=3)
# lora.add_channel(15, frequency=905300000, dr_min=0, dr_max=3)
# lora.add_channel(65, frequency=927500000, dr_min=4, dr_max=4)
# lora.add_channel(66, frequency=926900000, dr_min=4, dr_max=4)

#Setting up channels for sub-band 2 for TTN
for index in range(0, 8):
    lora.remove_channel(index)

for index in range(16, 65):
    lora.remove_channel(index)

for index in range(66, 72):
    lora.remove_channel(index)



 # 500KHz uplink larger dr breaks(?)

# create an ABP authentication params
app_eui = ubinascii.unhexlify('70B3D57ED002CAD4')
app_key = ubinascii.unhexlify('99D5B3166C5DC477D74925A2774258F6')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

i = 1
# wait until the module has joined the network
while not lora.has_joined():
    i = i +1
    print(i)
    time.sleep(10)
    print('Not yet joined...')


print('Joined !!!')


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# make the socket non-blocking
s.setblocking(False)

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# get any data received...
data = s.recv(64)
print(data)
