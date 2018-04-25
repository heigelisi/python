import flask
import json
from flask import request
from flask import session
from PIL import Image,ImageDraw,ImageFont
import sqlite3
import random
import base64
import re
import time
import os
import sys
import math
app = flask.Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
path = os.path.dirname(sys.argv[0])
db = path+'/monitoring.db'


conn = sqlite3.connect(db)
c = conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS "info" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"perform"  INTEGER NOT NULL DEFAULT 0,
"seal"  INTEGER NOT NULL DEFAULT 0,
"cookie"  INTEGER NOT NULL DEFAULT 0,
"type"  TEXT(100) NOT NULL DEFAULT 未知,
"name"  TEXT(30) NOT NULL DEFAULT 网站名称,
"url"  TEXT(100) NOT NULL DEFAULT 网址,
"registered"  INTEGER NOT NULL DEFAULT 0,
"listen"  INTEGER NOT NULL DEFAULT 0,
"message"  INTEGER NOT NULL DEFAULT 0,
"friends"  INTEGER NOT NULL DEFAULT 0,
"hello"  INTEGER NOT NULL DEFAULT 0,
"username"  TEXT(30) NOT NULL DEFAULT username,
"password"  TEXT(30) NOT NULL DEFAULT 密码,
"email"  TEXT(30) NOT NULL DEFAULT 邮箱,
"note"  TEXT(100),
"addtime"  INTEGER
);'''
c.execute(sql)
conn.commit()
sql2 = '''CREATE TABLE IF NOT EXISTS "info2" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"perform"  INTEGER NOT NULL DEFAULT 0,
"seal"  INTEGER NOT NULL DEFAULT 0,
"cookie"  INTEGER NOT NULL DEFAULT 0,
"type"  TEXT(100) NOT NULL DEFAULT 未知,
"name"  TEXT(30) NOT NULL DEFAULT 网站名称,
"url"  TEXT(100) NOT NULL DEFAULT 网址,
"registered"  INTEGER NOT NULL DEFAULT 0,
"listen"  INTEGER NOT NULL DEFAULT 0,
"message"  INTEGER NOT NULL DEFAULT 0,
"friends"  INTEGER NOT NULL DEFAULT 0,
"hello"  INTEGER NOT NULL DEFAULT 0,
"username"  TEXT(30) NOT NULL DEFAULT username,
"password"  TEXT(30) NOT NULL DEFAULT 密码,
"email"  TEXT(30) NOT NULL DEFAULT 邮箱,
"note"  TEXT(100),
"addtime"  INTEGER
);'''
c.execute(sql2)
conn.commit()
conn.close()

@app.route('/add/')
@app.route('/add',methods=['POST','GET'])
def add():
	if request.method == 'POST':
		data = request.form
		datas = (data.get('type'),data.get('name'),data.get('url'),data.get('registered'),data.get('listen'),data.get('message'),data.get('friends'),data.get('hello'),data.get('username'),data.get('password'),data.get('email'),data.get('note'),int(time.time()))
		conn = sqlite3.connect(db)
		c = conn.cursor()
		sql = """insert into info2(type,name,url,registered,listen,message,friends,hello,username,password,email,note,addtime) values(?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		res = c.execute(sql,(datas))
		if res:
			conn.commit()
			return flask.redirect('/index')
		else:
			return '<script>alert("添加失败！");window.history.go(-1);</script>'

	else:

		return flask.render_template('add.html')


@app.route('/update/')
@app.route('/update',methods=['POST'])
def update():
	conn = sqlite3.connect(db)
	c = conn.cursor()

	if request.method == 'POST':
		data = request.form
		datas = (data.get('type'),data.get('name'),data.get('url'),data.get('registered'),data.get('listen'),data.get('message'),data.get('friends'),data.get('hello'),data.get('username'),data.get('password'),data.get('email'),data.get('note'),data.get('perform'),data.get('id'))
		sql = """update info2 set type = ?,name = ?,url = ?,registered = ?,listen = ?,message = ?,friends = ?,hello = ?,username = ?,password = ?,email = ?,note = ?,perform = ? where id = ?"""
		res = c.execute(sql,(datas))
		if res:
			conn.commit()
			conn.close()
			return flask.redirect('/index')
		else:
			return '<script>alert("修改失败！");window.history.go(-1);</script>'

	else:
		id_ = request.args.get('id')
		sql = "select id,type,name,url,registered,listen,message,friends,hello,username,password,email,note,perform from info2 where id = "+id_
		c.execute(sql)
		data = c.fetchall()
		print(data[0])
		datas = []
		# for d in data:

		conn.close()
		return flask.render_template('update.html',data=data[0])	




@app.route('/index/')
@app.route('/',methods=['GET'])
def index():

	url = '' #分页中的url
	#筛选
	checked = request.args.getlist('screening')
	
	#关键字
	q = request.args.get('q')
	if q == 'None':
		q = ''
	#当前页数
	p = request.args.get('p')
	if not p:
		p = 1
	limit = (int(p) - 1) * 30
	where = ''
	if checked or q:
		where = "where "
	if checked:
		for u in checked:
			url += 'screening='+u+'&'

		for r in checked:
			r = r.split('_')
			where += r[0]+' = '+r[1]+' and '
	if q:
		url += "q="+q+'&'
		where += "(name like '%{0}%' or  url like '%{0}%' or username like '%{0}%' or password like '%{0}%' or note like '%{0}%')".format(q)

	where = where.strip().strip('and')
	conn = sqlite3.connect(db)
	c = conn.cursor()
	sql = "select * from info2 "+where+' limit %s,30'%limit
	c.execute(sql)
	data = c.fetchall()
	sql2 = "select count(1) from info2 "+where
	c.execute(sql2)
	count = c.fetchall()
	page = math.ceil(count[0][0] / 30)
	conn.close()
	screening = {
		'perform_1':'执行(是)','perform_0':'执行(否)',
		'seal_1':'封号(是)','seal_0':'封号(否)',
		'cookie_1':'cookie(是)','cookie_0':'cookie(否)',
		'registered_1':'注册(是)','registered_0':'注册(否)',
		'listen_1':'收听(是)','listen_0':'收听(否)',
		'message_1':'消息(是)','message_0':'消息(否)',
		'friends_1':'好友(是)','friends_0':'好友(否)',
		'hello_1':'招呼(是)','hello_0':'招呼(否)'
		};

	return flask.render_template('index.html',data=data,screening=screening,checked=checked,q=q,page=page,count=count[0][0],p=int(p),url=url,isreg='可以注册',title="不可注册列表")



@app.route('/delete')
def delete():
	id_ = request.args.get('id')
	sql = "delete from info2 where id = "+id_
	conn = sqlite3.connect(db)
	c = conn.cursor()
	if c.execute(sql):
		conn.commit()
		return '1'


@app.route('/status',methods=['POST'])
def status():
		if request.method == 'POST':
			parameter = request.form.get('parameter').strip()#账号
			parameter_ = parameter.split('_')
			sql = "select %s from info2 where id = %s"%(parameter_[0],parameter_[1])
			conn = sqlite3.connect(db)
			c = conn.cursor()
			c.execute(sql)
			status_ = c.fetchall()[0][0]
			sql2 = "update info2 set %s = %s where id = %s"%(parameter_[0],str(int(not int(status_))),parameter_[1])
			res = 0
			if c.execute(sql2):
				conn.commit()
				res = 1

			conn.close()
			datastr = json.dumps({'res':res,'perform':int(not int(status_))})
			return datastr

@app.route('/getcookieone',methods=['POST'])
def getcookieone():
	if request.method == 'POST':
		id_ = request.form.get('id').strip()#账号
		sql = "select url,username,password from info2 where id = "+str(id_)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute(sql)
		data = c.fetchall()[0]
		with open(path+'/exe/getcookieone.txt','w',encoding='utf8') as f:
			f.write(data[0]+'|-|'+data[1]+'|-|'+data[2])
		conn.close()
		return '1'


@app.route('/updatecookie')
def updatecookie():
	sql = "select id,url from info2"
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute(sql)
	data = c.fetchall()
	cookie0 = ''
	cookie1 = ''
	for row in data:
		if os.path.exists(path+'/exe/cookies/'+row[1].replace('http://','').replace('https://','')+'.json'):
			cookie1 += str(row[0]) + ','
		else:
			cookie0 += str(row[0]) + ','

	updatesql1 = "update info2 set cookie = 1 where id in (%s)"%(cookie1.strip(','))
	updatesql0 = "update info2 set cookie = 0 where id in (%s)"%(cookie0.strip(','))
	c.execute(updatesql1)
	conn.commit()
	c.execute(updatesql0)
	conn.commit()
	conn.close()
	return flask.redirect('/index')

@app.route('/updateinput',methods=['POST'])
def updateinput():
	type_ = request.form.get('type')
	input_ = request.form.get('input')
	id_ = request.form.get('id')
	print(type_,input_,id_)
	conn = sqlite3.connect(db)
	c = conn.cursor()
	sql = "update info2 set %s = '%s' where id = %d"%(type_,input_,int(id_))
	c.execute(sql)
	conn.commit()
	return '1'

@app.route('/notreg',methods=['POST'])
def notreg():
	if request.method == 'POST':
		id_ = request.form.get('id')
		sql = "insert into info(perform,seal,type,name,url,registered,listen,message,friends,hello,username,password,email,note,addtime,cookie) select perform,seal,type,name,url,registered,listen,message,friends,hello,username,password,email,note,addtime,cookie from info2 where id = "+str(id_)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		if c.execute(sql):
			conn.commit()
			delsql = "delete from info2 where id = "+str(id_)
			c.execute(delsql)
			conn.commit()
			return '1'



if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8009)