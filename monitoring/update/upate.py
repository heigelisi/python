import time
import threading
import os
import json
import sys
import re
import requests
import pyquery
import random
import queue
import random
from xml.sax.saxutils import unescape
import uuid
import platform


class Update(object):
	

	def login(self,url):
		print(url)
		time.sleep(3)
	# 	self.local.url = url
	# 	# self.local.username = username
	# 	# self.local.password = password
	# 	self.local.msg = msg
	# 	self.local.conn = requests.Session()
	# 	filejson = self.path+'cookies/'+url.replace('http://','').replace('https://','')+'.json'
	# 	if os.path.exists(filejson):
	# 		try:
	# 			with open(filejson, 'r', encoding='utf8') as f:
	# 				listCookies = json.loads(f.read())
	# 		except Exception as e:
	# 			self.showErrorMsg(cookielog,url+"\tcookie文件格式错误\r")

	# 		#添加cookie(登陆操作)
	# 		try:
	# 			for cookie in listCookies:
	# 				self.local.conn.cookies.set(cookie.get('name'),cookie.get('value'))
	# 		except Exception as e:
	# 			# print(e)
	# 			self.showErrorMsg(cookielog,url+"\tcookie设置错误，请更换cookie文件\r")

	# 		#看看是否登陆成功
	# 		try:
	# 			getlogin = self.local.conn.get(url+'/member.php?mod=logging&action=login',headers=self.headers)
				
	# 		except Exception as e:
	# 			self.showErrorMsg(loginerror,url+"\t此网站无法正常访问\r")


	# 		if getlogin.status_code != 200:
	# 			self.showErrorMsg(loginerror,url+"\t访问出错,错误状态码："+str(getlogin.status_code)+"\r")

	# 		q = pyquery.PyQuery(getlogin.text)
	# 		usernamestr = q("input[name='username']")
	# 		self.local.encodeing = requests.utils.get_encodings_from_content(getlogin.text)[0]#编码方式
	# 		self.local.formhash = q("input[name='formhash']").val()#验证字符串
	# 		if not usernamestr:
	# 			self.local.log = open(self.path+'log/'+url.replace('http://','').replace('https://','')+'.log','a',encoding='utf8')
	# 			self.local.log.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+"\r")
	# 			self.showSuccessMsg(url+"\t登陆成功\r")
	# 			# cookie_ = []
	# 			# for cook in getlogin.cookies:
	# 			# 	cookie_.append({'name':cook.name,'value':cook.value})
	# 			# if cookie_:
	# 			# 	with open(filejson, 'w', encoding='utf8') as f:
	# 			# 		f.write(str(cookie_))
	# 			#执行
	# 			self.monitoring()

	# 		else:
	# 			self.showErrorMsg(loginerror,url+"\t登陆失败\r")
	# 	else:
	# 		self.showErrorMsg(cookielog,url+"\tcookie文件不存在\t"+filejson+"\r")

	def main(self):

		filelist = os.listdir('cookies/')
		for i in filelist:
			if threading.active_count() < 3:
				url = 'http://'+i
				w = threading.Thread(target=self.login,args=(url,))
				w.start()
			else:
				print('等待其他操作完成')
				time.sleep(5)


if __name__ == '__main__':
	Update.main()