from tkinter import *
from math import *
from utilitaries import *


class Switch:
    def __init__(self, root, function_on=f_pass, function_off=f_pass):
        self.state = False
        self.function_on, self.function_off = function_on, function_off
        self.canvas = Canvas(root, bg="#0A062E", relief="flat", highlightbackground="#0A062E", width=30, height=20)
        self.border = [
            self.canvas.create_oval(1, 1, 21, 21, fill="#343563", width="0"),
            self.canvas.create_oval(11, 1, 31, 21, fill="#343563", width="0"),
            self.canvas.create_rectangle(8, -1, 23, 22, fill="#343563", width="0")
        ]
        self.bg = [
            self.canvas.create_oval(2, 2, 20, 20, fill="#48498A", width="0"),
            self.canvas.create_oval(12, 2, 30, 20, fill="#48498A", width="0"),
            self.canvas.create_rectangle(9, 0, 22, 21, fill="#48498A", width="0")
        ]
        self.button = self.canvas.create_oval(4, 4, 18, 18, fill="#DDE0F5", width="0")
        self.canvas.bind("<Button-1>", self.switch)

    def place(self, x, y, anchor="nw"):
        self.canvas.place(x=x, y=y, anchor=anchor)

    def switch(self, e):
        self.state = not self.state
        if self.state:
            for i in range(20):
                self.canvas.after(int(i/100*1000), lambda x=-5*cos(i/20*pi)+5*cos((i-1)/20*pi): self.canvas.move(self.button, x, 0))
                rgb = tuple(((i+1)*hex_to_rgb("#F5C110")[j] + (19-i)*hex_to_rgb("#48498A")[j])//20 for j in range(3))
                for k in range(3): self.canvas.after(int(i/100*1000), lambda color=rgb_to_hex(rgb), idx=k: self.canvas.itemconfig(self.bg[idx], fill=color))
                rgb = tuple(((i+1)*hex_to_rgb("#B59644")[j] + (19-i)*hex_to_rgb("#343563")[j])//20 for j in range(3))
                for k in range(3): self.canvas.after(int(i/100*1000), lambda color=rgb_to_hex(rgb), idx=k: self.canvas.itemconfig(self.border[idx], fill=color))
            self.function_on()
        else:
            for i in range(20):
                self.canvas.after(int(i/100*1000), lambda x=5*cos(i/20*pi)-5*cos((i-1)/20*pi): self.canvas.move(self.button, x, 0))
                rgb = tuple(((19-i)*hex_to_rgb("#F5C110")[j] + (i+1)*hex_to_rgb("#48498A")[j])//20 for j in range(3))
                for k in range(3): self.canvas.after(int(i/100*1000), lambda color=rgb_to_hex(rgb), idx=k: self.canvas.itemconfig(self.bg[idx], fill=color))
                rgb = tuple(((i+1)*hex_to_rgb("#343563")[j] + (19-i)*hex_to_rgb("#B59644")[j])//20 for j in range(3))
                for k in range(3): self.canvas.after(int(i/100*1000), lambda color=rgb_to_hex(rgb), idx=k: self.canvas.itemconfig(self.border[idx], fill=color))
            self.function_off()

    def destroy(self):
        self.canvas.destroy()


class VinylSwitch:
    def __init__(self, root, function_on=f_pass, function_off=f_pass):
        self.state = False
        self.function_on, self.function_off = function_on, function_off
        self.canvas = Canvas(root, bg="#0A062E", relief="flat", highlightbackground="#0A062E", width=240, height=200)
        self.canvas.bind("<Button-1>", self.switch)
        self.canvas.create_oval(-39, 1, 199, 239, fill="#343563")
        self.canvas.create_oval(-36, 4, 196, 236, fill="black")
        for i in range(3):
            self.canvas.create_oval(-20+17*i, 20+17*i, 180-17*i, 220-17*i, fill="#343563")
            self.canvas.create_oval(-17+17*i, 23+17*i, 177-17*i, 217-17*i, fill="black")
        self.canvas.create_polygon(80, 120, 80, 10, 0, 40, -24, 180, 80, 120, 80, 240, 153, 203, 187, 126, 174, 66, fill="black")
        self.canvas.create_oval(55, 95, 105, 145, fill="#F5C110", outline="#B59644")
        self.canvas.create_oval(77, 117, 83, 123, fill="#0A062E", outline="#B59644")
        self.arm = [
            self.canvas.create_line(230, 210, 230, 40, width=7, fill="#3D3F75"),
            self.canvas.create_polygon(*(217, 28), *(220, 23), *(226, 24), *(235, 43), *(225, 47), fill="#585AA8")
        ]


    def place(self, x, y, anchor="nw"):
        self.canvas.place(x=x, y=y, anchor=anchor)

    def switch(self, e):
        self.state = not self.state
        if self.state:
            self.function_on()
            for i in range(30):
                angle = pi/7/30*i
                self.canvas.after(int(i/100*1000), lambda a=angle: self.canvas.coords(self.arm[0], 230, 210, 230-sin(a)*170, 40+170-cos(a)*170))
                self.canvas.after(int(i/100*1000), lambda a=angle: self.canvas.coords(self.arm[1], *get_rot(217, 28, 230, 210, a),
                                                                                                   *get_rot(220, 23, 230, 210, a),
                                                                                                   *get_rot(226, 24, 230, 210, a),
                                                                                                   *get_rot(235, 43, 230, 210, a),
                                                                                                   *get_rot(225, 47, 230, 210, a)))
        else:
            self.function_off()
            for i in range(30):
                angle = pi/7-pi/7/30*(i+1)
                self.canvas.after(int(i/100*1000), lambda a=angle: self.canvas.coords(self.arm[0], 230, 210, 230-sin(a)*170, 40+170-cos(a)*170))
                self.canvas.after(int(i/100*1000), lambda a=angle: self.canvas.coords(self.arm[1], *get_rot(217, 28, 230, 210, a),
                                                                                                   *get_rot(220, 23, 230, 210, a),
                                                                                                   *get_rot(226, 24, 230, 210, a),
                                                                                                   *get_rot(235, 43, 230, 210, a),
                                                                                                   *get_rot(225, 47, 230, 210, a)))

    def destroy(self):
        self.canvas.destroy()