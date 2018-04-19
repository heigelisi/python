import time
import threading
import os
import json
import sys
import re
import requests
import sqlite3
import pyquery
import pymysql


class Spider(object):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
	def __init__(self):
		pass



	def grab(self,id_,url):
		try:
			#链接数据库
			# conn = sqlite3.connect('./spider.db')
			# cursor = conn.cursor()
			conn = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
			cursor = conn.cursor();#创建一个游标
			print('正在抓取 ',url)
			title = ''
			
			try:
				htmlobj = requests.get(url,headers=self.headers,timeout=10)
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
				self.myclose(url,cursor,conn,id_,'访问超时')

			print(url, ' 正在获取页面信息')
			#判断是否是dz
			try:
				if htmlobj.status_code == 200:
					html = htmlobj.text.encode().decode('utf8')
					# pattern1 = re.compile(r'.*?<title>(.*?)</title>.*?',re.S)
					# title = re.findall(pattern1,html)[0].strip().replace('"','').replace("'",'').replace('--','')
					q = pyquery.PyQuery(html)
					title = q('title').text()[0:300].strip().replace('"','').replace("'",'').replace('--','')
					print(url,title)
					if '错误' in title or '404' in title or '页面不存在' in title or '找不回' in title or '新闻' in title or '找不回' in title:
						self.myclose(url,cursor,conn,id_,title)

					if 'href="forum.php"' in html or "href='forum.php'" in html:
						#为dz论坛 添加到dz表
						print(url,' DZ')
						try:

							selectsql = "select * from dz where url = '%s'"%url
							cursor.execute(selectsql)
							seledata = cursor.fetchall()
							if not seledata:
								sql = "insert into dz(url,title) values('%s','%s')"%(url,title)
								cursor.execute(sql)
								conn.commit()
						except Exception as e:
							pass
					else:
						print(url, '不是DZ')	

				else:
					sys.exit()
			except Exception as e:
				print(url ,e,' 3')
			
			print(url, ' 提取外部链接')

		# 	try:
		# 		#匹配所有觉得连接
		# 		pattern = re.compile(r'.*?(http:\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
		# 		urls = list(set(re.findall(pattern,html)))
		# 		# print(urls)
		# 		urllist = []
		# 		for u in list(urls):
		# 			#排除子域名 防止站群
		# 			try:
		# 				myurl = url.split('.')[1] #切割当前访问的连接
		# 				uurl = u.split('.')[1]
		# 				if url not in u and 'w3.org' not in u and 'qq.com' not in u and 'cnzz.com' not in u and 'baidu.com' not in u and '0455xx.cn' not in u and myurl != uurl:
		# 					urllist.append(u)
		# 			except Exception as e:
		# 				print(url ,e,7)

		# 	except Exception as e:
		# 		print(url ,e,' 4')
		# 	if urllist:
		# 		sql = "insert into tmp(url,title) values"
		# 		for row in urllist:
		# 			sql += "('%s',''),"%(row)
		# 		cursor.execute(sql[0:-1])
		# 		conn.commit()
				
				

		except Exception as e:
			print(e,' 5')

		self.myclose(url,cursor,conn,id_,title)
		
	def myclose(self,url,cursor,conn,id_,title):
		#抓取完成后 从待抓取中删除
		try:
			sql = "delete from tmp where url = '%s'"%url
			cursor.execute(sql)
			conn.commit()
		except Exception as e:
			pass

		try:
			#添加到已经抓取
			sql = "insert into already(url,title) values('%s','%s')"%(url,title)
			cursor.execute(sql)
			conn.commit()
		except Exception as e:
			pass
		
		
		conn.close()
		print(url ,'抓取完成')
		sys.exit()

	def main(self,initurl):
		try:
			#链接数据库
			# conn = sqlite3.connect('./spider.db')
			# cursor = conn.cursor()
			conn = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
			cursor = conn.cursor();#创建一个游标

			#添加到待抓取表
			try:
				sql1 = "select * from tmp where url = '%s'"%initurl
				cursor.execute(sql1)
				if not cursor.fetchall():

					sql = "insert into tmp(url,title) values('%s','%s')"%(initurl,'初始')
					cursor.execute(sql)
					conn.commit()


			except Exception as e:
				print(e)
				pass
			
			id_ = 0
			data = None
			conn.close()
			while True:
				#判断线程数量
				try:
					conn = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
					cursor = conn.cursor();#创建一个游标
				except Exception as e:
					continue
				if (threading.active_count()) < 100:
					#查询待抓取
					try:
						sql = "select id,url from tmp where id > "+str(id_)+" limit 1"
						cursor.execute(sql)
						data = cursor.fetchall()
					except Exception as e:
						continue
					
					#判断待抓取中是否有
					if data:
						id_ = data[0][0]

						#查询是否已经抓取过
						res = None
						try:
							sql = "select id,url from already where url = '%s'"%str(data[0][1])
							cursor.execute(sql)
							res = cursor.fetchall()
							if res:
								continue

						except Exception as e:
							print(e)
							continue


						w = threading.Thread(target=self.grab,args=(data[0][0],data[0][1],))
						w.start()
						print(threading.active_count(),'个线程正在运行',)
						# print('等待抓取的个数 ',len(self.urllist))
				else:
					print('等待其他抓取完成...')
					time.sleep(3)
				conn.close()	
		except Exception as e:
			print(e,' 6')	




if __name__ == '__main__':
	
	Spider().main('http://www.500dh.us')
