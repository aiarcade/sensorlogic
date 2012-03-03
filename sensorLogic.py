import sys

from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import serial

class sensor():
	def __init__(self, device):
		self.port = serial.Serial(device,9600, timeout=1)
	def readValue():
		value=self.port.readline()
		return value
	def close():
		self.port.close()
		

class mainPlot(Qt.QWidget):
	def __init__(self, *args):
		Qt.QWidget.__init__(self, *args)
		self.layout = Qt.QGridLayout(self)
		self.prsPlot = Qwt.QwtPlot(self)
        self.prsPlot.setTitle('Pressure Sensor')
        self.prsPlot.setCanvasBackground(Qt.Qt.white)
        self.prsPlot.plotLayout().setCanvasMargin(0)
        self.prsPlot.plotLayout().setAlignCanvasToScales(True)
        self.layout.addWidget( self.prsPlot, 0, 0)
        self.prsPlot.replot()
        
        
def main(args):
    app = Qt.QApplication(args)
    demo = make()
    sys.exit(app.exec_())

# main()


def make():
    demo = mainPlot()
    demo.resize(400, 600)
    demo.show()
    return demo

# make()


# Admire!
if __name__ == '__main__':
    main(sys.argv)
