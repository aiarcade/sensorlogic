from numpy import interp
import serial

port = serial.Serial('/dev/ttyUSB1',9600, timeout=1)
data=0
while 1:
	try:	
		line=port.readline()
		line=line.replace("\n","")
		print "D"+line
		try:		
			data=float(line)
			if data>280:
				print "high"
			volt=interp(data,[0,1023],[0,5])
			#print "Voltage"+str(volt)
			volt=volt-1.35
			g=(volt*1000)/800
			print round(g,3)
			
		except:
			print "Unknown value"
		
	except KeyboardInterrupt:
		break
port.close()
