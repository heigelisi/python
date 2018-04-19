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
	userlist = []
	count = 0

	def select(self):
		conn = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
		cursor = conn.cursor();#创建一个游标
		limit = 0
		while True:
			if len(self.userlist) < 3:
				limit += 1
				sql = "select url from tmp limit %s,100"%str(limit)
				cursor.execute(sql)
				data = cursor.fetchall()
				for row in data:
					self.userlist.append(row[0])
				
			else:
				print('已过虐条数',limit*100)
				time.sleep(10)

	def grab(self,url):
		try:
			htmlobj = requests.get(url,headers=self.headers,timeout=25)
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
			print(e)
			print('访问超时',url)
			sys.exit()


		#判断是否是dz
		try:
			if htmlobj.status_code == 200:
				html = htmlobj.text.encode().decode('utf8')
				q = pyquery.PyQuery(html)
				title = q('title').text()[0:300].strip().replace('"','').replace("'",'').replace('--','')
				if '错误' in title or '404' in title or '页面不存在' in title or '找不回' in title or '新闻' in title or '找不回' in title:
					sys.exit()

				if 'href="forum.php"' in html or "href='forum.php'" in html:
					#为dz论坛 添加到dz表
					try:
						conn = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
						cursor = conn.cursor();#创建一个游标
						selectsql = "select * from dz where url = '%s'"%url
						cursor.execute(selectsql)
						seledata = cursor.fetchall()
						if not seledata:
							sql = "insert into dz(url,title) values('%s','%s')"%(url,title)
							cursor.execute(sql)
							conn.commit()
							conn.close()
							sys.exit()
					except Exception as e:
						pass
					

			else:
				sys.exit()
		except Exception as e:
			print(url ,e,' 3')

		sys.exit()


	def main(self):

		w = threading.Thread(target=self.select)
		w.start()

		while True:
			if len(self.userlist) > 0 and threading.active_count() < 100:

				url = self.userlist.pop()
				w = threading.Thread(target=self.grab,args=(url,))
				w.start()
				print(threading.active_count(),'个线程正在运行',)


if __name__ == '__main__':
	Spider().main()