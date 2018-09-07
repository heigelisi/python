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

class Spider(object):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
	SearchWaiting = []
	SearchDzlist = []
	path = os.path.dirname(sys.argv[0])+'/'
	stop = ''
	def __init__(self):
		print('正在启动...')
		pass
		
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

				if '错误' in title or '404' in title or '页面不存在' in title or '找不回' in title or '新闻' in title:
					sys.exit()

				#判断是否是dz
				if 'href="forum.php' in html or "href='forum.php" in html:
					url_ = url.split('/')
					url = url_[0]+'//'+url_[2]
					dz = True
					self.SearchDzlist.append(url+':::'+title[0:15])

			except Exception as e:
				sys.exit()
			
		except Exception as e:
			pass
		sys.exit()


	def baiduSearch(self,keywords,pagecount):
		try:
			print('检测网络状态...')
			url = "https://www.baidu.com/s?wd="+keywords
			htmlobj = requests.get(url,headers=self.headers,allow_redirects=False,timeout=10)
			if htmlobj.status_code != 200:
				print(htmlobj.status_code)
				sys.exit()
		except Exception as e:
			print('访问超时，请检测网络状态')
			self.stop = True
			sys.exit()
		try:
			doc = pyquery.PyQuery(htmlobj.text)
			purl = "https://www.baidu.com/s?wd="+str(keywords)
			for i in range(pagecount):
				try:
					if i+1 == pagecount:
						self.stop = True
					htmlobj2 = requests.get(purl,headers=self.headers,timeout=10)
					print('采集第 '+str(i+1)+' 页',htmlobj2.url)
					doc2 =  pyquery.PyQuery(htmlobj2.text.encode().decode('utf8'))
					next_ = doc2('#page .n').attr('href')#获取下一页链接
					#没找到就没用下一页了
					if not next_:
						print('没有了')
						sys.exit()

					purl = "https://www.baidu.com"+next_#下一页链接
					#要抓取的内容
					li = doc2('.c-container h3 a')
					for row in li:
						doc3 = pyquery.PyQuery(row)
						url = doc3('a').attr('href')
						self.SearchWaiting.append(url)
						print(url)

				except Exception as e:
					pass


		except Exception as e:
			pass


	def main(self,keywords,pagecount=10):
		
		w = threading.Thread(target=self.baiduSearch,args=(keywords,pagecount,))
		w.start()

		wlist = []
		while True:
			if self.stop and len(self.SearchWaiting) <= 0:
				break
			if len(self.SearchWaiting) <= 0:
				continue
			if threading.active_count() < 200:
				url = self.SearchWaiting.pop()
				if url:
					w = threading.Thread(target=self.grab,args=(url,))
					w.start()
					wlist.append(w)
				

			else:
				print('等待其它线程抓取完成')
				time.sleep(3)

		for w in wlist:
			w.join()

		if self.SearchDzlist:
			while True:
				print('没有了等待所有线程完毕...')
				if threading.active_count() <= 1:
					break
				time.sleep(1)
			urllist = list(set(self.SearchDzlist))
			urlliststr = "\n".join(urllist)
			f = open(self.path+'dzlist.txt','a',encoding='utf8')
			msg = "搜索 "+keywords+" 共查找 "+str(pagecount)+" 页 获取到 "+str(len(urllist))+" 条数据"
			print(msg)
			f.write("\n\n\n"+time.strftime('%Y-%m-%d %H:%M:%S')+msg+"\n")
			f.write(urlliststr)
			f.close()
			print('获取完毕,数据也保存到当前目录下的',self.path+'dzlist.txt','文件中')
		else:
			print('没有找到任何结果')


if __name__ == '__main__':

	while True:
		try:
			pass
			input_ = input('请输入关键字、要获取的页数,用英文状态下的三个 ::: 连接,格式：关键词:::页数(数字)\n').split(":::")
			if len(input_) < 2:
				print('参数错误，请重新输入')
				continue
			keywords = input_[0]
			pagecount = int(input_[1])
			break
		except Exception as e:
			print('参数错误，请重新输入')
		
	Spider().main(keywords,pagecount)
	time.sleep(10)