import sys
from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4 import QtCore
import PyQt4.Qwt5 as Qwt
import serial
from PyQt4.Qwt5.anynumpy import *
import random
import thread
import threading
import bluetooth
import time

class mainPlot(Qt.QWidget):
	def __init__(self, *args):
		
		prsPenColors=[Qt.Qt.red,Qt.Qt.green,Qt.Qt.red,Qt.Qt.red,Qt.Qt.red]
		acsPenColors=[Qt.Qt.red,Qt.Qt.green,Qt.Qt.blue,Qt.Qt.cyan,Qt.Qt.red]
		Qt.QWidget.__init__(self, *args)
		#Initialize bluetooth comm
		#self.socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		print "Initialising connection..."
		#self.socket.connect(("00:19:A4:02:44:88", 1))
		print "Done."
		print "Commencing transfer..."
		#self.socket.send("3")
		#self.socketfile=self.socket.makefile('rw',0)
		self.lockbt=0
		self.socketfile=serial.Serial("/dev/ttyUSB0",9600, timeout=1)		
		self.QUAD=Sensor(self.socketfile,self.lockbt)
		

		#self.layout=Qt.QGridLayout(self)
		self.hbox = QtGui.QHBoxLayout(self)
		#Pressure graph
		self.prsPlot=Qwt.QwtPlot(self)
		self.prsPlot.setTitle('Pitch and Roll')
		self.prsPlot.setCanvasBackground(Qt.Qt.white)
		self.prsPlot.plotLayout().setCanvasMargin(0)
		self.prsPlot.plotLayout().setAlignCanvasToScales(True)
		
		#set all legends	
		self.prsPlot.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend);
		
		self.curveP1 = Qwt.QwtPlotCurve("pitch")
		self.curveP1.attach(self.prsPlot)
		self.curveP2 = Qwt.QwtPlotCurve("roll")
		self.curveP2.attach(self.prsPlot)
		self.curveP3 = Qwt.QwtPlotCurve("P3")
		self.curveP3.attach(self.prsPlot)
		self.curveP4 = Qwt.QwtPlotCurve("P4")
		self.curveP4.attach(self.prsPlot)
		self.curveP5 = Qwt.QwtPlotCurve("P5")
		self.curveP5.attach(self.prsPlot)
		
		self.curveP1.setPen(Qt.QPen(prsPenColors[0]))
		self.curveP2.setPen(Qt.QPen(prsPenColors[1]))
		self.curveP3.setPen(Qt.QPen(prsPenColors[2]))
		self.curveP4.setPen(Qt.QPen(prsPenColors[3]))
		self.curveP5.setPen(Qt.QPen(prsPenColors[4]))
		
		self.x = arange(0.0, 100.1, 0.5)
		self.pitch = zeros(len(self.x), Float)
		self.roll = zeros(len(self.x), Float)
		self.curveP1.setData(self.x, self.pitch)
		
		#Acceleration
		self.acsPlot=Qwt.QwtPlot(self)
		self.acsPlot.setTitle('Acceleration Sensor')
		self.acsPlot.setCanvasBackground(Qt.Qt.white)
		self.acsPlot.plotLayout().setCanvasMargin(0)
		self.acsPlot.plotLayout().setAlignCanvasToScales(True)
		#self.layout.addWidget( self.acsPlot, 1, 0)
		self.acsPlot.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend);		
		
		self.curveA1 = Qwt.QwtPlotCurve("az")
		self.curveA1.attach(self.acsPlot)
		self.curveA2 = Qwt.QwtPlotCurve("ay")
		self.curveA2.attach(self.acsPlot)
		self.curveA3 = Qwt.QwtPlotCurve("yaw")
		self.curveA3.attach(self.acsPlot)
		self.curveA4 = Qwt.QwtPlotCurve("ax")
		self.curveA4.attach(self.acsPlot)
		self.curveA5 = Qwt.QwtPlotCurve("A5")
		self.curveA5.attach(self.acsPlot)
			
		self.az = zeros(len(self.x), Float)
		self.curveA1.setData(self.x, self.az)
		self.ay= zeros(len(self.x), Float)
		self.curveA2.setData(self.x, self.ay)
		self.yaw= zeros(len(self.x), Float)
		self.curveA3.setData(self.x, self.yaw)
		self.ax= zeros(len(self.x), Float)
		self.curveA4.setData(self.x, self.ax)
				
				
		self.curveA1.setPen(Qt.QPen(acsPenColors[0]))
		self.curveA2.setPen(Qt.QPen(acsPenColors[1]))
		self.curveA3.setPen(Qt.QPen(acsPenColors[2]))
		self.curveA4.setPen(Qt.QPen(acsPenColors[3]))
		self.curveA5.setPen(Qt.QPen(acsPenColors[4]))
		
		
		
		
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
		#Add some basic gui components
		
		self.exitButton=QtGui.QPushButton(self.prsFrame)
		self.exitButton.setText("Exit")
		psld = QtGui.QSlider(QtCore.Qt.Horizontal,self.prsFrame)
		psld.setGeometry(30, 40, 100, 30)
		isld = QtGui.QSlider(QtCore.Qt.Horizontal,self.prsFrame)
		isld.setGeometry(30, 60, 100, 30)
		dsld = QtGui.QSlider(QtCore.Qt.Horizontal,self.prsFrame)
		dsld.setGeometry(30, 80, 100, 30)

		psld.setMinimum(0)
		psld.setMaximum(100)
		psld.valueChanged[int].connect(self.changePConst)

		dsld.setMinimum(0)
		dsld.setMaximum(100)
		dsld.valueChanged[int].connect(self.changeDConst)

		isld.setMinimum(0)
		isld.setMaximum(100)
		isld.valueChanged[int].connect(self.changeIConst)

		
		self.setLayout(self.hbox)
		self.prsPlot.replot()
		self.acsPlot.replot()    

		self.acc =[0,0,0]
		self.gyr =[0,0,0]
		self.tiltcomp = 0
		#Kalman filter
		self.Kp = 0.0
		self.Ki = 0.0
		self.Kd = 0.0

		#Controllers
		self.pitchcntrl = pid(self.Kp,self.Ki,self.Kd,1,self.acc,self.gyr)
		self.rollcntrl = pid(self.Kp,self.Ki,self.Kd,0,self.acc,self.gyr)
		
		#setup motors
		self.fmotor=Motor(self.socketfile,"front")	
		self.bmotor=Motor(self.socketfile,"back")	
		self.lmotor=Motor(self.socketfile,"left")
		self.rmotor=Motor(self.socketfile,"right")		
		#self.fmotor.setSpeed(60)
		
		#Connection
		self.connect(self.exitButton, Qt.SIGNAL("clicked()"), self.exitPlot)
		self.startTimer(10)
	def updateMotor(self):
 		self.tiltcomp = self.pitchcntrl.updatepid()
		self.fmotor.speed=(self.fmotor.thrust-self.tiltcomp-self.fmotor.yaw)
		if self.fmotor.speed<self.fmotor.minspeed:
			self.fmotor.speed = self.fmotor.minspeed
		self.fmotor.decodeAndSend(self.fmotor.speed)
		self.bmotor.speed=(self.bmotor.thrust+self.tiltcomp-self.bmotor.yaw)
		if self.bmotor.speed<self.bmotor.minspeed:
			self.bmotor.speed = self.bmotor.minspeed
		self.bmotor.decodeAndSend(self.bmotor.speed)
		
		self.tiltcomp = self.rollcntrl.updatepid()
		self.lmotor.speed=(self.lmotor.thrust+self.tiltcomp-self.lmotor.yaw)
		if self.lmotor.speed<self.lmotor.minspeed:
			self.lmotor.speed = self.lmotor.minspeed
		self.lmotor.decodeAndSend(self.lmotor.speed)
		self.rmotor.speed=(self.rmotor.thrust-self.tiltcomp-self.rmotor.yaw)
		if self.rmotor.speed<self.rmotor.minspeed:
			self.rmotor.speed = self.rmotor.minspeed
		self.rmotor.decodeAndSend(self.rmotor.speed)
		#print self.bmotor.speed,self.fmotor.speed


	def changePConst(self,value):
		self.pitchcntrl.p=value/300.0
		print self.pitchcntrl.p
	def changeIConst(self,value):
		self.pitchcntrl.i=value/50.0
		print self.pitchcntrl.i
	def changeDConst(self,value):
		self.pitchcntrl.d=value/100.0
		print self.pitchcntrl.d

 
	def exitPlot(self):
		self.QUAD.kill=0
		self.close()
	def alignScales(self):
		self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
		self.canvas().setLineWidth(1)
		for i in range(Qwt.QwtPlot.axisCnt):
			scaleWidget = self.axisWidget(i)
			if scaleWidget:
				scaleWidget.setMargin(0)
			scaleDraw = self.axisScaleDraw(i)
			if scaleDraw:
				scaleDraw.enableComponent(Qwt.QwtAbstractScaleDraw.axbone, False)

	def timerEvent(self, e):	
		self.pitch = concatenate((self.pitch[:1], self.pitch[:-1]), 1)
		self.pitch[0] =float(self.QUAD.pitch)
		self.roll = concatenate((self.roll[:1], self.roll[:-1]), 1)
		self.roll[0] =float(self.QUAD.roll)
		self.yaw = concatenate((self.yaw[:1], self.yaw[:-1]), 1)
		self.yaw[0] =float(self.QUAD.yaw)
		self.ax = concatenate((self.ax[:1], self.ax[:-1]), 1)
		self.ax[0] =float(self.QUAD.ax)
		self.ay = concatenate((self.ay[:1], self.ay[:-1]), 1)
		self.ay[0] =float(self.QUAD.ay)
		self.az = concatenate((self.az[:1], self.az[:-1]), 1)
		self.az[0] =float(self.QUAD.az)
		
		self.pitchcntrl.kalman.ac=self.QUAD.acc
		self.pitchcntrl.kalman.gy=self.QUAD.gyr
		self.rollcntrl.kalman.ac=self.QUAD.acc
		self.rollcntrl.kalman.gy=self.QUAD.gyr
		self.updateMotor()	

		#Set data		

		self.curveP1.setData(self.x, self.pitch)
		self.curveP2.setData(self.x, self.roll)
		self.curveA1.setData(self.x, self.az)
		self.curveA2.setData(self.x, self.ay)
		self.curveA3.setData(self.x, self.yaw)
		self.curveA4.setData(self.x, self.ax)
		self.prsPlot.replot()
		self.acsPlot.replot()
	


