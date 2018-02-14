#!/usr/bin/python

# import libraries
import soco, time
from phue import Bridge
from random import randint, random

# Connect to bridge
b = Bridge('192.168.1.65')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
# b.get_api()


#####################


# Print light names
print "Lights:"
for l in b.lights:
  print l.light_id, ":", l.name, "- Colormode =", l.colormode
print

# # Print group names with lights
# print "Groups and lights:"
# for g in b.get_group():
# 	print "- ", b.get_group(g, 'name')
# 	print get_group(g, 'lights')
# 	for l in b.get_group(g, 'lights'):
# 		print "  - ", l.name


#####################


# test lights
print "Testing living room lights color fade"

# Set all lights to on
for l in b.lights:
	l.on = True
	#l.colormode = 'hs' # Hue/saturation
	l.transitiontime = 30

while True:
	speed = randint(1, 50)
	for l in b.lights: 
		l.transitiontime = speed
		l.brightness = randint(0, 254)
		l.xy = [ random(), random() ]
	time.sleep(speed/10)


