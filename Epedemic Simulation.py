import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import matplotlib.pyplot as plt
from matplotlib import style
from tkinter import *
global n
global s
n = 800
s = n
width = 650
height = 650

class Person():
    def __init__(self, canvas, x, y, fill, speed, range_, testFactor):
        r = 2.75
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        self.speed = speed
        self.range_ = range_
        self.testFactor = testFactor * 100

        self.x = x
        self.y = y
        self.infected = False
        self.state = "healthy"
        self.timeInfected = 0

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')

    def move(self):
        dx = 0
        dy = 0
        if self.x < 20:
            dx = 20
        elif self.x > height-20:
            dx = -20
        elif self.y < 20:
            dy = 20
        elif self.y > height-20:
            dy = -20
        else:
            dx = random.choice([-self.speed, self.speed])
            dy = random.choice([-self.speed, self.speed])

        self.canvas.move(self.id, dx, dy)
        self.x = self.x + dx
        self.y = self.y + dy

    def check_infected(self, persons, ni):
        global s
        for persons in ni:
            if ((self.x - persons.x) * (self.x - persons.x) + (self.y - persons.y) * (self.y - persons.y) <=
                self.range_ * self.range_) and self.state=="healthy":
                self.infected = True
                s -= 1

            if self.infected == True and self.state != "dead" and self.state != "cured":
                self.timeInfected += 1
                if self.timeInfected < self.testFactor:
                    self.state = "aSym"
                    self.canvas.itemconfig(self.id, fill='yellow')
                elif self.timeInfected > self.testFactor and self.timeInfected < 1800:
                    self.state = "quan"
                    self.canvas.itemconfig(self.id, fill='red')
                    self.infected = False
                    self.range_= 0
                    self.speed = 0
                elif self.timeInfected > 1400:
                    if random.uniform(0,1) < 0.01:
                        self.state = "dead"
                        self.infected = False
                        self.canvas.itemconfig(self.id, fill='gray')
                        self.speed = 0
                    else:
                        self.state = "cured"
                        self.infected = False
                        self.canvas.itemconfig(self.id, fill='blue')
                        self.speed = 6

    def infect(self):
        self.infected = True

class App():
    def __init__(self, master):
        self.ni = []
        self.master = master
        self.canvas = tk.Canvas(self.master, width=width, height=height,background='black')
        self.canvas.pack()

        self.infobox = tk.Text(master,height=2,width=30)
        self.infobox.insert(INSERT,"Changes only apply after reset")
        self.infobox.pack(side=tk.TOP)

        self.but_reset = ttk.Button(master, text = "Restart", command=self.restart_sim)
        self.but_reset.pack(side=tk.TOP)

        self.but_graph = ttk.Button(master, text = "Update Graph", command=self.graph)
        self.but_graph.pack(side=tk.RIGHT)

        self.but_stop = ttk.Button(master, text = "STOP", command=self.stop_sim)
        self.but_stop.pack(side=tk.LEFT)

        self.var = DoubleVar()
        self.speed = tk.Scale(master,orient="horizontal", showvalue=1, label="SPEED", from_=1, to=10, variable=self.var, )
        self.speed.pack(side=tk.BOTTOM)
        self.var.set(6)
        speed = int(self.var.get())

        self.var2 = DoubleVar()
        self.speed = tk.Scale(master,orient="horizontal", showvalue=1, label="RANGE", from_=5, to=30, variable=self.var2,)
        self.speed.pack(side=tk.BOTTOM)
        self.var2.set(10)
        range_ = int(self.var2.get())

        self.var3 = DoubleVar()
        self.testFactor = tk.Scale(master,orient="horizontal", showvalue=1, label="TestFactor", from_=1, to=20, variable=self.var3,)
        self.testFactor.pack(side=tk.BOTTOM)
        self.var3.set(10)
        testFactor = int(self.var3.get())
        self.init_sim(speed,range_,testFactor)

        self.master.after(100, self.update)
        self.frame=0

    def init_sim(self, speed, range_, testFactor):
        self.canvas.delete('all')
        self.persons = []
        self.infectedX = [0]
        self.timeY = [0]
        self.frame = 0
        for i in range(n):
            x = random.randint(0,width)
            y = random.randint(0,height)
            p = Person(self.canvas, x, y, 'white', speed, range_, testFactor)
            self.persons.append(p)

            self.persons[0].infect()
            self.start=time.time()

        self.canvas.pack()

    def restart_sim(self):
        global s
        global n
        print(self.infectedX,self.timeY)
        print(s, "people was not infected")
        print("-----------------------------------------------")

        s = n
        speed = int(self.var.get())
        range_ = int(self.var2.get())
        testFactor = int(self.var3.get())
        self.init_sim(speed,range_,testFactor)

    def stop_sim(self):
        print(self.infectedX,self.timeY)

        self.canvas.delete('all')
        root.destroy()
        self.end=time.time()
        print("Frames:",app.frame)
        print("Runtime:",self.end-self.start)
        print("Framerate:", app.frame/(self.end-self.start))

    def graph(self):
        plt.ion()
        style.use('fivethirtyeight')
        plt.plot(self.timeY,self.infectedX)
        plt.xlabel('x - Infected')
        plt.ylabel('y - Time')
        plt.title('Infected over time')

    def update(self):
        self.ni = []
        for person in self.persons:
            if person.infected == True and person.state != "cured" and person.state != "cured":
                self.ni.append(person)

        for person in self.persons:
            person.move()
            person.check_infected(self.persons,self.ni)

        self.frame += 1
        self.master.after(10,self.update)

        if self.frame % 10 == 0:
            self.timeY.append(self.frame)
            self.infectedX.append(len(self.ni))

        if len(self.ni) == 0:
            self.graph()
            self.restart_sim()

root = tk.Tk()
App(root)
root.mainloop()
