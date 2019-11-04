#!/usr/bin/env python3

import os
import time
import sqlite3
import csv

msg_path = '/home/pi/obd_analyzer/data/can_msg/'
db_path = '/home/pi/obd_analyzer/data/storage.db'


def printdb2csv(indb, date, start_t, stop_t):

    # Open the db file
    conn = sqlite3.connect(indb)
    try:
        # Create cursor
        cursor = conn.cursor()

        # Create folder
        isExists = os.path.exists(msg_path)
        if not isExists:
            os.makedirs(msg_path)

        # Time format conversion
        timearray = time.strptime(date, '%Y%m%d')
        timestamp = time.mktime(timearray)
        tt_start = timestamp + 60 * 60 * start_t
        tt_stop = timestamp + 60 * 60 * stop_t

        # Print msg to csv
        csvfile = open(msg_path + date + '_' + str(start_t) + '_' + str(stop_t) + '.csv', 'w', newline='')
        writer = csv.writer(csvfile)
        cursor.execute('SELECT ts, arbitration_id, data, extended FROM messages WHERE ts >= ? AND ts < ?', (tt_start, tt_stop)) 
        for row in cursor.fetchall():
            str_tmp = [(row[0] - timestamp) / 3600] \
                    + [hex(row[1])] \
                    + ['*' + row[2].hex()] \
                    + [row[3]] 
            writer.writerow(str_tmp)

    except Exception as e:
        print('Failed to print data:', e)

    finally:
        # Close csv file
        csvfile.close()
        # Close the cursor
        cursor.close()
        # Close the db file
        conn.close()


ts = time.strftime('%Y%m%d', time.localtime())
#ts = '20191026'

printdb2csv(db_path, ts, 0, 2)
printdb2csv(db_path, ts, 3, 5)
printdb2csv(db_path, ts, 6, 8)
printdb2csv(db_path, ts, 9, 11)
printdb2csv(db_path, ts, 12, 14)
printdb2csv(db_path, ts, 15, 17)
printdb2csv(db_path, ts, 18, 20)
printdb2csv(db_path, ts, 21, 23)

