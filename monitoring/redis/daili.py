
import redis
import requests
import pyquery
import time
import threading
import re

class Daili(object):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
	page = 1
	def __init__(self):

		pool = redis.ConnectionPool(host='localhost', port=6379)
		self.conn = redis.Redis(connection_pool=pool)



	# r.set('name', 'zhangsan')   #添加
	# print (r.get('name'))   #获取
	# print (r.get('name'))   #获取

	def proxiesfun(self):

		while True:
			if self.conn.scard('iplist1') < 1000:
				try:
					htmlobj = requests.get('https://www.kuaidaili.com/free/inha/%s/'%str(self.page),headers=self.headers).text.encode().decode('utf8')
					ip_adress = re.compile('<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>')
					re_ip_adress = ip_adress.findall(htmlobj)
					for adress, port in re_ip_adress:
						print(adress)
						self.conn.sadd('iplist1',adress+':'+port)

				except Exception as e:
					print(e)
					continue
					pass
				self.page += 1
			else:
				print(self.conn.smembers('iplist1'))
				time.sleep(30)





	# def proxiesfun(self):

	# 	while True:
	# 		if self.conn.scard('iplist1') < 1000:
	# 			try:
	# 				htmlobj = requests.get('http://www.xicidaili.com/nn/'+str(self.page),headers=self.headers).text.encode().decode('utf8')
	# 				doc = pyquery.PyQuery(htmlobj)
	# 				tr = doc('tr')
	# 				for i in tr:
	# 					d = pyquery.PyQuery(i)
	# 					ip = d('td').eq(1).text()
	# 					prot = d('td').eq(2).text()
	# 					self.conn.sadd('iplist1',ip+':'+prot)
	# 			except Exception as e:
	# 				# print(e)
	# 				pass
	# 			self.page += 1
	# 		else:
	# 			# print(self.conn.smembers('iplist1'))
	# 			time.sleep(30)



	def getproxies(self):

		while True:
			# print('获取')
			try:
				if self.conn.scard('iplist2') < 200:
					ip = self.conn.spop('iplist1')
					if ip:
						print('检测',ip,'是否可以正常访问,第',self.page,'页数据')
						ip = ip.decode()
						proxies = {"http":"http://"+ip}
						htmlobj = requests.get('http://permissions.hk-dna.cc/ip.php',headers=self.headers,proxies=proxies,timeout=10)
						if htmlobj.status_code == 200:
							self.conn.sadd('iplist2',ip)
							print(ip,' 正常')
					else:
						print('等待获取ip')
						time.sleep(10)
				else:
					print(self.conn.smembers('iplist2'))
					time.sleep(10)
			except Exception as e:
				print(e)
				# time.sleep(5)
				pass
		


	def main(self):
		w = threading.Thread(target=self.proxiesfun)
		w.start()
		for i in range(100):
			w = threading.Thread(target=self.getproxies)
			w.start()

if __name__ == '__main__':
	Daili().main()