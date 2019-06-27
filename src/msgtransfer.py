#!/usr/bin/env python3

import os
import can

os.system('sudo ip link set can0 type can bitrate 250000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native

#msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], extended_id=False)

f = open("../data/dev1/test.txt", "a")

msg = True
while msg is not None:
    msg = can0.recv(10.0)
    f.write("%s\n" % msg)
    print(msg)
else:
    f.close()
    print('Timeout occurred, no message.')

os.system('sudo ifconfig can0 down')
