#! /usr/bin/python3.5

from datetime import datetime, timedelta
import json

class MDay(object):
	fields = ('si', 'tio', 'ext', 'red')

	def __init__(self, si, tio, ext, red):
		self.si = si
		self.tio = tio
		self.ext = ext
		self.red = red

	@property
	def so(self):
		return self.si + (
			self.total_ext - self.total_red)

	@property
	def total_ext(self):
		return sum(timedelta(),self.ext[:])

	@property
	def total_red(self):
		return sum(self.red)

	def to_json(self):
		return json.dumps(
				{x: getattr(self, x) for x in self.fields}
			)

	def from_json(self, json_d):
		return MDay(**json.loads(json_d))


def test_MDay():
	si = datetime.today()
	tio = timedelta()
	ext = [timedelta(), ]
	red = [timedelta(), ]

	mday = MDay(si, tio, ext, red)
	assert mday.so == mday.si


if __name__ == '__main__':
	test_MDay()