#!/usr/bin/python

# import libraries
import soco, time
from phue import Bridge
from random import randint, random
from pprint import pprint

# Connect to bridge
b = Bridge('192.168.178.22')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
# b.get_api()


#####################


# Print sensor names
print "Sensors:"
for s in b.sensors:
  print s.sensor_id, ":", s.name
  pprint(s.state)
print




