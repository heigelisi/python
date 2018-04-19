import pymysql,requests
from urllib import parse

connect = pymysql.connect(host='118.193.194.3',user='root',passwd='DgLs@1SL@*JLG[dE6URzf^O8&IEY4f$(U5TO*3ghWI)YfH]',db='xkx7_cc',charset='utf8',port=3306);#链接数据库
cursor = connect.cursor();#创建一个游标

connect2 = pymysql.connect(host='localhost',user='root',passwd='',db='vip',charset='utf8',port=3306);#链接数据库
cursor2 = connect2.cursor();#创建一个游标


sql = "select * from info"

cursor.execute(sql)
data = cursor.fetchall()

for i in data:
	username = requests.get('http://www.b.com/vip/index/test?cipher=%s&iv=%s'%(parse.quote(i[3]),parse.quote(i[4]))).text
	password = requests.get('http://www.b.com/vip/index/test?cipher=%s&iv=%s'%(parse.quote(i[5]),parse.quote(i[6]))).text
	insersql = "insert into info(name,url,username,password) values('%s','%s','%s','%s')"%(i[1],i[2],username,password)
	print(insersql)
	cursor2.execute(insersql)
	connect2.commit()