class basicSensor():
	def __init__(self, device):
		self.port = serial.Serial(device,9600, timeout=1)
	def readValue(self):
		value=self.port.readline()
		return value
	def close(self):
		self.port.close()
		
class Sensor(threading.Thread):
	def __init__(self,btfile,btlock):
		
		threading.Thread.__init__(self, None)
		#self.quad=basicSensor(self.sensor)
		self.kill=1	
		self.ax=0
		self.ay=0
		self.az=0
		self.acc=[0,0,0]
		self.gyr=[0,0,0]
		self.pitch=0
		self.roll=0
		self.yaw=0
		self.file=btfile
		self.lock=btlock	
		self.start()
	def run(self):
		while self.kill:		
			try:			
				
				self.readings=self.file.readline()
				
				#print self.readings
				self.decodeData()
				
				
			except:
				print "On a wait"
				continue
		self.file.close()
	def acqLock(self):
		self.lock=1
	def relLock(self):
		self.lock=1
	def decodeData(self):
		data=self.readings.replace("\n","").replace("\r","").split("#")
		self.roll=data[3]
		self.pitch=data[4]
		self.yaw=data[5]
		self.ax=data[0]
		self.ay=data[1]
		self.az=data[2]
		self.acc = [float(self.ax),float(self.ay),float(self.az)]
		self.gyr = [float(self.roll),float(self.pitch),float(self.yaw)]
		#print self.acc,self.gyr

