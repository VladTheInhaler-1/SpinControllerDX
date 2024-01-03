#SpinControllerDX

A DIY open-source gamepad for rhythm games.

Developed with CircuitPython

https://www.youtube.com/shorts/g_zpPSL3rEk


Code Updates:

v0.4:
- Changed board to Seed Xiao nRF52840
- Implemented Bluetooth Connection
- Replaced Bourns encoder with AS5600 Magnetic position sensor
- Sensor voltage mapped to read the direction of rotation and send keypress
- HID keyboard input


The current iteration uses an AS5600 magnetic encoder sending voltage to an analog pin on a Seeed Xiao nRF52840. 
