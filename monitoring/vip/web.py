import redis
import sqlite3
import pymysql
import os
from flask import Flask
from flask import render_template
from flask import request
import time
app = Flask(__name__)



def updates():
	print('同步数据')
	conn = sqlite3.connect('vip.db')
	c = conn.cursor()
	connect = pymysql.connect(host='118.184.48.71',user='root',passwd='DgLs@1SL@*JLG[dE6URzf^O8&IEY4f$(U5TO*3ghWI)YfH]',db='xkx7_cc',charset='utf8',port=3306);#链接数据库
	cursor = connect.cursor();#创建一个游标
	sql = "select url,title from info where status = 1"
	cursor.execute(sql)
	data = cursor.fetchall()
	for row in data:
		sql2 = "select * from vip where url like '%"+"%s"%row[0]+"%'"
		c.execute(sql2)
		data = c.fetchall()
		if not data:
			insersql = "insert into vip(name,url) values('%s','http://%s')"%(row[1],row[0])
			c.execute(insersql)
			conn.commit()
			print(insersql)

updates()

@app.route('/')
@app.route('/')
def index():
	conn = sqlite3.connect('vip.db')
	c = conn.cursor()
	sql = "select * from vip"
	c.execute(sql)
	data = c.fetchall()
	datas = {}
	ii = 1
	for row in data:
		row = list(row)
		if os.path.exists('cookies/'+row[2].replace('http://','').replace('https://','')+'.json'):
			row.append('是')
		else:
			row.append('否')
		datas[ii] = row
		ii += 1



	return render_template('index.html',data=datas)



@app.route('/updateusername', methods=['POST'])
def updateusername():
	type_ = request.form.get('type')
	username = request.form.get('username')
	id_ = request.form.get('id')
	conn = sqlite3.connect('vip.db')
	c = conn.cursor()
	sql = "update vip set %s = '%s' where id = %d"%(type_,username,int(id_))
	c.execute(sql)
	conn.commit()
	return '1'


@app.route('/getcookie', methods=['POST'])
def getcookie():

	id_ = request.form.get('id')

	conn = sqlite3.connect('vip.db')
	c = conn.cursor()
	sql = "select url,username,password from vip where id = %s"%str(id_)
	c.execute(sql)
	data = c.fetchall()
	filestr = "%s|-|%s|-|%s"%(data[0][0],data[0][1],str(data[0][2]))
	with open('getcookieone.txt','w',encoding='utf8') as f:
		f.write(filestr)


	# conn.commit()
	return id_



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)