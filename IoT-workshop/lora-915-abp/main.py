from network import LoRa
import socket
import ubinascii
import ustruct
import time

# Initialise LoRa in LORAWAN mode.


lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an ABP authentication params
#app_eui = ubinascii.unhexlify('70B3D57ED0029290')
#app_key = ubinascii.unhexlify('C02FBAC4EFFB5C230CED81EEC502F969')

# dev_addr_TTN is shown in reverse order, that's why the additional code is needed below.

dev_addr_TTN = '2602109F'
dev_addr2 = ubinascii.unhexlify(dev_addr_TTN)
dev_addr = ustruct.pack('<l',ustruct.unpack(">l", ubinascii.unhexlify(dev_addr_TTN))[0])

nwk_swkey = ubinascii.unhexlify('57922EDE8D9F16C59B71ACF6B10E59F8')
app_swkey = ubinascii.unhexlify('A7D110F8417E3B329547529004D0B2E5')


lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
# make the socket non-blocking
s.setblocking(True)

i = 1
# wait until the module has joined the network
while True:
    i = i +1
    print(i)
    s.send(bytes(i))
    time.sleep(30)
