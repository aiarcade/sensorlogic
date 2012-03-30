import serial

port = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
while 1:
	try:	
		line=port.readline()
		print line	
	except KeyboardInterrupt:
		break
port.close()
