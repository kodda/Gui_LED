import numpy as np
#import matplotlib.pyplot as plt
from matplotlib.widgets import Lasso
from matplotlib.figure import Figure 
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import matplotlib.colors as col
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from matplotlib import path


def matrix_figure(N1=160, N2=32):
   r=0.4

   fsx=20.
   fsy=fsx*N2/N1

   f=Figure(figsize=(fsx,fsy),frameon=False)
   #f=plt.figure(figsize=(fsx,fsy),frameon=False)
   
   ax=f.add_subplot(111,axisbg='k')
   ax.set_xlim([-2*r,N1-1+2*r])
   ax.set_ylim([-2*r,N2-1+2*r])
   ax.set_axis_bgcolor('k')
   ax.set_yticks([])
   ax.set_xticks([])
   ax.set_frame_on(False) 
   x=np.arange(N1)
   y=np.arange(N2)

   xx,yy=np.meshgrid(x,y)
   cmap = col.ListedColormap([ '#6E6E6E','#FE2E2E', '#64FE2E', '#FF8000'])
   colors=np.random.randint(0,4,(N1,N2))

   patches = []
   for x1,y1 in zip(xx.flatten(), yy.flatten()):
     circle = Circle((x1,y1), r)
     patches.append(circle)

   p = PatchCollection(patches, cmap=cmap)
   p.set_array(colors.flatten())
   ax.add_collection(p)
   f.subplots_adjust(0,0,1,1)
   return ax, colors

def make_xys(N1,N2):
   x=np.arange(N1)
   y=np.arange(N2)
   xx, yy=np.meshgrid(x,y)
   xys=[]
   for k in range(N1*N2):
      xys.append((xx.flatten()[k],yy.flatten()[k]))    
   return xys

class LassoManager(object):
    def __init__(self, ax, canvas, data, N1, N2):
        self.axes = ax
        self.canvas = canvas
        self.data = data
        fig = ax.figure
        self.collection = ax.collections[0]
        self.Nxy = len(data)
        self.xys=make_xys(N1,N2)
        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.cColor=0

    def callback(self, verts):
        vals = self.collection.get_array()
        p = path.Path(verts)
        ind = p.contains_points(self.xys)
        for i in range(len(self.xys)):
            if ind[i]: vals[i] = self.cColor 
        self.collection.set_array(vals)
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        del self.lasso

    def onpress(self, event):
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)
