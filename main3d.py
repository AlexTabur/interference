import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtWidgets, mkQApp
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider
from PyQt6.QtCore import Qt
from PyQt6 import uic
n_points = 200
minmax = [-1000, 1000]
tr = -n_points*0.5
sources=[0,0,0]
sources1=[0,0,0]
n_dimensions = 3
a = 0
def valmap(x, amin, amax, bmin, bmax):
    aw=amax-amin
    bw=bmax-bmin
    return (x-amin)/aw*bw+bmin
def func(x, y, z, x0, y0, z0, p0, wavelength):
    x = valmap(x, 0, n_points, minmax[0], minmax[1])-x0
    y = valmap(y, 0, n_points, minmax[0], minmax[1])-y0
    z = valmap(z, 0, n_points, minmax[0], minmax[1])-z0
    r = (x**2+y**2+z**2)**0.5
    phi = r*2*np.pi/wavelength+p0
    return np.exp(1j*phi)#*r**(-2)
def calculate():
    total = sources[0] + sources[1] #+ sources[2]
    #real = total.real
    #mul=real
    amplitude = abs(total)
    #mul=amplitude
    #phase = np.angle(total)%np.pi
    #mul=phase
    intensity = amplitude**2
    mul = intensity
    return valmap(mul, np.min(mul), np.max(mul), 0, 1)  
def calculate1(num):
    total = sources[num]
    #real = total.real
    #mul=real
    amplitude = abs(total)
    #mul=amplitude
    #phase = np.angle(total)%np.pi
    #mul=phase
    intensity = amplitude**2
    mul = intensity
    return valmap(mul, np.min(mul), np.max(mul), 0, 1)  
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('main2.ui', self)
        self.show()
        def update_source(i):
            def func():
                x0 = getattr(self, f"x{i}").value() / n_points
                y0 = getattr(self, f"y{i}").value() / n_points
                z0 = getattr(self, f"z{i}").value() / n_points
                p0 = getattr(self, f"p{i}").value() / n_points
                update_image(x0, y0, z0, p0, i)
            return func
        if n_dimensions==2:
            w2 = pg.GraphicsLayoutWidget()
            plot1 = w2.addPlot()
            plot1.showAxes(True, showValues=(True,False,False,True) )
            plot1.setRange(xRange=(0,n_points), yRange=(0, n_points), padding=0)
            self.layout1.addWidget(w2)
            roi_circle = pg.CircleROI([250, 250], [120, 120], pen=pg.mkPen('r',width=2))
            def source(x0, y0, z0, p0, wavelength):
                return np.fromfunction(lambda x, y: func(x, y, z0, x0, y0, z0, p0, wavelength), (n_points, n_points))
            def update_image(x0, y0, z0, p0, num):
                sources[num] = source(x0, y0, z0, p0, 1)
                i1 = pg.ImageItem(image=255*calculate())
                plot1.clear()
                plot1.addItem(i1)
                x0 = getattr(self, f"x0").value() / n_points
                y0 = getattr(self, f"y0").value() / n_points
                x1 = getattr(self, f"x1").value() / n_points
                y1 = getattr(self, f"y1").value() / n_points
                x2 = getattr(self, f"x2").value() / n_points
                y2 = getattr(self, f"y2").value() / n_points
                plot1.plot([valmap(x0, minmax[0], minmax[1], 0, n_points)], [valmap(y0, minmax[0], minmax[1], 0, n_points)], symbol="o", symbolSize=20, symbolBrush="b")
                plot1.plot([valmap(x1, minmax[0], minmax[1], 0, n_points)], [valmap(y1, minmax[0], minmax[1], 0, n_points)], symbol="o", symbolSize=20, symbolBrush="b")
                plot1.plot([valmap(x2, minmax[0], minmax[1], 0, n_points)], [valmap(y2, minmax[0], minmax[1], 0, n_points)], symbol="o", symbolSize=20, symbolBrush="b")
        if n_dimensions==3:
            data = np.ones((n_points, n_points, n_points, 4), dtype=np.ubyte)*255
            #data[..., 3] = 0
            w3 = gl.GLViewWidget()
            w3.setCameraPosition(distance=50)
            v = gl.GLVolumeItem(data)
            v.translate(tr,tr,tr)
            w3.addItem(v)
            g = gl.GLGridItem()
            g.scale(10, 10, 1)
            w3.addItem(g)
            self.layout1.addWidget(w3)
            
            def source(x0, y0, z0, p0, wavelength):
                return np.fromfunction(lambda x, y, z: func(x, y, z, x0, y0, z0, p0, wavelength), (n_points, n_points, n_points))
            def update_image(x0, y0, z0, p0, num):
                sources[num] = source(x0, y0, z0, p0, 1)
                #a = calculate1(0)
                #b = calculate1(1)
                #c = 0 #calculate1(2)
                d = calculate()*255
                #print(np.max(a), np.max(b), np.max(c))
                data[..., 0] = d#(a+b+c)*255//3 #(255*a + 0*b   + 255*c)//2
                data[..., 1] = d#(a+b+c)*255//3 #(0*a   + 255*b + 255*c)//2
                data[..., 2] = d#(a+b+c)*255//3 #(255*a + 255*b + 0*c  )//2
                data[..., 3] = d//2# (a+b)*255//2//10
                v.setData(data)
        for a in ["x", "y", "z", "p"]:
            for num in range(3):
                getattr(self, f"{a}{num}").sliderReleased.connect(update_source(num))
                getattr(self, f"{a}{num}").setMinimum(n_points*minmax[0])
                getattr(self, f"{a}{num}").setMaximum(n_points*minmax[1])
mkQApp("ColorBarItem Example")
main_window = MainWindow()

## Start Qt event loop
if __name__ == '__main__':
    pg.exec()