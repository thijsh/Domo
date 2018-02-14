#!/usr/bin/python

from time import sleep
from multiping import multi_ping
import ping

addrs = {
  'xanne': '192.168.1.69',
  'thijs': '192.168.1.73',
}
last_state = 'none'

while True:
	# Multiping gives socket errors on Windows
	# responses, no_responses = multi_ping(addrs, 1, 1)
	# print responses

	# Start with a none state
	state = 'none'
	for name, addr in addrs.items():
		speed = ping.do_one(addr, 1, 64) # Timeout of 1 second, send 64 bytes
		if speed is not None:
			state = name if state == 'none' else 'both'
		# print name, "@", addr, "=", speed
	if state != last_state:
		print "State changed:", state
		last_state = state
	sleep(1)