class FlightAngle_KalmanFilter:  
	def __init__(self,axis,acc,gyr):
		self.ROLL = 0
		self.PITCH = 1
		self.YAW = 2
		self.ac = acc
		self.gy = gyr		
		self.angle=[0.0, 0.0, 0.0] 
		self.gyroAngle=[0.0, 0.0, 0.0]
		self.x_angle=[0.0,0.0,0.0] 
		self.x_bias=[0.0,0.0,0.0]  
		self.P_00=[1.0,1.0,1.0] 
		self.P_01=[0.0,0.0,0.0] 
		self.P_10=[0.0,0.0,0.0] 
		self.P_11=[1.0,1.0,1.0]
		self.Q_angle = 0.001  
		self.Q_gyro = 0.003  
		self.R_angle = 0.3
		self.x = time.time()		
		self.G_Dt=time.time() - self.x	
		self.axis = axis
	def calculatekalman(self):  
		self.x_angle[self.axis] += self.G_Dt * (self.gy[self.axis] - self.x_bias[self.axis])  
		self.P_00[self.axis] += -self.G_Dt * (self.P_10[self.axis] + self.P_01[self.axis]) + self.Q_angle * self.G_Dt  
		self.P_01[self.axis] += -self.G_Dt * self.P_11[self.axis]
		self.P_10[self.axis] += -self.G_Dt * self.P_11[self.axis]  
		self.P_11[self.axis] += +self.Q_gyro * self.G_Dt
		self.y = self.ac[self.axis] - self.x_angle[self.axis]  
		self.S = self.P_00[self.axis] + self.R_angle  
		self.K_0 = self.P_00[self.axis] / self.S  
		self.K_1 = self.P_10[self.axis] / self.S  
		self.x_angle[self.axis] += self.K_0 * self.y  
		self.x_bias[self.axis] += self.K_1 * self.y  
		self.P_00[self.axis] -= self.K_0 * self.P_00[self.axis]  
		self.P_01[self.axis] -= self.K_0 * self.P_01[self.axis]  
		self.P_10[self.axis] -= self.K_1 * self.P_00[self.axis]  
		self.P_11[self.axis] -= self.K_1 * self.P_01[self.axis]  
		self.G_Dt=time.time() - self.x 
		return self.x_angle[self.axis] 
	
