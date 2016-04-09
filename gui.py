#!/usr/bin/python  
# -*- coding: utf-8 -*-

import tkinter as tk
import urllib.parse
from functools import partial

import spider
import sorter

class _Application(tk.Frame):


    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.l_texts = []
        self.buttons = []
        self.create_widgets()
        self.spider = spider._MusicSpider()
        self.sorter = sorter.Sorter()
        self.answer = []

    #create the widgets whick are needed
    def create_widgets(self):
        self.create_search()
        self.create_label()
        self.create_text()
    
    #the widget of search
    def create_search(self):
        self.s_panel = tk.Frame(master=self)
        self.s_panel.pack()

        self.search = tk.Button(self.s_panel,text="Search",command=self.search)
        self.search.pack(side='right')

        self.contents = tk.StringVar()
        self.contents.set("输入关键词以搜索")
        self.s_box = tk.Entry(self.s_panel,textvariable=self.contents)
        self.s_box.pack(side='left')
        
    #the widget display the result
    def create_label(self):
        self.result = tk.Frame(master=self)
        self.result.pack()
        for i in range(10):
            panel = tk.Frame(master=self.result, width=100)
            panel.pack()
            v = tk.StringVar()
            l = tk.Label(master=panel, textvariable=v, width=90)
            self.l_texts.append(v)
            l.pack(side='left')
            b = tk.Button(master=panel, text='下载', width=10)
            self.buttons.append(b)

    def create_text(self):
        self.link_t = tk.Text(master=self)
        self.back = tk.Button(master=self,command=self.go_back,text='后退')

    def go_back(self):
        self.link_t.forget()
        self.back.forget()
        self.result.pack()
                                         
    #for button when is clicked
    def search(self):
        self.go_back()
        target = self.spider.search(self.contents.get())
        self.sorter.initial(target,self.spider.websites)
        self.answer = self.sorter.by_rank_all()
        self.update()
        
    def update(self):
        if (len(self.answer) >= 10):
            self.u_texts(10)
            self.u_buttons(10)
        else:
            self.u_texts(len(self.answer))
            self.u_buttons(len(self.answer))

    #use text to fresh content
    def u_texts(self,length):
            for i in range(length):
                self.l_texts[i].set(self.answer[i][1])
    
    def u_buttons(self,length):
        for i in range(length):
            full_url = str(self.answer[i][2]) + str(self.answer[i][0])
            self.buttons[i].config(command=partial(self.get_links,full_url))
            self.buttons[i].pack(side='right')
        if length<10:
            for i in range(length,10):
                self.buttons[i].forget()
            
    def get_links(self,address):
        links = self.spider.get_links(address)
        self.result.forget()
        self.link_t.delete(1.0,tk.END)
        for link in links:
            self.link_t.insert(tk.END,'%s\n'%link)
        self.go_front()
        
    def go_front(self):
        self.result.forget()
        self.link_t.pack()
        self.back.pack(side='bottom')




    


    