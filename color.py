import serial

port = serial.Serial('/dev/ttyUSB0',4200, timeout=1)
while 1:
		line=port.readline()
port.close()