class pid:  
	def __init__(self,Kp,Ki,Kd,axis,acc,gyr):  
		self.interror=0.0  
		self.preverror=0.0  
		self.differror=0.0  
		self.p=Kp 
		self.i=Ki  
		self.d=Kd  
		self.reqrdstate=0.0	
		self.axis=axis 
		self.acc = acc
		self.gyr = gyr
		self.kalman= FlightAngle_KalmanFilter(self.axis,self.acc,self.gyr) 
		self.kalman.calculatekalman()
 
	def updatepid(self):  
		
		self.curstate = self.kalman.calculatekalman()
		self.error=self.reqrdstate - self.curstate
		self.interror += self.error*self.kalman.G_Dt
		self.differror = (self.error-self.preverror)/self.kalman.G_Dt
		if self.interror>100:
			self.interror = 100
		elif	self.interror< -100:
			self.interror = -100	
		#self.prevstate = self.curstate
		self.result=self.p*self.error+self.i*self.interror-self.d*self.kalman.gy[self.axis]  
		self.preverror = self.error
		self.kalman.x = time.time()				
		return (self.result)
  	def setpid(self, a, b, c):  
		self.p=a  
		self.i=b  
		self.d=c  

class Motor:

	def __init__(self,btfile,location):
		self.file=btfile
		self.location=location
		self.tiltcomp = 0
		self.minspeed = 65
		self.speed = 65	
		self.thrust = 65
		self.yaw = 0 
	def setSpeed(self,speed):
		self.decodeAndSend(speed)
	def stop(self):
		self.decodeAndSend(0)
	def setHeight(self):
		self.decodeAndSend(self.thrust)	
	def decodeAndSend(self,data):
		string=""	
 		if self.location=='front':
			string='#'
		if self.location=='back':
			string='$'
		if self.location=='left':
			string='%'
		if self.location=='right':
			string='&'
		string=string+chr(int(data))+"."
		#print string
		for i in range(3):
			self.file.writelines(string)
		
						
		
app = Qt.QApplication(sys.argv)
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

demo = mainPlot()
demo.resize(1000, 700)
demo.show()
sys.exit(app.exec_())


    
    
    
