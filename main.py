#version 2
#Main - resposible for calling the functions sequentially
#Author: Ruopan Li (Robin)
#Date: 06/12/2022
#Inputs: user inputs
#Outputs: modifications to the GUI - displaying graphs, buttons, etc.

from tkinter import *
import math
import KdV as kdv
import time

import plotter as plot

class controlPanel:
    def __init__(self, master):
        self.inputpanel = master
        self.inputpanel.title("Control Panel")

        self.labels = []
        self.entries = []

        self.flag1 = "play"  #determines whether to keep playing the animation
#0
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=1, column=1, padx=5, pady=5)
        new_entry.insert(0,"0.02")
        self.entries.append(new_entry)
        #1
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=2, column=1, padx=5, pady=5)
        new_entry.insert(0,"0.002")
        self.entries.append(new_entry)
        #2
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=3, column=1, padx=5, pady=5)
        new_entry.insert(0,"50")
        self.entries.append(new_entry)
        #3
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=4, column=1, padx=5, pady=5)
        new_entry.insert(0,"0.03")
        self.entries.append(new_entry)
        #4
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=5, column=1, padx=5, pady=5)
        new_entry.insert(0, "1")
        self.entries.append(new_entry)

        #scaling and panning
        #5
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=6, column=1, padx=5, pady=5)
        new_entry.insert(0, "0")
        self.entries.append(new_entry)
        #6
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=7, column=1, padx=5, pady=5)
        new_entry.insert(0, "0")
        self.entries.append(new_entry)
        #7
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=8, column=1, padx=5, pady=5)
        new_entry.insert(0, "1000")
        self.entries.append(new_entry)
        #8
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=9, column=1, padx=5, pady=5)
        new_entry.insert(0, "500")
        self.entries.append(new_entry)
        #9
        new_entry = Entry(self.inputpanel)
        new_entry.grid(row=10, column=1, padx=5, pady=5)
        new_entry.insert(0, "1")
        self.entries.append(new_entry)

        new_label = Label(self.inputpanel, text="dx")
        new_label.grid(row=1, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="dt")
        new_label.grid(row=2, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="N")
        new_label.grid(row=3, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="delta")
        new_label.grid(row=4, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="A")
        new_label.grid(row=5, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="X offset")
        new_label.grid(row=6, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="Y offset")
        new_label.grid(row=7, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="X scale")
        new_label.grid(row=8, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="Y scale")
        new_label.grid(row=9, column=0, padx=5, pady=5)
        self.labels.append(new_label)
        new_label = Label(self.inputpanel, text="simulation duration")
        new_label.grid(row=10, column=0, padx=5, pady=5)
        self.labels.append(new_label)

        w = Tk()
        self.G = plot.graphsketcher(w)
        Button(self.inputpanel, text = "Show analytical result animation", command = self.analytical_animation).grid(row = 1, column = 2, padx = 0, pady = 0)
        Button(self.inputpanel, text = "Show numerical result animation", command = self.numerical_animation).grid(row = 4, column = 2, padx = 0, pady = 0)
        Button(self.inputpanel, text = "Clear all", command = self.G.clear).grid(row = 2, column = 2, padx = 0, pady = 0)
        Button(self.inputpanel, text = "pause / unpause animation", command = self.trigger).grid(row = 3, column = 2, padx = 0, pady = 0)

        w.mainloop()

    def trigger(self):
        if self.flag1 == "play":
            self.flag1 = "stop"
        else:
            self.flag1 = "play"

    def numerical_animation(self):

        #numerical approximation using finite elements method

        #extract inputs
        dx = float(self.entries[0].get())
        dt = float(self.entries[1].get())
        N  = int(self.entries[2].get())
        delta = float(self.entries[3].get())
        A = float(self.entries[4].get())
        x_offset = float(self.entries[5].get())
        y_offset = float(self.entries[6].get()) 
        x_scale = float(self.entries[7].get())
        y_scale = float(self.entries[8].get())
        duration = float(self.entries[9].get())

        #generate initial conditions
        initial_waveform = kdv.init_gen(N, A, delta, dx)
        #initiate the KdV class
        dataClass = kdv.kdv(N, initial_waveform, duration, dt, dx, A, delta)

        #call the numerical approximation method
        numerical_solution = dataClass.numerical()
        print(numerical_solution)




    def analytical_animation(self):
        #extract inputs
        #call the kdv module
        #then plot the graph

        #now get the inputs
        dx = float(self.entries[0].get())
        dt = float(self.entries[1].get())
        N  = int(self.entries[2].get())
        delta = float(self.entries[3].get())
        A = float(self.entries[4].get())
        x_offset = float(self.entries[5].get())
        y_offset = float(self.entries[6].get()) 
        x_scale = float(self.entries[7].get())
        y_scale = float(self.entries[8].get())
        duration = float(self.entries[9].get())

        #generate the initial conditions
        initial_waveform = kdv.init_gen(N, A, delta, dx)

        #initiate the KdV class
        dataClass = kdv.kdv(N, initial_waveform, duration, dt, dx, A, delta)

        #calculate analytical result
        analytical_result = dataClass.analytical()
        print(analytical_result)
            
        #write results to text file for easy viewing
        file = open("analytical.txt", "w")
        rows = len(analytical_result)
        for m in range(0, rows):
            line = ""
            cols = len(analytical_result[0])
            for n in range(0, cols):
                line += str(round(analytical_result[m][n], 2)) + " , "
            line += "\n"
            file.write(line)
        file.close()

        #draw animation - use the graph plotter module
        #create a new window for them
        plotterWindow = Tk() 
        self.G  = plot.graphsketcher(plotterWindow) 

        #iterate through all rows of the table, plotting a frame on the graph for each row
        #i marks vertical incresments in time, j is horizontal across the table in position
        for i in range(0, rows):
            x = [None]*N
            y = [None]*N

            #decompose the 2D array into strips of x and y
            for j in range(0, N):
                x[j] = j * dx
                y[j] = analytical_result[i][j]

            xprime, yprime = self.G.mapping(x, y, x_offset, y_offset, x_scale, y_scale)
            self.G.clear()
            self.G.draw(xprime, yprime)
            self.G.drawAxisLabels(x_offset, y_offset, x_scale, y_scale)
            time.sleep(dt)

        # soliton_numerical= dataClass.numerical(soliton_analytical[0], 0.03, 1, 0.002, 0.02)
        # print(soliton_numerical)
        # file = open("numerical.txt", "w")
        # rows = len(soliton_numerical)
        # for m in range(0, rows):
        #     line = ""
        #     for n in range(0, cols):
        #         line += str(soliton_numerical[m][n]) + " , "
        #     line += "\n"
        #     file.write(line)
        # file.close()

        # #draw the lines
        # x_offset = float(self.entries[5].get())
        # y_offset = float(self.entries[6].get())
        # x_scale = float(self.entries[7].get())
        # y_scale = float(self.entries[8].get())

        # x = [None]*cols
        # for i in range(0, cols):
        #     x[i] = i * dx

        # i = 0
        # while i < rows:

        #     if self.flag1 == "play":

        #         y1 = soliton_numerical[i]
        #         y2 = soliton_analytical[i]
        #         xprime, yprime1 = self.G.mapping(x, y1, x_offset, y_offset, x_scale, y_scale)
        #         xprime2, yprime2 = self.G.mapping(x, y2, x_offset, y_offset, x_scale, y_scale)
        #         self.G.clear()
        #         self.G.draw(xprime, yprime1)
        #         self.G.draw(xprime, yprime2)
        #         self.G.drawAxisLabels( x_offset, y_offset, x_scale, y_scale)
        #         i += 1
        #         time.sleep(1)

        #     else:
        #         self.inputpanel.update()

#create tkinter window object
root = Tk()
#let the controlPanel class inherit this object
controlPanel(root)
#keep the window open ; prevent it from self destructing
root.mainloop()
