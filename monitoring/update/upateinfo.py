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


class UpdateInfo(object):
	public = {}
	registered_ = {}
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
	path = os.path.dirname(sys.argv[0])+'/'
	def __init__(self):
		self.local = threading.local() 
		self.config()
		

	
	def config(self):
		try:
			database = {}
			configs = {'config':[]}
			with open(self.path+'config.ini','r',encoding='utf8') as f:
				for line in f.readlines():
					line = line.strip()#去除两段空字符
					#如果为空或者为注释跳过
					if len(line) < 1 or line[0] == '#':
						continue
					#配置文件类型
					if line[0] == '[' and line[-1] == ']':
						class_ = line[1:-1]

					#数据库
					if '=' in line and class_ == 'database':
						conf = line.split('=')
						database[conf[0].strip()] = conf[1].strip()
					#公共
					if '=' in line and class_ == 'public':
						conf = line.split('=')
						self.public[conf[0].strip()] = conf[1].strip()
					#注册配置
					if '=' in line and class_ == 'registered':
						conf2 = line.split('=')
						self.registered_[conf2[0].strip()] = conf2[1].strip()

		except Exception as e:
			# print(e)
			print('配置文件错误')
			exit()
		
		
		

	def login(self,url):
		print(url)
		try:
			url_ = 'http://'+url.replace('.json','')
			cookiefile = 'cookies/'+url
			if os.path.exists(cookiefile):
				options = webdriver.ChromeOptions()
				prefs = {
				    'profile.default_content_setting_values': {
				        'images': 2
				    }
				}
				options.add_experimental_option('prefs', prefs)
				# browser = webdriver.Chrome()#声明一个浏览器对象
				browser = webdriver.Chrome()#声明一个浏览器对象

				browser.get(url_)
				# 删除第一次建立连接时的cookie
				browser.delete_all_cookies()
				# 读取登录时存储到本地的cookie
				with open(cookiefile, 'r', encoding='utf8') as f:
					listCookies = json.loads(f.read())
					# print(listCookies)

				for cookie in listCookies:
					try:
					    browser.add_cookie({
					        'domain': cookie.get('domain'),  # 此处xxx.com前，需要带点
					        'name': cookie.get('name'),
					        'value': cookie.get('value'),
					        'path': '/',
					        'expires': None
					    })
					except Exception as e:
						# print(e)
							pass
			# time.sleep(50)
			# browser.quit()
			# sys.exit()
		except Exception as e:
			pass
		self.updatedata(browser,url_)
		

	def	updatedata(self,browser,url):



		#个人主页
		try:
			browser.get(url+'/home.php?mod=spacecp&ac=profile&op=info')
			site = browser.find_element(By.CSS_SELECTOR,"input[name='site']")
			site.clear()
			site.send_keys(self.registered_['site'])
			
		except Exception as e:
			pass
			print(e,1)
		
		#个人签名 sightml
		try:
			site = browser.find_element(By.CSS_SELECTOR,"textarea[name='sightml']")
			site.clear()
			site.send_keys(self.registered_['sightml'])
		except Exception as e:
			print(e,2)
			pass

		#自我介绍 bio
		try:
			site = browser.find_element(By.CSS_SELECTOR,"textarea[name='bio']")
			site.clear()
			site.send_keys(self.registered_['bio'])
		except Exception as e:
			print(e,3)
			pass
			
		#兴趣爱好 interest
		try:
			site = browser.find_element(By.CSS_SELECTOR,"textarea[name='interest']")
			site.clear()
			site.send_keys(self.registered_['interest'])
		except Exception as e:
			print(e,4)
			pass


		try:
			profilesubmitbtn = browser.find_element(By.CSS_SELECTOR,"button[name='profilesubmitbtn']")
			profilesubmitbtn.click()
		except Exception as e:
			pass

		# time.sleep(5000)
		browser.quit()
		sys.exit()


		

	def main(self):

		filelist = os.listdir('cookies/')
		for url in filelist:
			if threading.active_count() < 5:
				
				w = threading.Thread(target=self.login,args=(url,))
				w.start()
			else:
				print('等待其他操作完成')
				time.sleep(5)


if __name__ == '__main__':
	UpdateInfo().main()