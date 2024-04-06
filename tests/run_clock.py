#!/usr/bin/python

from datetime import datetime
from hackclock.runapp.Libs.Clock import Clock
from hackclock.runapp.Libs.SevenSegment import Display

# Set to bright between 6:30 AM and 7:45 PM
brightnessStart = (6, 30)
brightnessEnd = (19, 45)
# Brightness is a range from 0 to 15
brightnessValue = 10
dimnessValue = 0

# Connect to the internal machine clock
clock = Clock()
# Connect to the LED display
display = Display()

# Show the current time
def showCurrentTime():
  now = datetime.now()

  # Set the minutes
  display.setMinutes(now.minute)

  # Set the hours
  hour = now.hour % 12
  if hour == 0:
    hour = 12
  display.setHours(hour)

  # Set the indicator lights
  display.setColon(True)
  # Set the dot on the right digit for PM
  if (now.hour > 11):
    # Buffer row 4 is right digit
    x = display.display.getBufferRow(4)
    # 8th bit is for the dot
    display.display.setBufferRow(4, x | 1 << 7)
  # Set the brightness (0 to 15, 15 is the brightest)
  display.setBrightness(getBrightness(now))
      
# What to do when the internal clock ticks
clock.onTick(showCurrentTime)


def getBrightness(now):
  if beforeTime(now, brightnessStart) or afterTime(now, brightnessEnd):
    return dimnessValue
  return brightnessValue

def beforeTime(now, t):
  return now.hour < t[0] or (now.hour == t[0] and now.minute < t[1])

def afterTime(now, t):
  return now.hour > t[0] or (now.hour == t[0] and now.minute > t[1])
