import sys
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import serial


class mainPlot(Qt.QWidget):
	def __init__(self, *args):
		print "hello"
		Qt.QWidget.__init__(self, *args)
		self.layout=Qt.QGridLayout(self)
		#Pressure graph
		self.prsPlot=Qwt.QwtPlot(self)
		self.prsPlot.setTitle('Pressure Sensor')
		self.prsPlot.setCanvasBackground(Qt.Qt.white)
		self.prsPlot.plotLayout().setCanvasMargin(0)
		self.prsPlot.plotLayout().setAlignCanvasToScales(True)
		self.layout.addWidget( self.prsPlot, 0, 0)
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
		self.prsPlot.replot()
        


class sensor():
	def __init__(self, device):
		self.port = serial.Serial(device,9600, timeout=1)
	def readValue():
		value=self.port.readline()
		return value
	def close():
		self.port.close()
		


        
app = Qt.QApplication(sys.argv)
print "hello"
demo = mainPlot()
demo.resize(400, 600)
demo.show()
sys.exit(app.exec_())

    
    
    
