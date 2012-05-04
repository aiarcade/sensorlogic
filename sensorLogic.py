import sys
from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4 import QtCore
import PyQt4.Qwt5 as Qwt
import serial
from PyQt4.Qwt5.anynumpy import *
import random
import time
import thread
import threading
import sys
import math

class Logger():
	def __init__(self,channel):
		return
	def log(self,mesg):
		print mesg

class kalmanFilter():
	def __init__(self,q,r,p,initial_value):
		self.q=q
		self.p=p
		self.r=r
		self.x=initial_value
	def addSample(self,measurement):
		self.p=self.p+self.q
		self.k=self.p/(self.p+self.r)
		self.x= self.x + self.k*(measurement-self.x)
		self.p=(1-self.k)*self.p
		return self.x
class Recorder():
	def __init__(self,filename):
		self.filename=filename
		self.recorder=open(filename,"w")
	def record(self,data):
		self.recorder.writelines(data)
	def close(self):
		self.recorder.close()
		
		


class mainPlot(Qt.QWidget):
	def __init__(self, *args):

	
		#create a logger to handle logs
		
		self.uiLogger=Logger(sys.stdout)
		self.ACSrecorder=Recorder("acc"+str(time.time())+".csv")
		self.PRSrecorder=Recorder("prs"+str(time.time())+".csv")
		# Initialize sensors #Detect and Attach all sensors
		print "Connecting to sensors"
		self.sensor1=Sensor("/dev/ttyUSB0",1,self.uiLogger)
		self.sensor2=Sensor("/dev/ttyUSB1",1,self.uiLogger)
		
		time.sleep(1)
		
		#setup kalaman filters for accelerometers
		self.A1filter=kalmanFilter(0.4, 256, 100, 0)
		self.A2filter=kalmanFilter(0.4, 256, 100, 0)
		self.A3filter=kalmanFilter(0.4, 256, 100, 0)
		self.A4filter=kalmanFilter(0.4, 256, 100, 0)
		self.A5filter=kalmanFilter(0.4, 256, 100, 0)

		self.acsdata=[]
		self.prsdata=[]
		self.displacement=[0.0,0.0,0.0,0.0,0.0]
		
		self.acsError=[0,0,0,0,0]
		self.prsError=[0,0,0,0,0]
		self.acsCalibrate=0	
		self.prsCalibrate=0	
		self.timeInterval=10
		self.recordCounter=0
		self.record=0
		

		prsPenColors=[Qt.Qt.red,Qt.Qt.green,Qt.Qt.black,Qt.Qt.cyan,Qt.Qt.blue]
		acsPenColors=[Qt.Qt.red,Qt.Qt.green,Qt.Qt.black,Qt.Qt.cyan,Qt.Qt.blue]
		Qt.QWidget.__init__(self, *args)
		#self.layout=Qt.QGridLayout(self)
		self.hbox = QtGui.QHBoxLayout(self)
		#Pressure graph
		self.prsPlot=Qwt.QwtPlot(self)
		self.prsPlot.setTitle('Pressure Sensor')
		self.prsPlot.setCanvasBackground(Qt.Qt.white)
		self.prsPlot.plotLayout().setCanvasMargin(0)
		self.prsPlot.plotLayout().setAlignCanvasToScales(True)
		#self.layout.addWidget( self.prsPlot, 0, 0)
		
		self.curveP1 = Qwt.QwtPlotCurve("5")
		self.curveP1.attach(self.prsPlot)
		self.curveP2 = Qwt.QwtPlotCurve("4")
		self.curveP2.attach(self.prsPlot)
		self.curveP3 = Qwt.QwtPlotCurve("3")
		self.curveP3.attach(self.prsPlot)
		self.curveP4 = Qwt.QwtPlotCurve("2")
		self.curveP4.attach(self.prsPlot)
		self.curveP5 = Qwt.QwtPlotCurve("1")
		self.curveP5.attach(self.prsPlot)
		
		self.curveP1.setPen(Qt.QPen(prsPenColors[0]))
		self.curveP2.setPen(Qt.QPen(prsPenColors[1]))
		self.curveP3.setPen(Qt.QPen(prsPenColors[2]))
		self.curveP4.setPen(Qt.QPen(prsPenColors[3]))
		self.curveP5.setPen(Qt.QPen(prsPenColors[4]))
		
		self.px = arange(0.0, 100.1, 0.5)
		self.p1 = zeros(len(self.px), Float)
		self.curveP1.setData(self.px, self.p1)
		self.p2 = zeros(len(self.px), Float)
		self.curveP2.setData(self.px, self.p2)
		self.p3 = zeros(len(self.px), Float)
		self.curveP3.setData(self.px, self.p3)
		self.p4 = zeros(len(self.px), Float)
		self.curveP4.setData(self.px, self.p4)
		self.p5 = zeros(len(self.px), Float)
		self.curveP5.setData(self.px, self.p5)			

		#Acceleration
		self.acsPlot=Qwt.QwtPlot(self)
		self.acsPlot.setTitle('Acceleration Sensor')
		self.acsPlot.setCanvasBackground(Qt.Qt.white)
		self.acsPlot.plotLayout().setCanvasMargin(0)
		self.acsPlot.plotLayout().setAlignCanvasToScales(True)
		#self.layout.addWidget( self.acsPlot, 1, 0)
		
		self.curveA1 = Qwt.QwtPlotCurve("4")
		self.curveA1.attach(self.acsPlot)
		self.curveA2 = Qwt.QwtPlotCurve("3")
		self.curveA2.attach(self.acsPlot)
		self.curveA3 = Qwt.QwtPlotCurve("1")
		self.curveA3.attach(self.acsPlot)
		self.curveA4 = Qwt.QwtPlotCurve("2")
		self.curveA4.attach(self.acsPlot)
		self.curveA5 = Qwt.QwtPlotCurve("#")
		self.curveA5.attach(self.acsPlot)
		
		self.curveA1.setPen(Qt.QPen(acsPenColors[0]))
		self.curveA2.setPen(Qt.QPen(acsPenColors[1]))
		self.curveA3.setPen(Qt.QPen(acsPenColors[2]))
		self.curveA4.setPen(Qt.QPen(acsPenColors[3]))
		self.curveA5.setPen(Qt.QPen(acsPenColors[4]))
		
		self.prsPlot.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)
		self.acsPlot.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)		
		self.ax = arange(0.0, 100.1, 0.5)
		self.a1 = zeros(len(self.ax), Float)
		self.curveA1.setData(self.ax, self.a1)
		self.a2 = zeros(len(self.ax), Float)
		self.curveA2.setData(self.ax, self.a2)
		self.a3 = zeros(len(self.ax), Float)
		self.curveA3.setData(self.ax, self.a3)
		self.a4 = zeros(len(self.ax), Float)
		self.curveA4.setData(self.ax, self.a4)
		self.a5 = zeros(len(self.ax), Float)
		self.curveA5.setData(self.ax, self.a5)

		self.prsFrame=QtGui.QFrame(self)
		self.prsFrame.setFrameShape(QtGui.QFrame.StyledPanel)

		self.acsFrame=QtGui.QFrame(self)
		self.acsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		
		self.prsSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.prsSplitter.addWidget(self.prsPlot)
		self.prsSplitter.addWidget(self.prsFrame)
		self.acsSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.acsSplitter.addWidget(self.acsPlot)
		self.acsSplitter.addWidget(self.acsFrame)
		
		self.Splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.Splitter.addWidget(self.acsSplitter)
		self.Splitter.addWidget(self.prsSplitter)
		self.hbox.addWidget(self.Splitter)

		#add some button for calibration
		self.A1calbutton= QtGui.QPushButton(self.acsFrame)
		self.A1calbutton.setText("Calibrate ACS")
		self.A1calbutton.setGeometry(30, 40, 100, 30)
		self.connect(self.A1calbutton, Qt.SIGNAL("clicked()"), self.calibrateACS)
		
		self.Recbutton= QtGui.QPushButton(self.acsFrame)
		self.Recbutton.setGeometry(150, 40, 100, 30)
		self.Recbutton.setText("Start Record")
		self.connect(self.Recbutton, Qt.SIGNAL("clicked()"), self.startRecord)

		self.startTimer(self.timeInterval)
		self.setLayout(self.hbox)
		self.prsPlot.replot()
		self.acsPlot.replot()

	def calibrateACS(self):
		self.acsCalibrate=1
	def startRecord(self):
		self.record=not self.record
		if self.record==0:
			self.Recbutton.setText("Start Record")
			self.recordCounter=0
		else:
			self.Recbutton.setText("Stop Record")


	def timerEvent(self, e):
		
		
		
		
		if self.sensor1.type=='ACS' and self.sensor1.STATUS=='OK' :
			self.acsdata=self.processACSdata(self.sensor1.data)
		elif self.sensor2.type=='ACS'and self.sensor2.STATUS=='OK' :
			self.acsdata=self.processACSdata(self.sensor2.data)
		if self.sensor1.type=='PRS' and self.sensor1.STATUS=='OK':
			self.prsdata=self.processPRSdata(self.sensor1.data)
		elif self.sensor2.type=='PRS' and self.sensor2.STATUS=='OK':
			self.prsdata=self.processPRSdata(self.sensor2.data)
		
	
		#print acsdata
		

		#update array and replot 		
		if 	len(self.acsdata)>0:
			
			self.a1 = concatenate((self.a1[:1], self.a1[:-1]), 1)
			self.a1[0] =self.acsdata[0]
			self.curveA1.setData(self.ax, self.a1)
		
			self.a2 = concatenate((self.a2[:1], self.a2[:-1]), 1)
			self.a2[0] =self.acsdata[1]
			self.curveA2.setData(self.ax, self.a2)

			self.a3 = concatenate((self.a3[:1], self.a3[:-1]), 1)
			self.a3[0] =self.acsdata[2]
			self.curveA3.setData(self.ax, self.a3)

			self.a4 = concatenate((self.a4[:1], self.a4[:-1]), 1)
			self.a4[0] =self.acsdata[3]
			self.curveA4.setData(self.ax, self.a4)
	
			self.a5 = concatenate((self.a5[:1], self.a5[:-1]), 1)
			self.a5[0] =self.acsdata[4]
			self.curveA5.setData(self.ax, self.a5)
			self.acsPlot.replot()
		if 	len(self.prsdata)>0:	
			self.p1 = concatenate((self.p1[:1], self.p1[:-1]), 1)
			self.p1[0] =self.prsdata[0]
			self.curveP1.setData(self.px, self.p1)
		
			self.p2 = concatenate((self.p2[:1], self.p2[:-1]), 1)
			self.p2[0] =self.prsdata[1]
			self.curveP2.setData(self.px, self.p2)

			self.p3 = concatenate((self.p3[:1], self.p3[:-1]), 1)
			self.p3[0] =self.prsdata[2]
			self.curveP3.setData(self.px, self.p3)

			self.p4 = concatenate((self.p4[:1], self.p4[:-1]), 1)
			self.p4[0] =self.prsdata[3]
			self.curveP4.setData(self.px, self.p4)
	
			self.p5 = concatenate((self.p5[:1], self.p5[:-1]), 1)
			self.p5[0] =self.prsdata[4]
			self.curveP5.setData(self.px, self.p5)
			self.prsPlot.replot()
		if self.record==1:	
			self.ACSrecorder.record(str(self.recordCounter)+","+str(self.a1[0])+","+str(self.a2[0])+","+str(self.a3[0])+","+str(self.a4[0])+","+str(self.a5[0])+"\n")
			self.PRSrecorder.record(str(self.recordCounter)+","+str(self.p1[0])+","+str(self.p2[0])+","+str(self.p3[0])+","+str(self.p4[0])+","+str(self.p5[0])+"\n")
			self.recordCounter=self.recordCounter+1
		if self.recordCounter>10000000:
			self.recordCounter=0
		

		
		return

	def calculateDisp(self,prevAcc,currAcc):
		time=self.timeInterval/1000.0
		print time
		disp=(prevAcc*(time)**2)/2+.25*(currAcc-prevAcc)*(time)**2
		return disp*1000.0

	def closeEvent(self, event):
		self.sensor1.exitMe=0
		self.sensor2.exitMe=0
		self.ACSrecorder.close()
		
		#event.accept()   
	def processACSdata(self,data):
		
		filterout=[]
		
		#data=[int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5])]
		#print data
		#print self.acsError
		#data=[data[1]-self.acsError[0],data[2]-self.acsError[1],data[3]-self.acsError[2],data[4]-self.acsError[3],data[5]-self.acsError[4]]
		try:
			a1=data[1]
			a1=self.calculateG(a1)
			a1=self.A1filter.addSample(a1)
			#filterout.append(a1)
		
			a2=data[2]
			a2=self.calculateG(a2)
			a2=self.A2filter.addSample(a2)
			#filterout.append(a2)
		
			a3=data[3]
			a3=self.calculateG(a3)
			a3=self.A3filter.addSample(a3)
			#filterout.append(a3)
		
			a4=data[4]
			a4=self.calculateG(a4)
			a4=self.A4filter.addSample(a4)
			#filterout.append(a4)
		
			a5=data[5]
			a5=self.calculateG(a5)
			a5=self.A5filter.addSample(a5)
			#filterout.append(a5)
			if self.acsCalibrate==1:
				self.acsError=[a1,a2,a3,a4,a5]
				self.acsCalibrate=0
				self.ACSrecorder.record("Calibrating ..........")
			filterout=[a1-self.acsError[0],a2-self.acsError[1],a3-self.acsError[2],a4-self.acsError[3],a5-self.acsError[4]]


		except:
				sys.exc_info()[0]
				self.uiLogger.log("WRN:process_acs_data:empty data array")
				filterout=[0,0,0,0,0]	
		
		return filterout
		
	def processPRSdata(self,data):
		#print data
		dataout=[float(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5])]
		#print dataout
		return dataout


	def calculateAngles(self,data):
		angles=[]
		for i in data[1:]:
			angles.append(self.calculateAngle(float(i)))
		return angles
			
	def calculateAngle(self,volt):
		
		angle=0
		volt=(volt-1.35)/0.44
		try:		
			angle=math.asin(volt)
		#angle=angle*180/3.14
		except:
			angle=0
		return angle
		

		
		
	def calculateG(self,adcvalue):
		voltage=interp(float(adcvalue),[0,1023],[0,5])
		volt=voltage-1.35
		g=(volt*1000)/800
		gcorrected=round(g,3)
		return gcorrected*9.8



		
	
		
		 


