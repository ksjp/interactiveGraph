from tkinter import Tk, Canvas, PhotoImage, mainloop
from math import *


#class definitions

class infoWindow:
    """
    InfoWindow class:
    Handles variables and drawing of content of the information window
    Tends to be a contained member (can have more than one potentially!) of the GraphWindow class
    """

    def __init__(self, canvas, gw):
        self.canvas = canvas
        self.graphW = gw
        self._id = []

    def draw(self):
        while(len(self._id) != 0):
            self.canvas.delete(self._id.pop())
        myString = str(self.graphW.getPos())
        self._id.append( self.canvas.create_text(100,100,text=myString,fill="white"))
        

class GraphWindow:
    """
    GraphWindow class:
    Handles variables and drawing of the graph window contents that represent a plot with a point on it that can be moved around
    And anything else parented on the GraphWindow (which, if it grows too much, should be moved to another class)
    """
    def __init__(self):
        self.posx = 0  #posx, posy, sizex, oldx, refer to location of the mouse active object
        self.posy = 0
        self.sizex = 5
        self.color = "blue"
        self.oldx = -1
        self.oldy = -1
        self.centerx = WIDTH / 2
        self.centery = HEIGHT / 2
        self._id = []
        
    def __init__(self,px,py,sx,sy,color):
        self.posx = px
        self.posy = py
        self.sizex = sx
        self.color = color
        self.oldx = -1
        self.oldy = -1
        self.centerx = WIDTH / 2
        self.centery = HEIGHT / 2
        self._id = []

    def setCanvas(self, canvas):
        self.canvas = canvas
        
    def move(self, newx, newy):
        self.posx = newx
        self.posy = newy
        
    def moveDelta(self, dx, dy):
        self.posx += dx
        self.posy += dy

    def draw(self):
        while(len(self._id) != 0):
            self.canvas.delete(self._id.pop())    
        self.__drawPlot();
        self.__drawCircle();
        self.__drawArrow();
        self.__updateInfoWindow()

    def __drawPlot(self):
        self._id.append(self.canvas.create_line(self.centerx, self.centery + HEIGHT/2, self.centerx, self.centery - HEIGHT/2, fill="white"))
        self._id.append(self.canvas.create_line(self.centerx + WIDTH/2, self.centery, self.centerx - WIDTH/2, self.centery, fill="white"))
        
    def __drawArrow(self):
        radius = self.sizex / 2
        vx = self.posx - self.centerx + radius
        vy = self.posy - self.centery - radius
        length = sqrt(vx*vx + vy*vy)
        vxhat = vx / length 
        vyhat = vy / length 
        self._id.append(self.canvas.create_line(self.centerx, self.centery,self.posx + radius - vxhat * radius, self.posy + radius - vyhat * radius,fill="red", arrow="last"))

    def __drawCircle(self):
        self._id.append(self.canvas.create_oval(self.posx, self.posy, self.sizex+self.posx, self.sizex+self.posy, fill=self.color))

    def __updateInfoWindow(self):
        self.infoW.draw();
        
    def clickedInside(self,cx, cy):
        vx = cx - self.posx
        vy = cy - self.posy
        if(vx < self.sizex and vy < self.sizex):
            return 1
        return 0

    def parentOn(self, cx, cy):
        self.move(cx-self.sizex/2,cy-self.sizex/2)

    def getPos(self):
        return (self.posx + self.sizex/2 - self.centerx, -1* (self.posy + self.sizex/2 - self.centery))

    def addInfoWindow(self, canvas):
        self.infoW = infoWindow(canvas, self); 
        
#end class definitions


"""
Mouse Handlers
Parent the GraphWindow whenever the mouse is pressed down
"""
def mouseDown(event):
    mouseDown = 1
def mouseUp(event):
    mouseDown = 0
def mouseClick(event):
    cx = event.x
    cy = event.y
    mouseI.parentOn(cx,cy)
    mouseI.draw()
        

"""
Global Variables, main script
"""
#global variables
WIDTH, HEIGHT = 640, 480
mouseDown = 0

#window initialization, more declarations
gwindow = Tk()
canvas = Canvas(gwindow, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
mouseI = GraphWindow(100,100,25,25,"blue")
mouseI.setCanvas(canvas)
iwindow = Tk()
canvasi = Canvas(iwindow, width=WIDTH, height=HEIGHT, bg="#000000")
canvasi.pack()
mouseI.addInfoWindow(canvasi)

#bind in mouse handlers
canvas.bind("<Button-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)
canvas.bind("<B1-Motion>", mouseClick)   

#initial draw and start loop
mouseI.draw()
mainloop()
