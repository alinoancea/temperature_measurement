#!/usr/bin/env python3

import os
import sys
import time
import _thread

import bottle

from log_temperature import log_temperature_and_humidity


HOME_PATH = os.path.dirname(os.path.realpath(__file__))
HISTORY = '%s/temperature_history.log' % HOME_PATH



class LogFile:


    def __init__(self, filename):
        self.filename = filename
        self.sep = '=' * 50
        self.write('%s\n' % self.sep)
        self.write('[*] Server started @ %s\n%s\n' % (time.strftime('%H:%M:%S, %d.%m.%Y'), self.sep))


    def write(self, s):
        open(self.filename, 'a').write(s)


    def flush(self):
        pass



@bottle.route('/')
def home():
    info = ''
    first = True
    with open(HISTORY) as ff:
        for i, l in enumerate(ff):
            ll = l.strip().split(';')

            dt = time.localtime(float(ll[0]))
            m = int(time.strftime('%m', dt)) - 1

            dt = time.strftime('%Y,', dt) + str(m) + time.strftime(',%d,%H,%M,%S', dt)
            info += '' if first else ','
            info += '[new Date(%s),%s,%s]' % tuple([dt] + ll[1:])

            if first:
                first = False
    return open('%s/templates/template.html' % HOME_PATH).read().replace('myData', info)


if __name__ == '__main__':
    _thread.start_new_thread(log_temperature_and_humidity, (HISTORY,))
    if not os.path.exists('%s/logs' % HOME_PATH):
        os.makedirs('%s/logs' % HOME_PATH)
    sys.stderr = sys.stdout = LogFile('%s/logs/server.log' % HOME_PATH)
    bottle.run(host='0.0.0.0', port='16722')  # 0x4152 = RA = 16722
