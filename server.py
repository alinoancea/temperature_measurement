#!/usr/bin/env python3

import os
import sys
import daemon
import _thread

import bottle

from log_temperature import log_temperature_and_humidity


HOME_PATH = os.path.dirname(os.path.realpath(__file__))
HISTORY = '%s/temperature_history.log' % HOME_PATH


@bottle.route('/')
def home():
    try:
        with open(HISTORY) as ff:
            return ff.read().replace('\n', '<br />')
    except:
        with open(HISTORY, 'w') as ff:
            pass
        return ''


if __name__ == '__main__':
    _thread.start_new_thread(log_temperature_and_humidity, (HISTORY,))
    bottle.run(host='0.0.0.0', port='8888')