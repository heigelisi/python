# 操作mysql的框架 sqlalchemy

pymysql.Connect()参数说明
host(str):      MySQL服务器地址
port(int):      MySQL服务器端口号
user(str):      用户名
passwd(str):    密码
db(str):        数据库名称
charset(str):   连接编码

connection对象支持的方法
cursor()        使用该连接创建并返回游标
commit()        提交当前事务
rollback()      回滚当前事务
close()         关闭连接

cursor对象支持的方法
execute(op)     执行一个数据库的查询命令
fetchone()      取得结果集的下一行
fetchmany(size) 获取结果集的下几行
fetchall()      获取结果集中的所有行
rowcount()      返回数据条数或影响行数
close()         关闭游标对象



import pymysql;
import hashlib;
import time;
connect = pymysql.connect(host='192.168.1.66',user='root',passwd='123',db='test',charset='utf8',port=3306);#链接数据库
cursor = connect.cursor();#创建一个游标
# cursor.execute("set names 'utf8'");#设置字符集


#增------------------------------------------------
password = hashlib.md5('123456'.encode('utf-8')).hexdigest();
# addtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()));
addtime = int(time.time());
insertsql = "insert into user(username,pwd,sex,tel,address,icon,status,addtime,wx,email) values('user7','%s','1','13539993040','广州','/1.jpg',1,%s,'vzhoufei','vzhoufei@qq.com')"%(password,addtime);
# insertsql = "insert into user(id,name) values(1,'zhoufei')";

try:
	res = cursor.execute(insertsql.encode('utf8'));#执行sql
	# 获取自增id
	dataid = cursor.lastrowid;
	connect.commit();#执行提交
	print(res)
except Exception as e:
	#如果报错回滚
	connect.rollback();




#改---------------------------------------------
updatesql = "update user set address = '广东' where id = 92";
try:
	cursor.execute(updatesql.encode('utf8'));
	connect.commit();
except Exception as e:
	print(e)
	# connect.rollback();



#删------------------------------------------------
delsql = "delete from user limit 1";
try:
	cursor.execute(delsql);
	# connect.commit();
except Exception as e:
	connect.rollback();


cursor.execute("set names 'utf8'");#设置字符集

#查-------------------------------------------------------
sql = "select * from user";
try:
	cursor.execute(sql);
	data = cursor.fetchall()
	for l in data:
		s = "id=%s,username=%s,pwd=%s,sex=%s,tel=%s,address=%s,icon=%s,status=%s,addtime=%s,wx=%s,email=%s"%(str(l[0]),str(l[1]),str(l[2]),str(l[3]),str(l[4]),str(l[5]),str(l[6]),str(l[7]),str(l[8]),str(l[9]),str(l[10]));
		print(s)
except Exception as e:
		print(e)







connect.close();#关闭
print(updatesql);

