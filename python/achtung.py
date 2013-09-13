#!/usr/bin/env python
"""
Send 'ON' or 'OFF' command to achtung transmitter.
"""
from __future__ import print_function
import os
import sys
import serial


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: achtung /dev/ttyXX <ON|OFF>")
        sys.exit(1)

    tty = sys.argv[1]
    if not os.path.exists(tty):
        print("ERROR: device '%s' is not exists" % tty)
        sys.exit(1)

    command = sys.argv[2]
    if command not in ('ON', 'OFF'):
        print("ERROR: unknown command '%s'" % command)
        sys.exit(1)

    transmitter = serial.Serial(tty, 9600)

    if transmitter.readline().strip() != 'Ready for achtung':
        print("ERROR: device is not initialized")
        sys.exit(1)

    transmitter.write("Achtung %s\n" % command)

    result = transmitter.readline().strip()
    if result != 'OK':
        print("ERROR: device response is not OK")
        sys.exit(1)
