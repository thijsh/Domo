#!/usr/bin/python
# coding: utf-8

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



'''´´
Sensor types:
- Daylight = generic
- CLIPGenericFlag = generic
- ZGPSwitch = kinetic switch
  - ZLLTemperature = temperature sensor
- ZLLSwitch = dimmer switch
  - CLIPGenericStatus = scene selection
- ZLLPresence = motion detector
  - ZLLLightLevel = light sensor
  - CLIPGenericStatus = scene selection
  - ZLLTemperature = temperature sensor

'''


# Button state values
buttonstates = {
  1001 : 'Power on button pressed',
  1002 : 'Power on button depressed',
  2001 : 'Dimmer up button pressed',
  2002 : 'Dimmer up button depressed',
  3001 : 'Dimmer down button pressed',
  3002 : 'Dimmer down button depressed',
  4001 : 'Power off button pressed',
  4002 : 'Power off button depressed',
    34 : 'Kinetic button 1 (off) pressed',
    16 : 'Kinetic button 2 (scene 1) pressed',
    17 : 'Kinetic button 3 (scene 2) pressed',
    18 : 'Kinetic button 4 (scene 3) pressed' 
}


#####################


'''
# Print sensor names
print "All sensors:"
for i, s in enumerate(b.sensors):
  if i==0:
    pprint(dir(s)) 
  # print s.sensor_id, ":", s.name, " = ", s.type
  # pprint(s.state)
print
'''


#####################


# Print sensor names
print "Button sensors:"
for i, s in enumerate(b.sensors):
  if s.type == 'ZLLSwitch':
    s2 = b.sensors[i+1]
    print s.sensor_id, ":", s.name, "-", buttonstates[s.state['buttonevent']], "/ scene selected =", s2.state['status']
  if s.type == 'ZGPSwitch':
    s2 = b.sensors[i+1]
    print s.sensor_id, ":", s.name, "-", buttonstates[s.state['buttonevent']] # , "scene selected =", s.state['status']
    # pprint(s2.state)
  # print s.sensor_id, ":", s.name
  # pprint(s.state)
print




