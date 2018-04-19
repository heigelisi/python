import requests
import re
import time
import redis
import sys
import pyquery
import threading
import pymysql

class DzSpider(object):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}

	def __init__(self):
		print('连接redis')
		try:
			pool = redis.ConnectionPool(host='localhost', port=6379)
			self.conn = redis.Redis(connection_pool=pool)
			print('redis连接成功')
		except Exception as e:
			print('redis连接失败!!!')
			exit()
		
		



	def grab(self,url):
		try:
			print('访问',url)
			dz = False
			title = ''
			try:
				htmlobj = requests.get(url,headers=self.headers,timeout=10)
				url = htmlobj.url
				try:
					try:
						encoding = requests.utils.get_encodings_from_content(htmlobj.text)[0]
					except Exception as e:
						encoding = 'utf8'
					if encoding:
						htmlobj.encoding = encoding
				except Exception as e:
					pass

			except Exception as e:
				print('访问超时',url)
				sys.exit()


			#如果状态码不等于200 关闭
			if htmlobj.status_code != 200:
				sys.exit()

			print(url, ' 正在获取页面信息')
			
			try:
				html = htmlobj.text.encode().decode('utf8')
				q = pyquery.PyQuery(html)
				title = q('title').text()[0:300].strip().replace('"','').replace("'",'').replace('--','')

				ban = ['错误','404','页面不存在','找不回','新闻','医生','医学','医院','自行车','单车','摩托车','旅游','投资','金融','垂钓','钓鱼','学院','财经','网赚','医疗','残疾','寻亲','减肥','房产','民航','诗词','教育','唐诗','诗歌','招聘','幼儿园','司法','千峰IT','QQ','糖尿病','安卓','中国','驴友','白癜风','飞行','中华','直升机','军人','足球']
				for b in ban:
					if b in title and '熟女' not in title and '街拍' not in title:
						sys.exit()

				#判断是否是dz
				if 'href="forum.php"' in html or "href='forum.php'" in html:
					dz = True
					self.conn.sadd('dzlist',url+':::'+title[0:10])

			except Exception as e:
				sys.exit()
			
			if not dz and '导航' not in title:
				print(url,'不是dz也不是网址导航，不提取链接')
				sys.exit()

			print(url, ' 提取外部链接')

			try:
				#匹配所有觉得连接
				pattern = re.compile(r'.*?(https?:\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
				urls = list(set(re.findall(pattern,html)))
				# print(urls)
				urllist = []
				for u in list(urls):
					#排除子域名 防止站群
					try:
						myurl = url.split('.')[1] #切割当前访问的连接
						uurl = u.split('.')[1]
						if url not in u and 'w3.org' not in u and 'qq.com' not in u and 'cnzz.com' not in u and 'baidu.com' not in u and '0455xx.cn' not in u and myurl != uurl:
							urllist.append(u)
					except Exception as e:
						continue

			except Exception as e:
				sys.exit()

			print('外部连接提取成功')
			if urllist:
				
				for row in urllist:

					self.conn.sadd('Waiting',row)
				

		except Exception as e:
			print(e)
		sys.exit()


	def setDb(self):
		while True:
			try:
				count = self.conn.scard('dzlist')
				if count >= 10:
					conn = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
					cursor = conn.cursor();#创建一个游标
					for r in range(10):
						url = self.conn.spop('dzlist').decode()
						urll = url.split(':::')
						sql = "insert into dzlist(url,title) values('%s','%s')"%(urll[0],urll[1])
						cursor.execute(sql)
						conn.commit()

				else:
					print(self.conn.smembers('dzlist'))
					time.sleep(30)
			except Exception as e:
				pass
			

	def main(self,starturl):
		if self.conn.scard('Waiting') == 0:
			self.conn.sadd('Waiting',starturl)

		w = threading.Thread(target=self.setDb)
		w.start()

		while True:
			if threading.active_count() < 200:
				url = self.conn.spop('Waiting')
				if url:
					url = url.decode()
					w = threading.Thread(target=self.grab,args=(url,))
					w.start()


			else:
				print('等待其它线程抓取完成')
				time.sleep(3)
			


if __name__ == '__main__':
	DzSpider().main('http://www.fuliking2.com')