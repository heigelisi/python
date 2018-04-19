

from selenium import webdriver
from selenium.webdriver.common.by import By #
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import time
import threading
import os
import json
import sys
import tkinter
from PIL import Image as MyImages, ImageTk
import re
import tkinter
import wmi
import requests
import pyquery
from multiprocessing import Process
import random
import queue
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}


class load(object):


	def __init__(self,url):
		self.url = url

	def html(self):
		urls = self.url.split('/')
		url = urls[0]+'//'+urls[2]
		urllist = []
		browser = webdriver.PhantomJS()#声明一个浏览器对象
		browser.get(self.url)
		browser.implicitly_wait(6)  
		html = browser.page_source.encode().decode('utf8')
		for image in browser.find_elements_by_tag_name("img"):  
		    imgsrc = image.get_attribute('src').strip()
		    print(imgsrc)
		    houzui = imgsrc[-4:]
		    if houzui != '.png' and houzui != '.gif' and houzui != 'jpeg' and houzui != '.jpg' and houzui != '.ico':
		    	continue
		    response = requests.get(imgsrc)
		    imgname = imgsrc.split('/')[-1]
		    html = html.replace(imgsrc.replace(url,''),'images/'+imgname)
		    with open('images/'+imgname,'wb') as f:
		    	f.write(response.content)
		    	f.close()
		for link in browser.find_elements_by_tag_name("link"):  
		    linkhref = link.get_attribute('href').strip()
		    if not linkhref:
		    	continue
		    print(linkhref)
		    response = requests.get(linkhref)
		    linkhref = linkhref.split('?')[0]
		    css = linkhref.split('/')[-1]
		    html = html.replace(linkhref.replace(url,''),'css/'+css)
		    with open('css/'+css,'wb') as f:
		    	f.write(response.content)
		    	f.close()

		for script in browser.find_elements_by_tag_name("script"):  
		    scriptsrc = script.get_attribute('src')
		    if not scriptsrc:
		    	continue
		    else:
		    	scriptsrc = scriptsrc.strip()
		    print(scriptsrc)
		    response = requests.get(scriptsrc)
		    scriptsrc = scriptsrc.split('?')[0]
		    scripts = scriptsrc.split('/')[-1]
		    html = html.replace(scriptsrc.replace(url,''),'js/'+scripts)
		    with open('js/'+scripts,'wb') as f:
		    	f.write(response.content)
		    	f.close()

		print(urllist)
		html = browser.page_source.encode().decode('utf8')
		f = open('index.html','w',encoding='utf8')
		f.write(html)

	def cssloadimg(self):
		imglist = []
		browser = webdriver.PhantomJS()#声明一个浏览器对象
		dirlist = os.listdir('css')
		for r in dirlist:
			print(r)
			browser.get('file:///F:\\PHP\\python\\monitoring\\loadimage\\css\\'+r)
			html = browser.page_source.encode().decode('utf8')
			print(html)
				# file = f.read()
			pattern = re.compile(r'''.*?url\('(.*?)'\).*?''',re.S)
			imglist += list(set(re.findall(pattern,html)))
		ff = open('csslist.txt','a',encoding='utf8')
		for i in imglist:
			ff.write(i+'\r\n')



if __name__ == '__main__':
	load('http://678v.cc/index/real.do').html()


