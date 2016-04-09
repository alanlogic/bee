#!/usr/bin/python  
# -*- coding: utf-8 -*-
#find resource is an egg-pain thing,so...
#A program let you download what you want
#movies,musics,softwares and so on

import tkinter as tk

import spider
import gui

root = tk.Tk()
root.title("Download Dict")
app = gui._Application(master=root)
app.mainloop()