
import pymysql
import sqlite3

import json
import re
import sys,os



#id到  26221
connect = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306);#链接数据库
cursor = connect.cursor();#创建一个游标

# connect2 = pymysql.connect(host='192.168.1.88',user='root',passwd='123456',db='vip',charset='utf8',port=3306);#链接数据库
# cursor2 = connect2.cursor();#创建一个游标
connect2 = sqlite3.connect('monitoring.db')
cursor2 = connect2.cursor()
sql = "select distinct url,id,title from dzlist where id > 26221"
cursor.execute(sql)
data = cursor.fetchall()
for r in data:
	url1 = r[0]
	title = r[2]
	ban = ['错误','404','页面不存在','找不回','新闻','医生','医学','医院','自行车','单车','摩托车','旅游','投资','金融','垂钓','钓鱼','学院','财经','网赚','医疗','残疾','寻亲','减肥','房产','民航','诗词','教育','唐诗','诗歌','招聘','幼儿园','司法','千峰IT','QQ','糖尿病','安卓','中国','驴友','白癜风','Discuz! 官方']
	for b in ban:
		if b in title:
			continue

	id_ = r[1]
	pattern = re.compile(r'.*?https?:\/\/([A-Za-z0-9]+\.)?([A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
	urls = pattern.findall(url1)
	url = urls[0][1]
	sql2 = "select url,name from info where url like '%"+"%s"%url+"%' or name = '"+title+"'"
	cursor2.execute(sql2)
	d = cursor2.fetchall()
	sql3 = "select url,name from info2 where url like '%"+"%s"%url+"%' or name = '"+title+"'"
	cursor2.execute(sql3)
	d2 = cursor2.fetchall()

	if not d and not d2:

		pattern = re.compile(r'.*?(https?:\/\/[A-Za-z0-9]+\.?[A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
		urls2 = pattern.findall(url1)[0]
		print(title,urls2)
		sql = "insert into info(url,name,username,password,email) values('%s','%s','www.ux7.cc','ADC3898658cds','www.ux7.cc@qq.com')"%(urls2,title)
		cursor2.execute(sql)
		connect2.commit()
	



# connect = pymysql.connect(host='192.168.1.88',user='root',passwd='123456',db='vip',charset='utf8',port=3306);#链接数据库
# cursor = connect.cursor();#创建一个游标

# # connect2 = pymysql.connect(host='192.168.1.88',user='root',passwd='123456',db='vip',charset='utf8',port=3306);#链接数据库
# # cursor2 = connect2.cursor();#创建一个游标
# connect2 = sqlite3.connect('monitoring.db')
# cursor2 = connect2.cursor()

# sql = "select perform,seal,type,name,url,registered,listen,message,friends,hello,username,password,email,note,addtime,cookie from info2"
# cursor.execute(sql)
# data = cursor.fetchall()
# for r in data:
# 	print(r)
# 	# url1 = r[5]
# 	# title = r[4]
# 	# ban = ['错误','404','页面不存在','找不回','新闻','医生','医学','医院','自行车','单车','摩托车','旅游','投资','金融','垂钓','钓鱼','学院','财经','网赚','医疗','残疾','寻亲','减肥','房产','民航','诗词','教育','唐诗','诗歌','招聘','幼儿园','司法','千峰IT','QQ','糖尿病','安卓','中国','驴友','白癜风','Discuz! 官方']
# 	# for b in ban:
# 	# 	if b in title:
# 	# 		continue

# 	# id_ = r[0]
# 	# pattern = re.compile(r'.*?https?:\/\/([A-Za-z0-9\-]+\.)?([A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
# 	# urls = pattern.findall(url1)
# 	# print(urls)
# 	# url = urls[0][1]
# 	# sql2 = "select url,name from info where url like '%"+"%s"%url+"%' or name = '"+title+"'"
# 	# cursor2.execute(sql2)
# 	# d = cursor2.fetchall()
# 	# if not d:

# 		# pattern = re.compile(r'.*?(https?:\/\/[A-Za-z0-9]+\.?[A-Za-z0-9]+\.[A-Za-z0-9]+).*?',re.S)
# 		# urls2 = pattern.findall(url1)[0]
# 		# print(title,urls2)
# 	if not r[13]:
# 		sql = "insert into info(perform,seal,type,name,url,registered,listen,message,friends,hello,username,password,email,note,addtime,cookie) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
# 		cursor2.execute(sql,r)
# 		connect2.commit()
# 	else:
# 		sql = "insert into info2(perform,seal,type,name,url,registered,listen,message,friends,hello,username,password,email,note,addtime,cookie) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
# 		cursor2.execute(sql,r)
# 		connect2.commit()

