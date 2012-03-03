import sys
from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4 import QtCore
import PyQt4.Qwt5 as Qwt
import serial
from PyQt4.Qwt5.anynumpy import *
import random

class mainPlot(Qt.QWidget):
	def __init__(self, *args):
		
		prsPenColors=[Qt.Qt.red,Qt.Qt.red,Qt.Qt.red,Qt.Qt.red,Qt.Qt.red]
		acsPenColors=[Qt.Qt.red,Qt.Qt.red,Qt.Qt.red,Qt.Qt.red,Qt.Qt.red]
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
		
		self.curveP1 = Qwt.QwtPlotCurve("P1")
		self.curveP1.attach(self.prsPlot)
		self.curveP2 = Qwt.QwtPlotCurve("P2")
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
		self.p1 = zeros(len(self.x), Float)
		self.curveP1.setData(self.x, self.p1)
		
		#Acceleration
		self.acsPlot=Qwt.QwtPlot(self)
		self.acsPlot.setTitle('Acceleration Sensor')
		self.acsPlot.setCanvasBackground(Qt.Qt.white)
		self.acsPlot.plotLayout().setCanvasMargin(0)
		self.acsPlot.plotLayout().setAlignCanvasToScales(True)
		#self.layout.addWidget( self.acsPlot, 1, 0)
		
		self.curveA1 = Qwt.QwtPlotCurve("P1")
		self.curveA1.attach(self.acsPlot)
		self.curveA2 = Qwt.QwtPlotCurve("P2")
		self.curveA2.attach(self.acsPlot)
		self.curveA3 = Qwt.QwtPlotCurve("P3")
		self.curveA3.attach(self.acsPlot)
		self.curveA4 = Qwt.QwtPlotCurve("P4")
		self.curveA4.attach(self.acsPlot)
		self.curveA5 = Qwt.QwtPlotCurve("P5")
		self.curveA5.attach(self.acsPlot)
		
		self.curveA1.setPen(Qt.QPen(acsPenColors[0]))
		self.curveA2.setPen(Qt.QPen(acsPenColors[1]))
		self.curveA3.setPen(Qt.QPen(acsPenColors[2]))
		self.curveA4.setPen(Qt.QPen(acsPenColors[3]))
		self.curveA5.setPen(Qt.QPen(acsPenColors[4]))
		
		
		self.a1 = zeros(len(self.x), Float)
		self.curveA1.setData(self.x, self.a1)
		
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
		
		self.setLayout(self.hbox)
		self.prsPlot.replot()
		self.acsPlot.replot()      


class sensor():
	def __init__(self, device):
		self.port = serial.Serial(device,9600, timeout=1)
	def readValue():
		value=self.port.readline()
		return value
	def close():
		self.port.close()
		


        
app = Qt.QApplication(sys.argv)
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
print "hello"
demo = mainPlot()
demo.resize(1000, 700)
demo.show()
sys.exit(app.exec_())

    
    
    
