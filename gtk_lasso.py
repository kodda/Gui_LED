from gi.repository import Gtk
import LED_matrix as LD
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

class CurrentColor:
   def __init__(self):
      self.red=0
      self.green=0

   def update_red(self,state):
      self.red=state

   def update_green(self,state):
      self.green=state

   def colorname(self):
     cname=""
     if (self.red and self.green): cname="orange"
     if (self.red and not(self.green)): cname="red"
     if (not(self.red) and self.green): cname="green"
     if (not(self.red) and not(self.green)): cname="blank"
     return cname

   def rgb(self):
      return [int(self.red), int(self.green),0] 

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def on_Red_clicked(self, Red):
       cColor.update_red(Red.get_active())
       lman.cColor=cColor.red+2*cColor.green
       print "Current color",cColor.colorname()

    def on_Green_clicked(self, Green):
       cColor.update_green(Green.get_active())
       lman.cColor=cColor.red+2*cColor.green
       print "Current color",cColor.colorname()


N1=160
N2=32

#N1=8
#N2=8

cColor=CurrentColor()

builder = Gtk.Builder()
builder.add_from_file("aff.glade")
builder.connect_signals(Handler())
sw = builder.get_object("scrolledwindow1")
#sw = Gtk.ScrolledWindow()
#win.add(sw)

ax,vals=LD.matrix_figure(N1,N2)
#lman=LD.LassoManager(ax,canvas, vals,N1,N2)

canvas = FigureCanvas(ax.figure)  # a Gtk.DrawingArea
canvas.set_size_request(800,160)
lman=LD.LassoManager(ax,canvas,vals,N1,N2)
sw.set_border_width (0)

canvas.show()
sw.add_with_viewport (canvas)

win1 = builder.get_object("window1")
win1.show_all()

Gtk.main()
