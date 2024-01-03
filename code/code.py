#
#	POC Spin Controller
#	v 0.4
#	Author: Evan Scheel - VladTheInhaler-1
#

import time
import board
import digitalio 
import analogio

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

######### SETTINGS ############

voltage = 3.3 
deadzone = .04 
deviceName = 'VladCraft SpinCon'

###############################

knob0 = analogio.AnalogIn(board.D4)


button1 = digitalio.DigitalInOut(board.D6)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.D7)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP


hid = HIDService()
kb = Keyboard(hid.devices)


advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = deviceName

ble = adafruit_ble.BLERadio()
ble.name = deviceName

#ble.tx_power = 20 ## Not currently Implemented with CP 8.2.9


def connectBLE():
    print('Advertising')
    ble.start_advertising(advertisement,scan_response)

def get_pos(pin):
    val = pin.value * voltage / 65536
    return(round(val,2))

def rotation():
    global last_pos
    position = get_pos(knob0)
    if position > last_pos + deadzone:
        last_pos = position
        kb.send(Keycode.DOWN_ARROW)
        print('Moved Right')
    elif position < last_pos - deadzone:
        last_pos = position
        kb.send(Keycode.UP_ARROW)
        print('Moved Left')
    else:
        pass

def buttons():
    global b1, b2
    if not button1.value:
        if not b1:  # Check if button was previously released
            kb.press(Keycode.ENTER)
            print('B pressed')
            b1 = True
    else:
        if b1:  # Check if button was previously pressed
            kb.release(Keycode.ENTER)
            print('B released')
            b1 = False
                
    if not button2.value:
        if not b2:
            kb.press(Keycode.BACKSPACE)
            print('N pressed')
            b2 = True
    else:
        if b2:
            kb.release(Keycode.BACKSPACE)
            print('N released')
            b2 = False
            
last_pos = get_pos(knob0)
b1 = False
b2 = False

if not ble.connected:
    connectBLE()
    
while True:
    while not ble.connected:
        pass
    
    print('Connected')

    while ble.connected:
        rotation() # handles knob inputs
        buttons() # handles button states
        
        
        time.sleep(0.03)
    
    # If script gets here, you lost connection. Attempts to reconnect
    print('Connection Lost')
    connectBLE()


