#!/usr/bin/env python
"""
Check for Jenkins jobs status and run shell command if job is not OK.
"""
import os
import sys
import time

import serial
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.exceptions import JenkinsAPIException


URL = 'http://jenkins.example.ru/'
USERNAME = 'jenkins'
PASSWORD = 'secret'
JOBS = ['build', 'test', 'lint']
TTY = '/dev/tty.usbserial-A900FYDU'


def job_failed(connect, job_name):
    """
    Returns boolean job status (True - success, False - fail).
    """
    if job_name not in connect:
        return True

    last_build = connect[job_name].get_last_build()

    if last_build.is_running():
        return False

    build_status = last_build.get_status()

    if build_status in ('FAIL', 'FAILED', 'FAILURE', 'ERROR', 'REGRESSION'):
        return True

    return False


def send_to_transmitter(device, command):
    """
    Send command to device and die on error.
    """
    device.write("Achtung %s\n" % command)

    result = device.readline().strip()
    if result != 'OK':
        print("ERROR: device response is not OK")
        sys.exit(1)


if __name__ == '__main__':
    if not os.path.exists(TTY):
        print("ERROR: device '%s' is not exists" % TTY)
        sys.exit(1)

    try:
        connect = Jenkins(URL, USERNAME, PASSWORD)

        if any(job_failed(connect, job_name) for job_name in JOBS):
            transmitter = serial.Serial(TTY, 9600)

            if transmitter.readline().strip() != 'Ready for achtung':
                print("ERROR: device is not initialized")
                sys.exit(1)

            send_to_transmitter(transmitter, 'ON')
            time.sleep(5)
            send_to_transmitter(transmitter, 'OFF')

    except JenkinsAPIException:
        sys.exit(1)
