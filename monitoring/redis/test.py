
import redis
import requests
import pyquery
import base64
import re
import time

# print(base64.b64decode('aHR0cDovL3d3dy5keGo4Lm1lL3NwYWNlLXVpZC0xMDAuaHRtbA=='))

pool = redis.ConnectionPool(host='localhost', port=6379)
conn = redis.Redis(connection_pool=pool)
# binfo = ['lao','wang','python']
# h = "ssshttps://www.baidu.com/sss/html/sss.html"
# pattern = re.compile(r'.*?(http.*?\.[A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
# urls = re.findall(pattern,h)[0]
# print(urls)
# print('__'.join(binfo))


# conn.sadd('test','192.168.1.99','111111111111','222222222222222222','222222222222222222',li)
# print(conn.smembers('test'))

print(conn.smembers('Waiting'))
time.sleep(100)
# html = "https://www.sobt5.org', b'http://www.btc98.com', b'http://www.11cdd.com', "
# pattern = re.compile(r'.*?(https?:\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
# urls = list(set(re.findall(pattern,html)))

# print(urls)

# print(conn.smembers("dzlist"))

# ban = ['错误','404','页面不存在','找不回','新闻','医生','自行车','单车','摩托车','旅游','投资','金融','垂钓','钓鱼','学院','财经','网赚','医疗']
# title = 'sdfd了的时间里就挂了手机铃声露横江两个号四六级发牢骚'

# for i in ban:
# 	if i in title:
# 		print(1111)

# # for i in range(1000):

# li = conn.smembers('dzlist')
# for i in li:
# 	print(i.decode())

# print(conn.smembers('SearchDzlist'))
# print(conn.scard('SearchDzlist'))
# print(conn.scard('Waiting'))
# for i in range(14130):
	# print(conn.spop('Waiting'))

# print(conn.spop('iplist2'))

# s = "http://www.baidu.com:::百度"
# sl = s.split(':::')
# print(sl)


# http://www.7pa.cc:::奇葩福利-专注宅男福
# http://www.ds88.ml:::杜尚,街拍,杜尚综合
# http://www.hlwbbs66.com:::好莱污精品社区论坛 
# http://www.pyp98.com:::手机成人电影,手机A
# http://www.ak123.me:::石榴社区_先锋影音_
# http://www.btshoufa.net:::BT首发论坛_电影论
# http://www.selutang02.com:::色撸堂♀性福生活♂第
# http://www.ds44.ml:::杜尚,街拍,杜尚综合
# http://www.19ytt.com:::N夜天堂论坛 - P
# http://www.ds99.ml:::杜尚,街拍,杜尚综合
# http://www.zls920.org:::宅狼社 - Powe
# http://ww.b8bbb.com:::有B吗？自拍论坛-w
# http://www.2b9c.com:::色妞论坛 - Pow