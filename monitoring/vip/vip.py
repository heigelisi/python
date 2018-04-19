import pymysql


# connect = pymysql.connect(host='192.168.1.88',user='root',passwd='123456',db='vip',charset='utf8',port=3306);#链接数据库
# cursor = connect.cursor();#创建一个游标
# sql = "select id,name from info"
# cursor.execute(sql)
# data = cursor.fetchall()

# 			connect.commit()


import sqlite3,os

conn = sqlite3.connect('vip.db')
c = conn.cursor()
sql = "select * from vip"
c.execute(sql)
data = c.fetchall()
datas = {}
ii = 1
for row in data:
	row = list(row)
	if os.path.exists('cookies/'+row[2]+'.json'):
		row.append('是')
	else:
		row.append('否')
	datas[ii] = row
	ii += 1

for k,v in datas.items():
	print(v)