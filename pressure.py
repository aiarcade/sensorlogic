import serial

port = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
while 1:
	try:	
		line=port.readline()
		voltage=0
		line=line.replace("\n","")
		try:		
			data=float(line)
			voltage=((5.0/1023.0)*data)-2.5
			print voltage*1000,line
		except:
			print "Unknown value"
		
	except KeyboardInterrupt:
		break
port.close()
