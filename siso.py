#! /usr/bin/python3.5
# change shebang line as per requirement, required 3.5 or above

from datetime import datetime, timedelta
import argparse, os, json

def parse_to_t(t):
    return time(*(map(int, t.split(':'))))

def get_args(o):
    return map(int, o.split(':'))

class D(object):
    def __init__(self, ioh=8, iom=0):
        self.log_file = os.path.expanduser('~/.sisologs.json')
        self.logs = dict()
        self.ioh, self.iom = ioh, iom

        self._init_logs_()

    def _init_logs_(self):
        try:
            with open(self.log_file) as f:
                self.logs = json.load(f)
        except FileNotFoundError:
            self.logs = {
                'si': datetime.now().timestamp(),
                'so': (datetime.now()+timedelta(hours=self.ioh, minutes=self.iom))
                    .timestamp()
                    }
            self.save()

    def si(self, h, m):
        t = datetime.now()
        sit = datetime(t.year, t.month, t.day, h, m)
        esot = sit + timedelta(hours=self.ioh, minutes=self.iom)

        self.logs['si'] = sit.timestamp()
        self.logs['so'] = esot.timestamp()

        self.save()

    def ext(self, h=0, m=0):
        csot = datetime.fromtimestamp(self.logs['so'])
        self.logs['so'] = (csot + timedelta(hours=h, minutes=m)).timestamp()
        self.save()

    def red(self, h=0, m=0):
        csot = datetime.fromtimestamp(self.logs['so'])
        self.logs['so'] = (csot - timedelta(hours=h, minutes=m)).timestamp()
        self.save()

    def o(self):
        return datetime.fromtimestamp(self.logs['so'])

    def save(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--si', action='store', type=str, required=False, help='Swipe in time')
    parser.add_argument('--ext', action='store', type=str, required=False, help='Extend swipe out time')
    parser.add_argument('--red', action='store', type=str, required=False, help='Reduce swipe out time')
    parser.add_argument('--iot', action='store', type=str, required=False, default='08:00', help='Change time in office, useful only aloing with *si*')
    parser.add_argument('-t', action='store_true', required=False, help='Use when testing the script')
    parser.add_argument('-o', action='store_true', required=False, help='Expected out time')


    args = parser.parse_args()

    d = D(*get_args(args.iot))

    if args.t:
        d.log_file = os.path.expanduser('~/.testsisologs.json')
        d._init_logs_()

    for x in ('si', 'ext', 'red'):
        v = getattr(args, x)
        if v:
            getattr(d, x)(*get_args(v))
    
    print(d.o())
    
