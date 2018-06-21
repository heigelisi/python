from selenium import webdriver
from selenium.webdriver.common.by import By #
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import time
import threading
import re
import json
import os
import requests
import pymysql
import config
AccessToken = None
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}

class GetEmailData(object):
	"""docstring for GetEmailData"""
	def __init__(self):
		# super(GetEmailData, self).__init__()
		pass	
		self.local = threading.local()	

	def login(self,username,password,password2):
		"""登陆qq邮箱"""
		try:
			self.local.username = username
			self.local.password = password
			self.local.password2 = password2
			browser = webdriver.Chrome()#声明一个浏览器对象
			browser.maximize_window()

			browser.get('https://mail.qq.com/')
			cookiefile = username.replace('@qq.com','')+'.json'
			cookielogin = None
			if os.path.exists(cookiefile):
				#使用cookie登陆
				# 删除第一次建立连接时的cookie
				browser.delete_all_cookies()
				# 读取登录时存储到本地的cookie
				with open(cookiefile, 'r', encoding='utf8') as f:
					listCookies = json.loads(f.read())

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
						print(e)
				browser.get('https://mail.qq.com/')
				time.sleep(10)

			#判断是否登陆成功
			toptitle = ''
			try:
				toptitle = browser.find_element(By.CSS_SELECTOR,'.toptitle').get_attribute('textContent')
				cookielogin = 1
			except Exception as e:
				pass

			#使用账号密码登陆
			if not cookielogin:
				#点击账号登陆按钮
				wait = WebDriverWait(browser,20)
				browser.switch_to.frame('login_frame')#切换到一个iframe页面
				switch_btn = browser.find_element(By.CSS_SELECTOR,'#switcher_plogin')
				switch_btn.click()
				#输入用户名密码
				username = username.strip()
				password = password.strip()
				password2 = password2.strip()

				u = browser.find_element(By.CSS_SELECTOR,'#u')
				u.clear()
				u.send_keys(username)
				p = browser.find_element(By.CSS_SELECTOR,'#p')
				p.clear()
				p.send_keys(password)
				#点击登陆
				login_button = browser.find_element(By.CSS_SELECTOR,'#login_button')
				login_button.click()
				# browser.switch_to.default_content()
				time.sleep(30)
				#是否有独立密码
				try:
					pp = browser.find_element(By.CSS_SELECTOR,'#pp')
					pp.send_keys(password2)
					#点击登陆
					login_button = browser.find_element(By.CSS_SELECTOR,'#btlogin')
					login_button.clear()
					login_button.click()
				except Exception as e:
					pass
				time.sleep(3)

			#判断是否登陆成功
			#判断是否登陆成功
			toptitle = ''
			try:
				toptitle = browser.find_element(By.CSS_SELECTOR,'.toptitle').get_attribute('textContent')
			except Exception as e:
				pass
			if toptitle:
				dictCookies = browser.get_cookies()
				jsonCookies = json.dumps(dictCookies)
				# 登录完成后，将cookie保存到本地文件
				with open(cookiefile, 'w') as f:
				    f.write(jsonCookies)
				print(username,'登陆成功')
				#执行获取邮件
				self.getData(browser)

			else:
				print(username,'登陆失败')

		except Exception as e:
			print('login',e)
			pass
		




	def getData(self,browser):
		'''获取邮件列表'''
		url = browser.current_url
		while 1:
			windows = browser.window_handles
			browser.switch_to.window(windows[0])
			try:
				#点击收件箱按钮
				browser.get(url)
				#判断是否掉线
				try:
					toptitle = browser.find_element(By.CSS_SELECTOR,'.toptitle').get_attribute('textContent')
				except Exception as e:
					# 已经掉线 推出
					browser.quit()
					self.login(self.local.username,self.local.password,self.local.password2)
					# 记录推出
					# with open('loginerror.log','a',encoding='utf8') as fff:
					# 	fff.write()
					# print(self.local.username,self.local.password,self.local.password2)
					# self.login(self.local.username,self.local.password,self.local.password2,1)

				folder_1 = browser.find_element(By.CSS_SELECTOR,'#folder_1')
				folder_1.click()

				#切换到未读邮件列表按钮frame
				browser.switch_to.frame('mainFrame')

				#点击未读邮件列表按钮
				# green = browser.find_element(By.CSS_SELECTOR,'.green')
				# green.click()

				#滚动页面到底部
				browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
				#查找文件列表
				# ur_l_item = browser.find_elements(By.CSS_SELECTOR,'.ur_l_item')
				# trs = browser.find_elements(By.CSS_SELECTOR,'tr')

				for p in range(config.c['page']):
					#点击下一页
					if p > 0:
						print('第',p,'次')
						try:
							wait = WebDriverWait(browser,10)
							inputs = wait.until(EC.presence_of_element_located((By.ID,'nextpage1')))
							nextpage1 = browser.find_element(By.CSS_SELECTOR,'#nextpage1')
							nextpage1.click()
						except Exception as e:
							print(e)
							continue

					#查找所有新窗口读信按钮
					cir = []
					try:
						wait = WebDriverWait(browser,10)
						inputs = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'tr > td.ci > div.cir.Ru')))
						cir = browser.find_elements(By.CSS_SELECTOR,'tr > td.ci > div.cir.Ru')
					except Exception as e:
						print('cir',e)
						pass
					print(p,cir)
					for i in cir:
						try:
							print(i.get_attribute('textContent'))
							i.click()
						except Exception as e:
							time.sleep(10)
							continue
							print(e)

				windows = browser.window_handles
				for r in range(1,len(windows)):
					browser.switch_to.window(windows[-r])#切换到新打开的窗口

					#读取邮件数据
					source = self.source(browser)
					if source:
						if source['source'][0] == '前程无忧':
							self._51job_com(browser,source['deliverytime'])
							# print('前程无忧')

						elif source['source'][0] == '赶集':
							self.ganji_com(browser,source['deliverytime'])
							print('赶集')

						elif source['source'][0] == '智联招聘':
							self.zhaopinmail_com(browser,source['deliverytime'])
							print('智联招聘')

						elif source['source'][0] == '58':
							self._58(browser,source['deliverytime'])
							print('58')

						else:
							print('未知来路')


					browser.close()#关闭新窗口
					time.sleep(1)
			except Exception as e:
				print(e)
				time.sleep(10)
				continue
			time.sleep(20)

	def source(self,browser):
		#判断邮件来源
		tipFromAddr_readmail = ''
		deliverytime = ''
		try:
			mainFrame_src = browser.find_element(By.CSS_SELECTOR,'#mainFrame').get_attribute('src')
			browser.get(mainFrame_src)
			try:
				tipFromAddr_readmail = browser.find_element(By.CSS_SELECTOR,'#tipFromAddr_readmail').get_attribute('fromaddr')

				
			except Exception as e:
				tipFromAddr_readmail = browser.find_element(By.CSS_SELECTOR,'#fromaddr').get_attribute('textContent')
			
			try:
				
				deliverytime = browser.find_element(By.CSS_SELECTOR,'#mainmail > div.readmailinfo > table:nth-child(4) > tbody > tr:nth-child(1) > td.settingtable.txt_left > b').get_attribute('textContent')
			except Exception as e:
				pass

		except Exception as e:
			print(e)
			pass
		# print(tipFromAddr_readmail)
		if tipFromAddr_readmail:
			for row in config.recruitmentList:
				if row[1] in tipFromAddr_readmail:
					return {'source':row,'deliverytime':deliverytime}

		# return row


	def _51job_com(self,browser,deliverytime):
		"""解析前程无忧"""
		print('解析前程无忧')
		try:
			
			#姓名
			#年龄
			#性别
			#工作经验年限
			basic = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table[1]/tbody/tr/td[1]').get_attribute('textContent')
			name,sex,age,work = basic.split('|')
			#手机 邮箱
			mobileEmail = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table[2]/tbody/tr/td/table[1]/tbody').get_attribute('textContent')
			# print(type(mobileEmail))
			pattern = re.compile(r'(13[0-9]{9})|(14[579]{9})|(15[0-3,5-9]{9})|(16[6]{9})|(17[0135678]{9})|(18[0-9]{9})|(19[0-9]{9})|(13[0-9]{9})$')
			mobile_ = re.search(pattern,mobileEmail)
			if mobile_:
				phone = mobile_.group().strip()
			else:
				phone = ''
			pattern = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
			mail_ = re.search(pattern,mobileEmail)
			if mail_:
				email = mail_.group().strip()
			else:
				email = ''
			#如果没有手机也没有邮箱这个简历就没有意义了
			if not phone and not email:
				return None


			#居住地
			address = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td[2]').get_attribute('textContent').strip()
			text = browser.find_element(By.CSS_SELECTOR,'#mailContentContainer').get_attribute('textContent')

			try:
				wb = browser.find_element_by_xpath('//*[@id="mainmail"]/div[2]/table[3]/tbody/tr[1]/td[2]/span[1]/a')
				wb.click()
			except Exception as e:
				pass
			# print(text)
			# print(name.strip(),age.strip(),sex.strip(),phone.strip(),email.strip(),address.strip(),'前程无忧',text.strip())
			# exit()
			# print('居住地',address)
			# print(username,sex,age,work,mobile,mail)
			self.setData([name.strip(),age.strip(),sex.strip(),phone.strip(),email.strip(),address.strip(),'前程无忧',text.strip(),deliverytime])


			# #应聘职位
			# position = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[1]/table/tbody/tr/td[2]').get_attribute('textContent')
			# print('应聘职位',position)
			# #应聘公司
			# company = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/table/tbody/tr/td[2]').get_attribute('textContent')
			# print('应聘公司',company)
			# #投递时间
			# time_ = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/span').get_attribute('textContent')
			# print('投递时间',time_)
			

		except Exception as e:
			print(e)
			return None


	def ganji_com(self,browser,deliverytime):
		"""赶集"""
		try:
			print('赶集')
			text = browser.find_element_by_xpath('//*[@id="mailContentContainer"]/table/tbody/tr/td/table[2]/tbody/tr/td/div/table').get_attribute('textContent')
			company = re.compile(r'.*?（.*?）')
			user = re.search(company,text)
			if user:
				user = user.group()
				users = user.split('（')
				name = users[0]
				user2 = users[1].split(' ')
				sex = user2[0]
				age = user2[1].strip('）')

			pattern = re.compile(r'(13[0-9]{9})|(14[579]{9})|(15[0-3,5-9]{9})|(16[6]{9})|(17[0135678]{9})|(18[0-9]{9})|(19[0-9]{9})|(13[0-9]{9})$')
			mobile_ = re.search(pattern,text)
			if mobile_:
				phone = mobile_.group().strip()
			else:
				phone = ''
			pattern = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
			mail_ = re.search(pattern,text)
			if mail_:
				email = mail_.group().strip()
			else:
				email = ''
			#如果没有手机也没有邮箱这个简历就没有意义了
			if not phone and not email:
				return None
			company = re.compile(r'.*?工作地点.*?([\u4e00-\u9fa5]+\s?\-\s?[\u4e00-\u9fa5]+\s?\-\s?[\u4e00-\u9fa5]+).*?',re.S)
			res = re.search(company,text)
			if res:
				address = res.group(1)
			else:
				address = ''
			self.setData([name.strip(),age.strip(),sex.strip(),phone.strip(),email.strip(),address.strip(),'赶集',text.strip(),deliverytime])
		except Exception as e:
			print(e)


	def zhaopinmail_com(self,browser,deliverytime):
		try:
			"""智联招聘"""
			print('智联招聘')
			text = browser.find_element(By.CSS_SELECTOR,'#mailContentContainer > table:nth-child(3)').get_attribute('innerHTML')
			#基本资料
			company = re.compile(r'.*?<td>.*?line-height:50px">(.*?)</td>.*?style="font-weight:bold">([男|女])</font>.*?weight:bold">([0-9]+年[0-9]+月)</font><br>(.*?)<small.*?href="(https://ihr\.zhaopin\.com.*?)".*?',re.S)
			strs = ''
			for r in text.split():
				if r:
					strs += r
			jiben = re.search(company,strs)
			if jiben:
				name = jiben.group(1)
				sex = jiben.group(2)
				age = jiben.group(3)
				address = jiben.group(4)
				url = jiben.group(5)
			else:
				return False

			#联系方式
			try:
				import urllib
				from urllib.parse import parse_qs
				query = urllib.parse.urlparse(url).query
				param = parse_qs(query)['param'][0]
				url = "https://ihr.zhaopin.com/resumemanage/emailim.do?s="+param
				contact = requests.get(url,headers=headers).text
				contact = json.loads(contact)
				if contact['code'] == 200:
					name = contact['data']['username']
					phone = contact['data']['phone']
					email = contact['data']['email']
				else:
					return False
			except Exception as e:
				print(e)
				return False

			#所有资料
			texts = browser.find_element(By.CSS_SELECTOR,'#mailContentContainer > table:nth-child(3)').get_attribute('textContent')
			self.setData([name.strip(),age.strip(),sex.strip(),phone.strip(),email.strip(),address.strip(),'智联招聘',texts.strip(),deliverytime])
		except Exception as e:
			print(e)

	def _58(self,browser,deliverytime):
		'''58'''
		print(58)
		try:
			position = ''
			try:
				#应聘职位
				position = browser.find_element(By.CSS_SELECTOR,'#mailContentContainer > div > div:nth-child(1) > span > a').get_attribute('textContent')
			except Exception as e:
				pass
			innerHTML = browser.find_element(By.CSS_SELECTOR,'#mailContentContainer > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(2)').get_attribute('innerHTML')
			strs = ''
			for r in innerHTML.split():
			  if r:
			    strs += r
			pattern = re.compile(r'.*?font-weight:normal;">(.*?)<span.*?padding:010px;">（([男|女]，\d+岁)）</span>.*?font-size:20px;">(\d{11})</span>.*?font-size:20px;">(.*?@?.*?)</span>',re.S)
			basic = re.search(pattern,strs)
			if basic:
				name = basic.group(1)
				sex,age = basic.group(2).split('，')
				phone = basic.group(3)
				email = basic.group(4)
				address = ''
				texts = browser.find_element(By.CSS_SELECTOR,'#mailContentContainer > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(2)').get_attribute('textContent')
				texts = "应聘职位："+position+'|'+texts
				self.setData([name.strip(),age.strip(),sex.strip(),phone.strip(),email.strip(),address.strip(),'58',texts.strip(),deliverytime])
			else:
				return False
		except Exception as e:
			print(e)
			return False

	def setData(self,data):
		print(data)
		try:
			# data[1] = re.findall(r'\d+',data[1])[0]
			connect = pymysql.connect(host=config.database['host'],user=config.database['user'],passwd=config.database['passwd'],db=config.database['db'],charset=config.database['charset'],port=int(config.database['port']));#链接数据库
			cursor = connect.cursor();#创建一个游标
			#生成用户唯一表示
			import hashlib
			validation = data[0]+data[1]+data[2]+data[3]+data[4]
			validation2 = hashlib.md5(validation.encode('utf-8')).hexdigest()
			data.append(validation2)
			#查询是否已经存在
			sql = "select id from info where validation = '%s' limit 1"%validation2
			res1 = cursor.execute(sql)
			if res1:
				connect.close()
				return False
			#转换成localtime
			timestamp = int(time.time())
			time_local = time.localtime(timestamp)
			#转换成新的时间格式(2016-05-05 20:28:54)
			dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
			data.append(dt)
			data.append(self.local.username)
			insert = "insert into info(username,age,sex,phone,email,address,source,texts,deliverytime,validation,addtime,froms) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			res = cursor.execute(insert,(data))
			if res:
				connect.commit()
			connect.close()
		except Exception as e:
			print('setData',e)
			try:
				connect.close()
			except Exception as e:
				pass
			time.sleep(3)
			self.setData(data)

	def setDataEC(self):
		""""""
		while True:
			try:
				file = 'static/id.txt'
				id_ = 0
				if os.path.exists(file):
					with open(file,'r',encoding='utf8') as f:
						id_f = f.read()
						if id_f:
							id_ = id_f.strip()


				sql = 'select username,age,sex,phone,email,address,source,texts,id,froms,deliverytime from info where id > %s limit 100'%(str(id_))
				connect = pymysql.connect(host=config.database['host'],user=config.database['user'],passwd=config.database['passwd'],db=config.database['db'],charset=config.database['charset'],port=int(config.database['port']));#链接数据库
				cursor = connect.cursor();#创建一个游标
				cursor.execute(sql)
				data = cursor.fetchall()
				if not data:
					continue
				# if data:
				# 	#获取EC accessToken
				# 	headers = {'cache-control':'no-cache','content-type':'application/json'}
				# 	data_ = json.dumps({'appId':342620696708382720,'appSecret':'OhPE5SGH9ygLUwIlglA'})
				# 	url = 'https://open.workec.com/auth/accesstoken'
				# 	accessToken = json.loads(requests.post(url,headers=headers,data=data_).text)
				# 	if accessToken['errCode'] == 200:
				# 		accesstoken = accessToken['data']['accessToken']

				
				if AccessToken:
					for r in data:
						id_ = r[8]
						birthday = None
						# birthday = '2018/5/31'
						sex = r[2].strip() or '0'
						phone = r[3].strip()
						email = r[4].strip()
						address = r[5].strip() or '无'
						source = r[6].strip() or '无'
						if r[7]:
							text =re.split(r'\s+',r[7])  
							strs = '|'.join(text)
							strs = strs.replace('：|','：')
							f_memo = strs[0:490]
							f_memo2 = strs[490:1480]
							f_memo3 = strs[1480:2470]
							f_memo4 = strs[2470:3460]
						else:
							f_memo = ''
							f_memo2 = ''
							f_memo3 = ''
							f_memo4 = ''

						

						#处理生日
						age = None
						#获取当前的年份
						#转换成localtime
						timestamp = int(time.time())
						time_local = time.localtime(timestamp)
						#转换成新的时间格式(2016-05-05 20:28:54)
						y_ = int(time.strftime("%Y",time_local))
						pattern = re.compile(r'.*?(\d+)\s?年(\d+)\s?月.*?',re.S)
						age = re.search(pattern,r[1])
						if age:
							birthday = age.group(1)+'/'+age.group(2)+'/30'
							age_ = int(y_) - int(age.group(1))

						if not birthday:
							pattern = re.compile(r'.*?(\d+/\d+/\d{0,2}).*?',re.S)
							age = re.search(pattern,r[1])
							if age:
								birthday = age.group(1)
								#提取年份
								pattern = re.compile(r'.*?(\d+)/(\d+)/\d{0,2}.*?',re.S)
								y_1 = re.search(pattern,birthday)
								age_ = int(y_) - int(y_1.group(1))

						if not birthday:
							pattern = re.compile(r'.*?(\d+\s?)岁.*?',re.S)
							age2 = re.search(pattern,r[1])
							if age2:
								age3 = int(age2.group(1))
								
								y = y_ - age3
								birthday = str(y)+'/12/30'
								age_ = age3

						# 过滤年龄 男：18-35 女：18:30
						if sex == '男':
							if age_ < 18 or age_ > 35:
								continue
						if sex == '女':
							if age_ < 18 or age_ > 30:
								continue

						if not birthday:
							birthday = '2018/5/31'
						# 5698609
						followUserId = '7508618'
						for c in config.emails:
							if c[0] == r[9]:
								followUserId = c[3]

						data_ = {
								    "optUserId":7508618,
								    # "groupId":5698611,
								    "followUserId":followUserId,
								    "f_name": r[0],
								    "f_birthday": birthday,
								    "f_title": r[9].replace('@qq.com',''),
								    "f_company":r[10],
								    # "f_mobile": phone,
								    "f_company_addr": address,
								    "f_memo": f_memo,
								    "f_gender": sex,
								    "f_channel": source,
								    "81116447":f_memo2,
								    "81127941":f_memo3,
								    "81127942":f_memo4,
								    "customFieldMapping": {
							        "81116447": {
							            "option_id": "",
							            "type": "1"
							        },
							        "81127941":{
							            "option_id": "",
							            "type": "1"
							        },
							        "81127942": {
							            "option_id": "",
							            "type": "1"
							        }
							    	}
								}
						if email:
							data_['f_email'] = email
						if phone:
							data_['f_mobile'] = phone
						data_ = json.dumps(data_)
						url = 'https://open.workec.com/customer/addCustomer'
						headers = {'authorization':AccessToken,'corp_id':'5698610','cache-control':'no-http://xiaorui.cc/page/2/','content-type':'application/json'}
						res = requests.post(url,headers=headers,data=data_).text
						resjson = json.loads(res)
						if resjson['errCode'] == 200:
							#写入EC成功 记录
							#转换成localtime
							timestamp = int(time.time())
							time_local = time.localtime(timestamp)
							#转换成新的时间格式(2016-05-05 20:28:54)
							dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
							self.statistical(id_,dt)

						resmsg = res+'录入客户：'+r[0]+phone
						print(resmsg)
						with open('static/log.log','a',encoding='utf8') as f2:
							f2.write(resmsg+'\r\n')

				else:
					continue

			except Exception as e:
				print('setDataEC',e)
				pass
			try:
				connect.close()
			except Exception as e:
				pass
			with open(file,'w',encoding='utf8') as f3:
				f3.write(str(id_))
			time.sleep(60)

	def cacheaccesstoken(self):
		while True:
			try:
				headers = {'cache-control':'no-cache','content-type':'application/json'}
				data_ = json.dumps({'appId':342620696708382720,'appSecret':'OhPE5SGH9ygLUwIlglA'})
				url = 'https://open.workec.com/auth/accesstoken'
				accessToken = json.loads(requests.post(url,headers=headers,data=data_).text)
				if accessToken['errCode'] == 200:
					global AccessToken
					AccessToken = accessToken['data']['accessToken']
					print(AccessToken)
				time.sleep(7000)
			except Exception as e:
				time.sleep(3)
				print('cacheaccesstoken',e)


	def statistical(self,infoid,datatime):
		"""统计入库EC数据"""
		while True:
			try:
				connect = pymysql.connect(host=config.database['host'],user=config.database['user'],passwd=config.database['passwd'],db=config.database['db'],charset=config.database['charset'],port=int(config.database['port']));#链接数据库
				cursor = connect.cursor();#创建一个游标
				sql = "insert into statistical(info_id,addtime) values(%s,%s)"
				res = cursor.execute(sql,([str(infoid),datatime]))
				if res:
					connect.commit()
				connect.close()
				break
			except Exception as e:
				print(e)
				try:
					connect.close()
				except Exception as e:
					pass
				time.sleep(3)
				self.statistical(infoid,datatime)


	# def froms(self):


	def main(self):
		w2 = threading.Thread(target=self.cacheaccesstoken)
		w2.start()
		w = threading.Thread(target=self.setDataEC)
		w.start()
		for row in config.emails:
			print(row)
			w = threading.Thread(target=self.login,args=(row[0],row[1],row[2],))
			w.start()

if __name__ == '__main__':
	GetEmailData().main()

