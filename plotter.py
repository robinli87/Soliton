from tkinter import *


class graphsketcher:
    def __init__(self, master):
        self.master = master #globalise this GUI object as master within our class
        self.master.title("2D Graph plotter")#set title of the window
        #self.master.state("zoomed")#set the size to fullscreen but windowed mode

        #set the GUI widgets as planned in the diagram

        self.canvas = Canvas(self.master, width = 950, height = 930, background="white")
        self.canvas.pack(side=LEFT, fill = BOTH)

        self.ysize = 900
        self.xsize = 900

        self.canvas.create_line(30, 10, 30, self.ysize+10)
        self.canvas.create_line(30, self.ysize+10, self.xsize+30, self.ysize+10)
        self.canvas.create_text(25, 5, text="u")
        self.canvas.create_text(915, 925, text="x")

        self.segments = []


    def clear(self):
        for item in self.segments:
            self.canvas.delete(item)
        self.segments = []
        self.master.update()

    def mapping(self, rawx, rawy, x_offset, y_offset, x_scale, y_scale):
        #extract data from entries and convert them to decimal

        #create 2 empty arrays to store processed coordinates in the python space
        processedx = []
        processedy = []

        length = len(rawx)
        for i in range(0, length):
            #apply the transform equations as discussed in the lab book
            xpython = (rawx[i] - x_offset) * x_scale + 30
            ypython = 910 - (rawy[i] - y_offset) * y_scale
            processedx.append(xpython)
            processedy.append(ypython)

        return(processedx, processedy)

    def drawAxisLabels(self, x_offset, y_offset, x_scale, y_scale):
        #extract offsets and scale
        #draw x first
        for i in range(0, 8):
            #create a marker which is a small straight line perpendicular to the axis
            marker = self.canvas.create_line(i*100+30, 907, i*100+30, 913)
            self.segments.append(marker)
            #we need to label this point, so calculate the value at this marker then draw it as text
            label = round(i * 100 / x_scale + x_offset, 4)
            marker = self.canvas.create_text(i*100+30, 917, text = str(label))
            #append the marker so that we can clean it up later
            self.segments.append(marker)

            #then draw y, using identical method
        for i in range(0, 8):
            marker = self.canvas.create_line(27, 910 - i * 100, 33, 910 - i * 100)
            self.segments.append(marker)
            label = round(i * 100 / y_scale + y_offset, 4)
            marker = self.canvas.create_text(20, 910 - i * 100, text = str(label))
            self.segments.append(marker)

        self.master.update()
		
		
    def simpledraw(self, x, y):
        xprime, yprime = self.mapping(x, y)
        self.clear()
        self.draw(xprime, yprime)
        self.drawAxisLabels()
		
    def draw(self, x, y):
        #find length of array. One can embed this in the for loop but this is more optimised.
        length = len(x)
        for i in range(0, length-2):
            #we can't reliably sketch curves in Python but many short line segments will assemble a "curve"
            #each segment links the nth point and n+1 th point
            segment = self.canvas.create_line(x[i], y[i], x[i+1], y[i+1])
            #append so we can clean up
            self.segments.append(segment)
        self.master.update()
        


