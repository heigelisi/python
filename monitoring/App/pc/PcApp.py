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
from PIL import Image as MyImages, ImageTk
import re
import tkinter
from tkinter import messagebox
from tkinter import ttk
import wmi
import requests
import random
import platform
import uuid
import math

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
sysstr = platform.system()
idstr = str(uuid.uuid1()).split("-")[4]
connect = requests.Session()
stop = False
file = os.path.basename(__file__)

def warningError(type_,msg):
	try:
		if type_ == 'Warning':
			messagebox.showwarning('Warning',msg)
		else:
			messagebox.showerror('Error',msg)
			stop = True
			# time.sleep(10)
			os.popen("taskkill /F /im %s*"%(file.split('.')[0]))
			os.popen("taskkill /F /im chrome*")
			exit()
	except Exception as e:
		# print(e)
		pass




class PcAPP(object):
	path = os.path.dirname(sys.argv[0])+'/'
	info = 0
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title('VIP分享')#设置title
		self.root.iconbitmap(self.path+'static/ico.ico')
		w,h = self.root.maxsize()
		self.w = w
		self.h = h

		# self.root.geometry('1000x800')#设置窗口大小和位置
		self.root.geometry("{}x{}+0+0".format(w, h)) 
	def __del__(self):
		try:
			os.popen("taskkill /F /im chrome*")
		except Exception as e:
			pass

	def nav(self):
		"""导航"""

		try:
			htmlobj = connect.get('http://www.xkx7.cc/app/index/nav',headers=headers,timeout=30)
			navs = json.loads(htmlobj.text)
			if htmlobj.status_code != 200 or int(navs['res']) == 0:
				warningError('Error','登录超时请重新登录!')

		except Exception as e:
			# print(e,1)
			warningError('Error','网络是否有点问题!')
			
		self.navlist = navs['data']
		self.foreachnav(self.navlist)


	def func(self,event):
		try:
			compile_ = re.compile(r'.*?(button\d+)',re.S)
			button_ = compile_.findall(str(event.widget))[0]
			compile_2 = re.compile(r'.*?(\d+)',re.S)
			type_ = int(compile_2.findall(button_)[0])
		except Exception as e:
			type_ = 1
			pass
		self.foreachnav(self.navlist,int(type_)-1)
		self.infolist(int(type_)-1,1)
				
		
	def foreachnav(self,data,typeid=0):
		try:
			self.navfrm.destroy()
			self.navfrm = tkinter.Frame(self.root)
		except Exception as e:
			pass
		nav = tkinter.Frame(self.navfrm,bg='pink',width=2000,height=30,relief="solid", borderwidth=1)
		ii = 0
		for v in data:
			fg = '#000'
			if ii == typeid:
				fg = '#f00'
			button = tkinter.Button(nav, text=v,font=("",14),fg=fg)
			button.bind('<Button-1>',self.func)
			button.pack(side=tkinter.LEFT,padx=5)
			ii += 1
		nav.pack()
		self.navfrm.pack()



	def infolist(self,typeid=0,p=1):
		try:
			#正在加载
			# load = MyImages.open(self.path+r'static/qrcode.png')
			# pic = ImageTk.PhotoImage(load)
			# label = tkinter.Label(self.root,image=pic)
			# label.pack()  #place
			# load = MyImages.open(self.path+'static/load.gif')
			# pic = ImageTk.PhotoImage(load)
			# label = tkinter.Label(self.root,image=pic,width=30,height=30)
			# label.place(x=0,y=0)
			pass

		except Exception as e:
			# print(e)
			pass

		#每页显示条数
		pagenum = int(self.h / 100)
		try:
			#更新数据
			self.frm.destroy()
			self.frm = tkinter.Frame(self.root,height=0.5)
		except Exception as e:
			pass
						
		while True:
			try:
				htmlobj = connect.get('http://www.xkx7.cc/app/index/index?type='+str(typeid)+'&pagenum='+str(pagenum)+'&page='+str(p),headers=headers,timeout=30)
				# print('http://www.xkx7.cc/app/index/index?type='+str(typeid)+'&pagenum='+str(pagenum)+'&page='+str(p))
				data = json.loads(htmlobj.text)
				if htmlobj.status_code != 200 or int(data['res']) == 0:
					warningError('Error','登录超时请重新登录!')
					
				break
			except Exception as e:
				# print(e,2)
				warningError('Error','网络是否有点问题!')
				

		def handlerAdaptor(fun, **kwds):  
			'''''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''  
			return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)  

		def alert():
			if userdata['userlevel'] > 1:
				msg = '您没有此网站的权限，请联系管理员升级会员！'
			else:
				msg = '请开通会员后查看！'
			warningError('Warning',msg)

		def func2(event,**kwds):
			# print(event.widget)
			try:
				print(e1.get())
				print(eval('%s'%kwds['e']).get())
				# kwds['e'].set('正在登录')
				# time.sleep(3)
				# kwds['e'].set('一键登录')
				print(locals())
				print(vars())

			except Exception as e:
				print(e)
				pass

		iii = 1
		for row in data['data']:
			price = ''
			if row['price']:
				price = "(原站价格：%s元)"%row['price']
			info = tkinter.Frame(self.frm,height=10,relief="solid", borderwidth=1,padx=3)
			btn1 = tkinter.Label(info,text=row['title']+price,height=2,width=110,justify='left',anchor='w',font=("",14))
			btn1.grid(row=0,column=0)

			#判断是否有权限查看
			site = []
			if userdata['appsite']:
				site = userdata['appsite'].split(',')
			if (int(row['permissions']) == 0 or int(row['permissions']) > int(userdata['userlevel']) or int(row['status']) == 0) and str(row['infoid']) not in site:
				btn2 = tkinter.Button(info, text='一键登录',height=1,fg='#f00',bg="#3BADF3",font=("",14),command=alert)
			else:
				# exec('e%d = tkinter.Variable()'%iii)
				# eval('e%d'%iii).set('一键登录')
				btn2 = tkinter.Button(info,text="一键登录",height=1,fg='#fff',bg="#3BADF3",font=("",14))
				btn2.bind('<Button-1>',handlerAdaptor(self.login, url=row['url']),)
				# btn2.bind("<ButtonRelease-1>", handlerAdaptor(func2,e='e%d'%iii))
			iii += 1
			btn2.grid(row=0,column=1)
			if row['des']:
				btn3 = tkinter.Label(info,text=row['des'],width=123,anchor='w',wraplength=1200,justify='left',font=("",13),pady=2)
				btn3.grid(row=1,column=0)
			info.pack(pady=2)


		#分页
		pagecount = math.ceil(data['count'] / pagenum)#总页数
		if pagecount > 1:
			page = tkinter.Frame(self.frm,height=10,padx=3)
			def pages(event):
				try:
					compile_ = re.compile(r'.*?(button\d+)',re.S)
					page_list = compile_.findall(str(event.widget))[0]
					compile_2 = re.compile(r'.*?(\d+)',re.S)
					page_ = int(compile_2.findall(page_list)[0])
				
				except Exception as e:
					page_ = 1
				self.infolist(typeid,page_)


			for pg in range(1,pagecount+1):

				fg = '#fff'
				if pg == p:
					fg = '#f00'
				pagebutton = tkinter.Button(page, text=pg,height=1,width=2,fg=fg,bg="#3BADF3",font=("",14))
				pagebutton.bind('<Button-1>',pages)
				pagebutton.grid(row=0,column=pg,padx=5)
			page.pack()
		
		self.frm.pack()

	def login_(self,domain,listCookies):
		try:
			ad = connect.get('http://www.xkx7.cc/app/ad',headers=headers).text
		except Exception as e:
			ad = ''
			pass
		# getcookie
		try:
			option = webdriver.ChromeOptions()
			option.add_argument('disable-infobars')
			# option.add_argument('--proxy-server=http://ip:port') 
			# chrome_options.add_argument('--headless')
			# chrome_options.add_argument('--disable-gpu')
			browser = webdriver.Chrome(chrome_options=option)#声明一个浏览器对象
			browser.get('http://'+domain)
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
					pass
			browser.get('http://'+domain)
			browser.maximize_window()
			while True:
				try:
					ad_ = browser.find_element(By.CSS_SELECTOR,"#_ad_")
				except Exception as e:
					browser.execute_script(ad)
				pass
				time.sleep(10)
		except Exception as e:
			pass

	def login(self,event,**kwds):
		domain = kwds['url']
		try:
			cookieobj = connect.get('http://www.xkx7.cc/app/index/getcookie?domain='+domain)
			listCookies = json.loads(cookieobj.text)
		except Exception as e:
			return

		w = threading.Thread(target=self.login_,args=(domain,listCookies))
		w.start()


	def main(self):

		global stop
		self.navfrm = tkinter.Frame(self.root)
		self.nav()
		self.frm = tkinter.Frame(self.root)
		self.frm.pack()
		self.infolist()
		self.root.mainloop()
		pass
		stop = True


if __name__ == '__main__':
	print('请不要关闭此窗口，关闭后程序无法正常运行。')
	def status(username):

		while True:
			if stop:
				sys.exit()
			try:
				status_ = json.loads(connect.get('http://www.xkx7.cc/app/index/status?username='+username).text)
				print('请不要关闭此窗口，关闭后程序无法正常运行。')
				if status_['res'] != 'off':
					os.popen("taskkill /F /im chrome*")
				elif status_['userdata']['pc'] != sysstr+'_'+idstr:
					warningError.showerror('Error','您的帐号在其它地方登录，您已被迫下线，如果不是您本人操作，请及时修改密码！')
					os.popen("taskkill /F /im %s*"%(file.split('.')[0]))
					os.popen("taskkill /F /im chrome*")
				else:
					global userdata
					userdata = status_['userdata']
				time.sleep(10)
			except Exception as e:
				# print(e)
				pass

	def login():

		try:
			dir_ = os.getcwd()
			path = dir_+'/static/'
			# print (os.environ["TEMP"])
			mydir = os.path.normpath(path)
			os.environ["PHANTOMJS"] = mydir
			# print (os.environ["MYDIR"])
			pathV = os.environ["PATH"]
			# print (pathV)
			os.environ["PATH"]= mydir + ";" + os.environ["PATH"]

		except Exception as e:
			pass


		root = tkinter.Tk()
		root.title('VIP分享用户登录')#设置title
		root.iconbitmap(os.path.dirname(sys.argv[0])+'/static/ico.ico')
		w,h = root.maxsize()
		w_ = int((w / 2) -50)
		h_ = int((h / 2) - 50)
		root.geometry('210x100+%s+%s'%(str(w_),str(h_)))#设置窗口大小和位置
		root.resizable(width=False, height=False)

		uname_ = tkinter.Variable()
		uname = tkinter.Label(root,text="用户名：")
		uname.grid(row=0,column=1)
		username = tkinter.Entry(root,textvariable=uname_)
		username.grid(row=0,column=2)

		pname = tkinter.Label(root,text="密码：")
		pname.grid(row=1,column=1)
		password_ = tkinter.Variable()
		password = tkinter.Entry(root,show="*",textvariable=password_)
		password.grid(row=1,column=2)

		def func():
			try:
				uname_var = uname_.get()
				if not uname_var:
					warningError('Warning','用户名不能为空！')
					return
				password_var = password_.get()
				if not password_var:
					warningError('Warning','密码不能为空！')
					return
				data = {'username':uname_var,'passwd':password_var,'equipment':sysstr+'_'+idstr}
				request = connect.post('http://www.xkx7.cc/App/Login/index',headers=headers,data=data)
				if request.status_code == 200:
					res = json.loads(request.text)
					if int(res['res']) == 1:
						root.destroy()

						#监控用户状态
						w = threading.Thread(target=status,args=(uname_var,))
						w.start()
						global userdata
						userdata = res['userdata']
						PcAPP().main()
					else:
						warningError('Warning',res['msg'])
				else:
					# print(e)
					warningError('Error','网络错误')
					
			except Exception as e:
				# print(e)
				warningError('Error','网络错误')

		button = tkinter.Button(root, text='登录',command=func)
		button.grid(row=2,column=2)
		root.mainloop()	

	login()
