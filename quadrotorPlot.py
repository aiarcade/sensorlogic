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

class mainPlot(Qt.QWidget):
	def __init__(self, *args):
		
		prsPenColors=[Qt.Qt.red,Qt.Qt.green,Qt.Qt.red,Qt.Qt.red,Qt.Qt.red]
		acsPenColors=[Qt.Qt.red,Qt.Qt.green,Qt.Qt.blue,Qt.Qt.cyan,Qt.Qt.red]
		Qt.QWidget.__init__(self, *args)
		#Sensor
		self.QUAD=Sensor("/dev/ttyUSB0")
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
		
		self.curveA1 = Qwt.QwtPlotCurve("right")
		self.curveA1.attach(self.acsPlot)
		self.curveA2 = Qwt.QwtPlotCurve("left")
		self.curveA2.attach(self.acsPlot)
		self.curveA3 = Qwt.QwtPlotCurve("front")
		self.curveA3.attach(self.acsPlot)
		self.curveA4 = Qwt.QwtPlotCurve("back")
		self.curveA4.attach(self.acsPlot)
		self.curveA5 = Qwt.QwtPlotCurve("A5")
		self.curveA5.attach(self.acsPlot)
			
		self.right = zeros(len(self.x), Float)
		self.curveA1.setData(self.x, self.right)
		self.left= zeros(len(self.x), Float)
		self.curveA2.setData(self.x, self.left)
		self.front= zeros(len(self.x), Float)
		self.curveA3.setData(self.x, self.front)
		self.back= zeros(len(self.x), Float)
		self.curveA4.setData(self.x, self.back)
				
				
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
		self.exitButton=QtGui.QPushButton(self.prsFrame)
		self.exitButton.setText("Exit")
		self.setLayout(self.hbox)
		self.prsPlot.replot()
		self.acsPlot.replot()      

		#Connection
		self.connect(self.exitButton, Qt.SIGNAL("clicked()"), self.exitPlot)
		self.startTimer(30)
 
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
				scaleDraw.enableComponent(Qwt.QwtAbstractScaleDraw.Backbone, False)

	def timerEvent(self, e):	
		self.pitch = concatenate((self.pitch[:1], self.pitch[:-1]), 1)
		self.pitch[0] =float(self.QUAD.pitch)
		self.roll = concatenate((self.roll[:1], self.roll[:-1]), 1)
		self.roll[0] =float(self.QUAD.roll)
		self.front = concatenate((self.front[:1], self.front[:-1]), 1)
		self.front[0] =float(self.QUAD.front)
		self.back = concatenate((self.back[:1], self.back[:-1]), 1)
		self.back[0] =float(self.QUAD.back)
		self.left = concatenate((self.left[:1], self.left[:-1]), 1)
		self.left[0] =float(self.QUAD.left)
		self.right = concatenate((self.right[:1], self.right[:-1]), 1)
		self.right[0] =float(self.QUAD.right)
		#Set data		
		self.curveP1.setData(self.x, self.pitch)
		self.curveP2.setData(self.x, self.roll)
		self.curveA1.setData(self.x, self.front)
		self.curveA2.setData(self.x, self.back)
		self.curveA3.setData(self.x, self.left)
		self.curveA4.setData(self.x, self.right)
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
	def __init__(self,sensor):
		self.sensor=sensor
		threading.Thread.__init__(self, None)
		self.quad=basicSensor(self.sensor)
		self.kill=1
		self.right=0
		self.left=0
		self.front=0
		self.back=0
		self.pitch=0
		self.roll=0
		self.yaw=0
		self.start()
	def run(self):
		while self.kill:		
			try:			
				self.readings=self.quad.readValue()
				print self.readings
				self.decodeData()
			except:
				print "On a wait"
				continue
	def decodeData(self):
		data=self.readings.replace("\n","").replace("\r","").split("#")
		self.right=data[0]
		self.left=data[1]
		self.front=data[2]
		self.back=data[3]
		self.pitch=data[5]
		self.roll=data[4]
		print data
		

        
app = Qt.QApplication(sys.argv)
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

demo = mainPlot()
demo.resize(1000, 700)
demo.show()
sys.exit(app.exec_())


    
    
    
