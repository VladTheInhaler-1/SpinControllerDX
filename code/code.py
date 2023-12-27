#
#	POC Spin Controller
#	v 0.3
#	Author: Evan Scheel - VladTheInhaler-1
#


#import board libaries 
import board
import digitalio
import rotaryio
import usb_hid
from adafruit_hid.mouse import Mouse
from time import sleep

#gamepad libary, obects, and 
from hid_gamepad import Gamepad

gpad = Gamepad(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

#list out board pins and set encoder zero
button0 = digitalio.DigitalInOut(board.GP20)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.UP

button1 = digitalio.DigitalInOut(board.GP16)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP27, board.GP26,1)


b0 = False
b1 = False 

last_position = 0
knob_pos = 0
      
while True:
    position = encoder.position
    if last_position is None or position < last_position:
        #print('left')
        mouse.move(-10,0)
    if last_position is None or position > last_position:
        #print('right')
        mouse.move(10,0)
    last_position = position
    
    
    if not button0.value:
        if not b0:  # Check if button0 was previously released
            mouse.press(Mouse.LEFT_BUTTON)
            b0 = True
    else:
        if b0:  # Check if button0 was previously pressed
            mouse.release(Mouse.LEFT_BUTTON)
            b0 = False
    
    if not button1.value:
        if not b1:  # Check if button1 was previously released
            mouse.press(Mouse.RIGHT_BUTTON)
            b1 = True
    else:
        if b1:  # Check if button1 was previously pressed
            mouse.release(Mouse.RIGHT_BUTTON)
            b1 = False
    sleep(0.01)

