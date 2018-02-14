#!/usr/bin/python

# import libraries
import soco
from phue import Bridge
import random
import threading
import time
import ping


# Shared object to share state and settings between threads
class Shared(object):
	# Monitor these phone IP addresses
	phone_addresses = {
	  'xanne': '192.168.1.69',
	  'thijs': '192.168.1.73',
	}

	# Order of the Philips Hue lights in the house
	order = [7, 9, 8, 12, 2, 3, 10, 1, 11, 13, 4, 6, 5]
	
	# Color ranges to use for each state
	ranges = {
		'none': [ [0.33, 0.33], [0.33, 0.33] ],
		'both': [ [0.0, 0.0], [0.7, 0.8] ],
		'thijs':  [ [0.25, 0.0], [0.6, 0.25] ],
		'xanne': [ [0.4, 0.3], [0.7, 0.5] ],
	}
	
	# Light speed (time between each individual light fades) maxmum in 1/10 seconds
	speed = 2
	
	# Light fade (time an individual light takes to fade color) maximum in 1/10 seconds
	fade = 10

	# Default brightness for all lights (this can be overridden in the app)
	brightness = 127

	# Sonos addresses
	sonos_addresses = [
		'192.168.1.68',
		'192.168.1.71',
		'192.168.1.72',
		'192.168.1.74',
	]

	# Sonos playlists
	sonos_playlists = {
		'none': '',
		'both': 'Both',
		'thijs': 'Thijs',
		'xanne': 'Xanne',
	}

	# Default minimum volume for all speakers (this can be overridden in the app)
	volume = 15
	
	# Init the state
	def __init__(self, state='none'):
		self.state = state


# Networking thread that pings cellphones
def networking(shared):
	last_state = shared.state
	while True:
		# Start with a none state
		state = 'none'
		for name, addr in shared.phone_addresses.items():
			try:
				speed = ping.do_one(addr, 1, 64) # Timeout of 1 second, send 64 bytes
				if speed is not None:
					state = name if state == 'none' else 'both'
			except:
				print "Ping failed. Network issue?"
		shared.state = state
		if shared.state != last_state:
			print "State changed:", shared.state
			last_state = shared.state
		time.sleep(1)


# Philips Hue color fade thread
def hue(shared):
	last_state = shared.state

	# Connect to bridge
	b = Bridge('192.168.1.65')

	# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
	b.connect()

	# Set the default color range
	shared.r = shared.ranges[shared.state]

	# Set all lights to on
	print "Lights in the house:"
	for l in b.lights:
		print l.light_id, ":", l.name, "-", ("On" if l.on else "Off"), "- Colormode =", l.colormode
		l.on = True
		l.transitiontime = 10
		l.brightness = shared.brightness
		l.xy = [ 0.33, 0.33 ] # CIE 1931
	print ""

	# Light fading function
	def fade():
		last_state = shared.state
		while True:
			# Generate random varibles for this iteration
			speed = random.randint(1, shared.speed) # between lights
			fade = random.randint(speed, shared.fade) # per light
			# brightness = random.randint(0, 254)
			color = [ random.uniform(shared.r[0][0], shared.r[1][0]), random.uniform(shared.r[0][1], shared.r[1][1]) ]
			for number in shared.order:
				l = b.lights[number-1]
				if l.colormode != 'xy' or l.on != True:
					return
				l.transitiontime = fade
				# l.brightness = brightness
				l.xy = color
				time.sleep(speed/10)

				# Check for state change
				if shared.state != last_state:
					shared.r = shared.ranges[shared.state]
					last_state = shared.state
					print "Color scheme changed to:", shared.state
					break

	while True:
		time.sleep(1)
		if shared.state != last_state:
			if shared.state != 'none' and last_state == 'none':
				print "Starting fade with light state", shared.state
				shared.r = shared.ranges[shared.state]
				fade()
				print "Fading paused because light was turned off or mode changed by the app..."
			else:
				last_state = shared.state



# Sonos music playlist thread
def sonos(shared):
	last_state = shared.state

	# Init all Sonos devices
	speakers = [soco.SoCo(address) for address in shared.sonos_addresses]
	sonos = None
	print "Speakers:"
	for speaker in speakers:
		print "-", speaker.player_name, '@', speaker.volume
		# print speaker.get_speaker_info()
		volume = max(speaker.volume, shared.volume) # minimum of 15 is default
		speaker.volume = 1
		speaker.ramp_to_volume(volume)
		if sonos is None and speaker.is_coordinator:
			print "  - This is the main coordinator!"
			sonos = speaker
	print ""

	while True:
		if shared.state != last_state:
			last_state = shared.state
			if shared.sonos_playlists[shared.state]:
				try:
					playlist = sonos.get_sonos_playlist_by_attr('title', shared.sonos_playlists[shared.state])
					print "Starting playlist:", shared.sonos_playlists[shared.state]
					sonos.clear_queue()
					sonos.add_uri_to_queue(playlist.resources[0].uri)
					sonos.play_mode = 'SHUFFLE'
					sonos.play()
				except:
					print "PLAYLIST NOT FOUND! Create one with this name..."
			else:
				sonos.stop()
		time.sleep(1)


# Init the threads
print "Starting Domo Arigato automation for Hue and Sonos."
print "Press CONTROL-C to exit...\n"
shared = Shared()
t = threading.Thread(name='hue', target=hue, args=(shared,))
t.setDaemon(True)
t.start()
time.sleep(3) # Allow for debug printing
t = threading.Thread(name='sonos', target=sonos, args=(shared,))
t.setDaemon(True)
t.start()
t = threading.Thread(name='networking', target=networking, args=(shared,))
t.setDaemon(True)
t.start()


# Keep doing nothing, let the threads thread
while True:
	time.sleep(1)

