import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtWidgets, mkQApp
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider
from PyQt6.QtCore import Qt
from PyQt6 import uic
 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        def valmap(x, amin, amax, bmin, bmax):
            aw=amax-amin
            bw=bmax-bmin
            return (x-amin)/aw*bw+bmin
        def func(x, y, z, x0, y0, z0, p0, wavelength):
            x = valmap(x, 0, self.n_points, self.minmax[0], self.minmax[1])-x0
            y = valmap(y, 0, self.n_points, self.minmax[2], self.minmax[3])-y0
            z = valmap(z, 0, self.n_points, self.minmax[0], self.minmax[1])-z0
            r = (x**2+y**2+z**2)**0.5
            phi = r*2*np.pi/wavelength+p0
            return np.exp(1j*phi)*r**(-2)
        def calculate():
            total = sources[1]  + sources[3] # + sources[2]
            #real = total.real
            #mul=real
            amplitude = abs(total)
            #mul=amplitude
            #phase = np.angle(total)%np.pi
            #mul=phase
            intensity = amplitude**2
            mul = intensity
            return valmap(mul, np.min(mul), np.max(mul), 0, 1)
        def calculate1():
            total = sources[0]
            #real = total.real
            #mul=real
            amplitude = abs(total)
            #mul=amplitude
            #phase = np.angle(total)%np.pi
            #mul=phase
            intensity = amplitude**2
            mul = intensity
            return valmap(mul, np.min(mul), np.max(mul), 0, 1) 
        def source(x0, y0, z0, p0, wavelength):
            return np.fromfunction(lambda x, y: func(x, y, z0, x0, y0, z0, p0, wavelength), (self.n_points, self.n_points))
        def update_image():
            self.n_points = int(self.ndots.text())
            wavelength = float(self.wavelength.text())
            self.width = float(self.wh.text())*10**6
            self.height = float(self.wh_2.text())*10**6
            self.n_points = int(self.ndots.text())
            self.minmax = [-self.width/2, self.width/2, -self.height/2, self.height/2]
            x0 = float(self.x0.text())*10**6
            y0 = float(self.y0.text())*10**6
            z0 = float(self.z0.text())*10**6
            for i in range(1, 4):
                x = float(getattr(self, f"x{i}").text())
                y = float(getattr(self, f"y{i}").text())
                z = float(getattr(self, f"z{i}").text())
                p = float(getattr(self, f"p{i}").text())*np.pi*2
                sources[i] = source(x+x0, y+y0, z+z0, p, wavelength) #nm
            i1 = pg.ImageItem(image=255*calculate())
            plot1.clear()
            plot1.addItem(i1)
            for i in range(1, 4):
                x = float(getattr(self, f"x{i}").text())
                y = float(getattr(self, f"y{i}").text())
                plot1.plot([valmap(x0, self.minmax[0], self.minmax[1], 0, self.n_points)], [valmap(y0, self.minmax[2], self.minmax[3], 0, self.n_points)], symbol="o", symbolSize=20, symbolBrush="b")
            
        uic.loadUi('main.ui', self)
        self.show()
        self.width = float(self.wh.text())*10**6
        self.height = float(self.wh_2.text())*10**6
        self.n_points = int(self.ndots.text())
        self.minmax = [-self.width//2, self.width//2, -self.height//2, self.height//2]
        sources=[0,0,0,0]
        w2 = pg.GraphicsLayoutWidget()
        plot1 = w2.addPlot()
        plot1.showAxes(True, showValues=(True,False,False,True) )
        plot1.setRange(xRange=(0,self.n_points), yRange=(0, self.n_points), padding=0)
        self.layout1.addWidget(w2)
        
        self.updateImage.clicked.connect(update_image)

mkQApp("ColorBarItem Example")
main_window = MainWindow()

## Start Qt event loop
if __name__ == '__main__':
    pg.exec()
