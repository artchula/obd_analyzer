#!/usr/bin/env python3

import os
import time
import can
import canapp

db_path = '/home/pi/obd_analyzer/data/storage.db'

# Create a can network interface with a specific name
os.system('sudo ip link add dev can0 type can')
os.system('sudo ip link set can0 up type can bitrate 250000')
#os.system('ip -details -statistics link show can0')

# Create can bus object
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Create notifier object
notifier = can.Notifier(bus, [can.Logger(db_path)])

while True:
    time.sleep(600)

    ts = time.strftime('%Y%m%d', time.localtime())
    canapp.printdb2csv(db_path, ts)

#print('Timeout occurred, no message.')

# To remove the network interface
os.system('sudo ip link del can0')

