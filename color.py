import serial
import time
port = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
while 1:
	try:	
		line=port.readline()
		line=line.replace("\r","").replace("\n","")
		s=line.split(" ")
		print s

	except KeyboardInterrupt:
		break
port.close()
