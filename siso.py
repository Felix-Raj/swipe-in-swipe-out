#! /usr/local/bin/python3.8
# change shebang line as per requirement, required 3.5 or above

from datetime import datetime, timedelta
import argparse
import os
import json
from functools import reduce


def parse_to_t(t):
    return time(*(map(int, t.split(':'))))


def get_args(o):
    return map(int, o.split(':'))


def seconds_to_h_m_s(seconds):
    x = seconds
    h, m, s = (
        ph := x // (60 * 60),
        pm := ((x // 60) - (ph * 60)),
        ps := (x - ph * 60 * 60 - pm * 60))
    return h, m, s


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
                if not isinstance(self.logs['ext'], list):
                    self.logs['ext'] = [self.logs['ext'], ]
                if not isinstance(self.logs['red'], list):
                    self.logs['red'] = [self.logs['red'], ]
        except FileNotFoundError:
            self.logs = {
                'si': datetime.now().timestamp(),
                'so': (datetime.now() + timedelta(hours=self.ioh,
                                                  minutes=self.iom))
                .timestamp(),
                'ext': [],
                'red': [],
            }
            self.save()
        self.i = self._i()
        self.o = self._o()

    def si(self, h, m):
        t = datetime.now()
        sit = datetime(t.year, t.month, t.day, h, m)
        esot = sit + timedelta(hours=self.ioh, minutes=self.iom)

        self.logs['si'] = sit.timestamp()
        self.logs['so'] = esot.timestamp()
        self.logs['ext'] = []
        self.logs['red'] = []

        self.save()

    def ext(self, h=0, m=0):
        csot = datetime.fromtimestamp(self.logs['so'])
        by = timedelta(hours=h, minutes=m)
        self.logs['ext'].append(by.seconds)
        self.logs['so'] = (csot + by).timestamp()
        self.save()

    def red(self, h=0, m=0):
        csot = datetime.fromtimestamp(self.logs['so'])
        by = timedelta(hours=h, minutes=m)
        self.logs['red'].append(by.seconds)
        self.logs['so'] = (csot - by).timestamp()
        self.save()

    def _o(self):
        return datetime.fromtimestamp(self.logs['so'])

    def _i(self):
        return datetime.fromtimestamp(self.logs['si'])

    def e(self):
        a = timedelta(seconds=sum(self.logs['ext']))
        return a

    def r(self):
        return timedelta(seconds=sum(self.logs['red']))

    def change_log_file(self, file_location):
        self.log_file = file_location
        self._init_logs_()

    def save(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f)

    def __str__(self):
        def ch(seconds):
            h, m, s = seconds_to_h_m_s(seconds)
            return f'{h:02.0f}:{m:02.0f}:{s:02.0f}'

        ext = ch(self.e().seconds)
        red = ch(self.r().seconds)
        e = '   '.join(map(ch, self.logs['ext']))
        r = '   '.join(map(ch, self.logs['red']))
        return f"I:{self._i()}\n" \
            f"O:{self._o()}\n" \
            f"S:{self._o()-self._i()-self.e()+self.r()}\n" \
            f"TE:{ext}\n" \
            f"\t{e}\n" \
            f"TR:{red}\n" \
            f"\t{r}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--si', action='store', type=str,
                        required=False, help='Swipe in time')
    parser.add_argument('--ext', action='store', type=str,
                        required=False, help='Extend swipe out time')
    parser.add_argument('--red', action='store', type=str,
                        required=False, help='Reduce swipe out time')
    parser.add_argument('--iot', action='store', type=str, required=False,
                        default='08:00', help='Change time in office, '
                                              'useful only aloing with *si*')
    parser.add_argument('-t', action='store_true',
                        required=False, help='Use when testing the script')
    parser.add_argument('-o', action='store_true',
                        required=False, help='Expected out time')
    parser.add_argument('-v', action='store_true',
                        required=False, help='Verbose')

    args = parser.parse_args()

    d = D(*get_args(args.iot))

    if args.t:
        d.change_log_file(os.path.expanduser('~/.testsisologs.json'))

    for x in ('si', 'ext', 'red'):
        v = getattr(args, x)
        if v:
            getattr(d, x)(*get_args(v))
    if args.v:
        print(d)
    if not args.v:
        print(d.o)


"""x=timedelta(minutes=17, seconds=9, hours=3).seconds
h, m, s = (ph:=x//(60*60), pm:=((x//60)-(ph*60)), ps:=(x-ph*60*60-pm*60))
print(m, s, h)"""
