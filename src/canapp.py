#!/usr/bin/env python3

import os
import time
import sqlite3
import csv

msg_path = '/home/pi/obd_analyzer/data/can_msg/'
db_path = '/home/pi/obd_analyzer/data/storage.db'


def printdb2csv(indb, date):

    # Open the db file
    conn = sqlite3.connect(indb)
    try:
        # Create cursor
        c = conn.cursor()

        # Create folder
        isExists = os.path.exists(msg_path)
        if not isExists:
            os.makedirs(msg_path)

        # Time format conversion
        timearray = time.strptime(date, '%Y%m%d')
        timestamp = time.mktime(timearray)
        tt_start = timestamp
        tt_stop = timestamp + 60 * 60 * 24

        # Print msg to csv
        cursor = c.execute('SELECT ts, arbitration_id, data, extended FROM messages WHERE ts >= ? AND ts < ?', (tt_start, tt_stop))
        with open(msg_path + date +'.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in cursor:
                str_tmp = [(row[0] - tt_start) / 3600] \
                        + [hex(row[1])] \
                        + ['*' + row[2].hex()] \
                        + [row[3]] 
                writer.writerow(str_tmp)

    except Exception as e:
        print('Failed to print data:', e)

    finally:
        # Close the db file
        conn.close()


