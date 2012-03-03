#!/usr/bin/env python

# The Python version of Qwt-5.0.0/examples/data_plot

# for debugging, requires: python configure.py  --trace ...
if False:
    import sip
    sip.settracemask(0x3f)

import random
import sys

from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import serial

class DataPlot(Qwt.QwtPlot):

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)
	self.port = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
        self.setCanvasBackground(Qt.Qt.white)
        self.alignScales()
	self.dataFile=open("pdata.csv","w")
	self.dataFile.writelines("Time;P1,P2,P3,P4,P5\n")
         
	self.ptime=0
        # Initialize data
        self.x = arange(0.0, 100.1, 0.5)
        self.p1 = zeros(len(self.x), Float)
        self.p2 = zeros(len(self.x), Float)
        self.p3 = zeros(len(self.x), Float)
	self.p4 = zeros(len(self.x), Float)
	self.p5 = zeros(len(self.x), Float)

        self.setTitle("Pressure sensors")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        self.curveP1 = Qwt.QwtPlotCurve("P1")
        self.curveP1.attach(self)
        self.curveP2 = Qwt.QwtPlotCurve("P2")
        self.curveP2.attach(self)

        #self.curveL.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,Qt.QBrush(),Qt.QPen(Qt.Qt.yellow),Qt.QSize(7, 7)))

        self.curveP1.setPen(Qt.QPen(Qt.Qt.red))
        self.curveP2.setPen(Qt.QPen(Qt.Qt.blue))

	self.curveP3 = Qwt.QwtPlotCurve("P3")
        self.curveP3.attach(self)
        self.curveP4 = Qwt.QwtPlotCurve("P4")
        self.curveP4.attach(self)

        #self.curveL.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,Qt.QBrush(),Qt.QPen(Qt.Qt.yellow),Qt.QSize(7, 7)))

        self.curveP3.setPen(Qt.QPen(Qt.Qt.cyan))
        self.curveP4.setPen(Qt.QPen(Qt.Qt.yellow))

	self.curveP5 = Qwt.QwtPlotCurve("P5")
        self.curveP5.attach(self)
	
        self.curveP5.setPen(Qt.QPen(Qt.Qt.green))



        mY = Qwt.QwtPlotMarker()
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.attach(self)

        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")
    
        self.startTimer(50)
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
	s=line.split("#")
	
        # y moves from left to right:
        # shift y array right and assign new value y[0]
        self.p1 = concatenate((self.p1[:1], self.p1[:-1]), 1)
        self.p1[0] =float(s[0])
	
	self.p2 = concatenate((self.p2[:1], self.p2[:-1]), 1)
	self.p2[0] =float(s[1])

	self.p3 = concatenate((self.p3[:1], self.p3[:-1]), 1)
        self.p3[0] =float(s[2])

	self.p4 = concatenate((self.p4[:1], self.p4[:-1]), 1)
        self.p4[0] =float(s[3])

	self.p5 = concatenate((self.p5[:1], self.p5[:-1]), 1)
        self.p5[0] =float(s[4])

        self.dataFile.writelines(str(self.ptime)+";"+s[0]+";"+s[1]+";"+s[2]+";"+s[3]+";"+s[4]+"\n")
	self.ptime=self.ptime+1
	if self.ptime==5000:
		self.ptime=0

        self.curveP1.setData(self.x, self.p1)
        self.curveP2.setData(self.x, self.p2)
        self.curveP3.setData(self.x, self.p3)
	self.curveP4.setData(self.x, self.p4)
	self.curveP5.setData(self.x, self.p5)
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
