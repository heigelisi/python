
upate info set listen = 1,message = 1,friends = 1,hello = 1
import pymysql


conn1 = pymysql.connect(host='localhost',user='root',passwd='',db='spider',charset='utf8',port=3306)
cursor1 = conn1.cursor();#创建一个游标

sql = "select url,title from dz"

cursor1.execute(sql)
data = cursor1.fetchall()


conn2 = pymysql.connect(host='localhost',user='root',passwd='',db='vip',charset='utf8',port=3306)
cursor2 = conn2.cursor();#创建一个游标

for row in data:

	insersql = "insert into info(name,url) values('%s','%s')"%(row[1][0:10],row[0])
	print(insersql)
	cursor2.execute(insersql.encode())
	conn2.commit()