class basicSensor():
	def __init__(self, device,logger):
		self.device=device
		self.port="NODEVICE"
		self.Logger=logger
		try:
			self.port = serial.Serial(self.device,9600, timeout=1)
			
		except:
			self.port="NODEVICE"
			self.Logger.log("CRT:basic_sensor_construct:Unable to open device "+	self.device)
	def reconnect(self):
		if self.port=='NODEVICE' :
			try:
				self.port = serial.Serial(self.device,9600, timeout=1)
			except:
				#print "Unable to opendevice on retry"+	self.device
				self.port="NODEVICE"		
	def readValue(self):
		if self.port !='NODEVICE':
			try:
				value=self.port.readline()
				return value
			except:
				value=-9888
				self.Logger.log("CRT:basic_sensor_readvalue:Unable to read from "+	self.device)
				return value
				
		
	def close(self):
		#print "Trying to close"+str(self.port)
		if self.port!='NODEVICE':
			try:
				self.Logger.log("MSG:basic_sensor_close:Closing device "+self.device)
				self.port.close()
			except:
				self.Logger.log("CRT:basic_sensor_close:Unable to close "+	self.device)
		else:
			self.Logger.log("CRT:basic_sensor_close:Not opened "+	self.device)
		
		
class Sensor(threading.Thread):
	def __init__(self,sensor,retry,logger):
	 	threading.Thread.__init__(self, None)
		self.Logger=logger
		self.retry=retry
		self.exitMe=1
		self.type='NONE'
		self.STATUS='NONE'
		self.data=[]
		self.sensor=basicSensor(sensor,self.Logger)
		self.start()
	def run(self):
		while(self.exitMe):
			#print self.sensor.port
			if self.sensor.port!='NODEVICE':
					data=self.sensor.readValue()
					if data==-9888:
						self.STATUS="READERROR"
					else:
						data=data.replace("\n","").replace("\r","")
						self.data=data[:-1].split("#")
						if self.data[0]=='ACS':
							self.type='ACS'
						elif self.data[0]=='PRS':
							self.type='PRS'
							
						self.STATUS="OK"
												
						
						
			else:
				if self.retry==1:
					self.sensor.reconnect()
			if self.sensor.port=='NODEVICE':
					self.STATUS="ERROR"
			#break
									
		self.sensor.close()


        
app = Qt.QApplication(sys.argv)
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
demo = mainPlot()
demo.resize(1000, 700)
demo.show()
sys.exit(app.exec_())

    
    
    
