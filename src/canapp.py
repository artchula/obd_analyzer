#!/usr/bin/env python3

import os
import time
import sqlite3
import csv

msg_path = '/home/pi/obd_analyzer/data/can_msg/'


def printdb2csv(indb, date):
    # Time format conversion
    timearray = time.strptime(date, '%Y%m%d')
    timestamp = time.mktime(timearray)
    tt_start = timestamp
    tt_stop = timestamp + 60 * 60 * 24
#    print(date + ':' + str(timestamp))

    # Open the db file
    conn = sqlite3.connect(indb)
    c = conn.cursor()

    # Create folder
    isExists = os.path.exists(msg_path)
    if not isExists:
        os.makedirs(msg_path)

    # Print db msg to csv
    cursor = c.execute('SELECT ts, arbitration_id, data, extended FROM messages WHERE ts >= ? AND ts < ?', (tt_start, tt_stop))
    with open(msg_path + date +'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in cursor:
            str_tmp = [(row[0] - tt_start) / 3600] \
                    + [hex(row[1])] \
                    + ['*' + row[2].hex()] \
                    + [row[3]] 
            writer.writerow(str_tmp)
#           print(str_tmp)

    # Close the db file
    conn.close()


