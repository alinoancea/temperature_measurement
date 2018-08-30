#!/usr/bin/env python3

import sys
import time

try:
    import Adafruit_DHT
except:
    raise ImportError('[!] Error importing [Adafruit_DHT]')


def calibrate():
    """
    Reads 2 times from the sensor to be sure that has the right data
    """
    for _ in range(2):
        get_temp_hum()


def get_temp_hum(sensor_type=Adafruit_DHT.DHT11, pin_no=4):
    """
    Return temperature and humidity as a dictionary; on error returns None
    @params
    :sensor_type: Adafruit_DHT.{DHT11,DHT22} - sensor type which will be questioned
    :pin_no: int - pin number on Raspberry Pi
    """
    if not pin_no:
        raise ValueError('[!] Specify a pin number!')
    humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin_no)
    if temperature or humidity:
        return {'temperature': temperature, 'humidity': humidity}
    else:
        return None


def log_temperature_and_humidity(path=None, delay=300, once=False):
    """
    Loggs temperature and humidity if a path exists, else print on stdout
    @params
    :path: string - path where to put loggs
    :delay: int - waiting time between readings (in seconds)
    """
    calibrate()
    while True:
        i = get_temp_hum()
        info_formated = '%s;%s;%s' % (time.strftime('%d-%m-%y %H:%M'), i['temperature'], i['humidity'])
        if once:
            return info_formated
        if path:
            with open(path, 'a') as f:
                f.write(info_formated + '\n')
        else:
            print(info_formated)
        time.sleep(delay)
