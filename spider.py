#!/usr/bin/python  
# -*- coding: utf-8 -*-

from threading import Thread
import tkinter as tk
from urllib import parse,request
import json
import re
       
class _MusicSpider:


    def __init__(self):
        self.websites = []
        self.fill()
        self.pages={}
          
    #use the file 'websites.txt' to fill the self.websites            
    def fill(self):
        with open('websites.json','r') as sites:
            str = sites.read()
            self.websites = json.loads(str)
    
    #seach the website from the list to get result about the keyword
    def search(self,keyword):
        self.getcontent(keyword)  
        c_items = {}
        for site in self.websites:
            if site['name'] not in self.pages:
                continue;
            target = self.pages[site['name']]
            items = re.findall(r"<a.*?href=['\"](%s[^>]*?\d{3,10}.html)['\"](.*?>.*?%s.*?)</a>"%(site['key'],keyword), target, re.S)
            mainurl = site['mainUrl'],
            newitems = list(map(lambda item : item + mainurl,items))
            c_items[site['name']] = newitems
        return c_items

    #create some thread to get the page more efficiently
    def getcontent(self,keyword):
        t_pool=[]
        for site in self.websites:
            search_url = site["query"] + parse.quote(keyword,encoding=site["encode"])
            t = Thread(target=self.get_page,args=(search_url,site['name'],site['encode']))
            t.start()
            t_pool.append(t)
        for thread in t_pool:
            thread.join(timeout=5)
    
    def get_page(self,url,key,encode):
        page = self.scratch(url,encode)
        self.pages[key] = page

    #to get objects from website whick address is url  
    def scratch(self,url,encode='utf-8'):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent':user_agent}
        req = request.Request(url,headers=headers)
        result = request.urlopen(req)
        page = result.read()
        u_page = page.decode(encode,errors="ignore")
        result.close()
        return u_page
        
    #get download link from file_url
    def get_links(self,file_url):
        target = self.scratch(file_url)
        links = []
        mag_url = re.findall(r'magnet:\?[^\'"<]+',target,re.S)
        links += mag_url
        ed2k_url = re.findall(r'ed2k://\|[^\'"<]+',target,re.S)
        links += ed2k_url
        ftp_url = re.findall(r'ftp://[^\'"<]+',target,re.S)
        links += ftp_url
        return set(links)