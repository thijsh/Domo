#!/usr/bin/python

# Import libraries
import soco
import time

# List of all Sonos devices (first is the master)
addresses = ['192.168.1.72', '192.168.1.68', '192.168.1.71', '192.168.1.76']
speakers = [soco.SoCo(address) for address in addresses]
print speakers
sonos = speakers[0]

# 
# sonos = soco.discovery.any_soco()

# List speakers
print "Speakers:"
for speaker in speakers:
	print "-", speaker.player_name, '@', speaker.volume
	# speaker.partymode()
	# print speaker.get_speaker_info()
	volume = max(speaker.volume, 15)
	speaker.volume = 1
	speaker.ramp_to_volume(volume)
	if speaker.is_coordinator:
		print "  - This is the coordinator!"
		sonos = speaker


playlist = sonos.get_sonos_playlist_by_attr('title', 'Eastern')
if playlist:
	sonos.clear_queue()
	sonos.add_uri_to_queue(playlist.resources[0].uri)
	sonos.play_mode = 'SHUFFLE'
sonos.play()
print sonos.get_current_track_info()

# time.sleep(5)


# x-sonos-http:track%3a249951540.mp3?sid=160&flags=8224&sn=5