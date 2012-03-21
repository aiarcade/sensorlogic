#!/usr/bin/env python

# The Python version of Qwt-5.0.0/examples/data_plot
# for debugging, requires: python configure.py  --trace ...
if False:
	import sip
	sip.settracemask(0x3f)

import random
import sys
from numpy import interp
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import serial

class kalmanFilter():
	def __init__(self,q,r,p,initial_value):
		self.q=q
		self.p=p
		self.r=r
		self.x=initial_value
	def addSample(self,measurement):
		self.p=self.p+self.q
		self.k=self.p/(self.p+self.r)
		self.x= self.x + self.k*(measurement-self.x);
		self.p=(1-self.k)*self.p;
		return self.x;


class DataPlot(Qwt.QwtPlot):

	def __init__(self, *args):
		Qwt.QwtPlot.__init__(self, *args)
		self.port = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
		self.filter=kalmanFilter(0.4, 256, 100, 0)
		self.setCanvasBackground(Qt.Qt.white)
		self.alignScales()
		self.dataFile=open("adata.csv","w")
		self.dataFile.writelines("Time;P1,P2,P3,P4,P5\n")
		
		self.ptime=0
		# Initialize data
		self.x = arange(0.0, 100.1, 0.5)
		self.x1 = zeros(len(self.x), Float)
		self.y1 = zeros(len(self.x), Float)
		self.z1 = zeros(len(self.x), Float)
	

		self.setTitle("Acceleration")
		self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

		self.curveX1 = Qwt.QwtPlotCurve("X1")
		self.curveX1.attach(self)
		self.curveY1 = Qwt.QwtPlotCurve("Y1")
		self.curveY1.attach(self)

		#self.curveL.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,Qt.QBrush(),Qt.QPen(Qt.Qt.yellow),Qt.QSize(7, 7)))

		self.curveX1.setPen(Qt.QPen(Qt.Qt.red))
		self.curveY1.setPen(Qt.QPen(Qt.Qt.blue))

		self.curveZ1 = Qwt.QwtPlotCurve("Z1")
		self.curveZ1.attach(self)
		self.curveZ1.setPen(Qt.QPen(Qt.Qt.green))



		mY = Qwt.QwtPlotMarker()
		mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
		mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
		mY.setYValue(0.0)
		mY.attach(self)

		self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
		self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")
	
		self.startTimer(3)
		self.phase = 0.0

	# __init__()

	def alignScales(self):
		self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
		self.canvas().setLineWidth(1)
		for i in range(Qwt.QwtPlot.axisCnt):
			scaleWidget = self.axisWidget(i)
			if scaleWidget:
				scaleWidget.setMargin(0)
			scaleDraw = self.axisScaleDraw(i)
			if scaleDraw:
				scaleDraw.enableComponent(
					Qwt.QwtAbstractScaleDraw.Backbone, False)

	# alignScales()
	
	def timerEvent(self, e):
		if self.phase > pi - 0.0001:
			self.phase = 0.0
		line=self.port.readline()
		voltage=0
		print line
		g=0
		line=line.replace("\n","")
		try:		
			data=float(line)
			volt=interp(data,[0,1023],[0,5])
			volt=volt-1.35
			g=(volt*1000)/800
			g=round(g,3)
		#print data
		except:
			print "Unknown value"
			g=0
		org_g=g
		g=self.filter.addSample(g)	
		g=self.filter.addSample(g)
		# y moves from left to right:
		# shift y array right and assign new value y[0]
		self.x1 = concatenate((self.x1[:1], self.x1[:-1]), 1)
		self.x1[0] =g
		self.y1 = concatenate((self.y1[:1], self.y1[:-1]), 1)
		self.y1[0] =g

		self.z1 = concatenate((self.z1[:1], self.z1[:-1]), 1)
		self.z1[0] =org_g

	

		#self.dataFile.writelines(str(self.ptime)+";"+s[0]+";"+s[1]+";"+s[2]+";"+s[3]+";"+s[4]+"\n")
		self.ptime=self.ptime+1
		if self.ptime==5000:
			self.ptime=0

		self.curveX1.setData(self.x, self.x1)
		self.curveY1.setData(self.x, self.y1)
		self.curveZ1.setData(self.x, self.z1)
	
		self.replot()
		

	# timerEvent()

# class DataPlot

def make():
	demo = DataPlot()
	demo.resize(500, 300)
	demo.show()
	return demo

# make()

def main(args): 
	app = Qt.QApplication(args)
	demo = make()
	sys.exit(app.exec_())

# main()

# Admire
if __name__ == '__main__':
	main(sys.argv)

# Local Variables: ***
# mode: python ***
# End: ***
