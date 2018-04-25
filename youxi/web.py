import flask
import json
import datas
from flask import request
from flask import session
from PIL import Image,ImageDraw,ImageFont
import sqlite3
import random
import base64
import re
import time
app = flask.Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

conn = sqlite3.connect('game.db')
c = conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS info (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"accountr"  TEXT(30) NOT NULL DEFAULT NULL,
"passwordr"  TEXT(30) NOT NULL DEFAULT NULL,
"renewpassword"  TEXT(30) NOT NULL DEFAULT NULL,
"verifycoder"  TEXT(30) NOT NULL DEFAULT NULL,
"username"  TEXT(30) NOT NULL DEFAULT NULL,
"phone"  TEXT(30) NOT NULL DEFAULT NULL,
"time"  TEXT(30) NOT NULL DEFAULT NULL
);'''
c.execute(sql)
conn.commit()
conn.close()

@app.route('/index/')
@app.route('/')
def index():

	config = {
	'logo':'http://678v.cc/images/',
	'lunbo':'https://yb6.me/img/ASER/',
	'top':'http://678v.cc/images/',
	'jieshao':'http://678v.cc/images/',
	'nvyou':'http://678v.cc/common/template/third/newLiveV3/images/',
	'huangguan':'https://hg98089.com/style/hgxjwi/',
	'ag':'http://678v.cc/common/template/third/egame/images/',
	'mg':'http://678v.cc/common/template/third/egame/images/v2/',
	'pt':'http://678v.cc/common/template/third/newEgame/images/pt/pc/',
	'qt':'http://678v.cc/common/template/third/newEgame/images/qt/pc/',
	'qipai':'https://777.bge888.com/ipl/src/static/images/components/CardComponent/common/',
	}
	# session['userdata'] = None 
	userdata = session.get('userdata')

	# config = {
	# 'logo':'/static/images/',
	# 'lunbo':'/static/images/lunbo/',
	# 'top':'/static/images/top/',
	# 'jieshao':'/static/images/',
	# 'nvyou':'/static/images/nvyou/',
	# 'huangguan':'/static/images/',
	# 'ag':'/static/images/ag/',
	# 'mg':'/static/images/mg/',
	# 'pt':'/static/images/pt/',
	# 'qt':'/static/images/qt/',
	# 'qipai':'/static/images/qipai/',
	# }



	return flask.render_template('index.html',ag=datas.ag,mg=datas.mg,pt=datas.pt,qt=datas.qt,config=config,qipai=datas.qipai,userdata=userdata)

@app.route('/login',methods=['POST'])
def login():
	try:
		if request.method == 'POST':
			username = request.form.get('username').strip()
			password = request.form.get('password').strip()
			code = request.form.get('code').strip()
			print(code,session['code'])
			if code.lower() != session['code'].lower():
				return '验证码错误！'

			conn = sqlite3.connect('game.db')
			c = conn.cursor()
			sql = "select accountr from info where accountr = :username and passwordr = :password"
			c.execute(sql,{'username':username,'password':password})
			data = c.fetchall()
			if data:
				session['userdata'] = username
				return 'ok'
			else:
				return '用户名或密码错误！'
				

		else:
			return ''
	except Exception as e:
		pass

@app.route('/loginout')
def loginout():
	session['userdata'] = None
	return flask.redirect('/')

@app.route('/code')
def code():
	codes = ''
	#定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片
	img1=Image.new(mode="RGB",size=(80,32),color=(255,255,255))

	 #实例化一支画笔
	draw1=ImageDraw.Draw(img1,mode="RGB")

	#定义要使用的字体
	font1=ImageFont.truetype("AdobeFanHeitiStd-Bold.otf",20)

	for i in range(4):
	    #每循环一次,从a到z中随机生成一个字母或数字
	    #65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符
	    #str把生成的数字转换成字符串
	    char1=random.choice([chr(random.randint(65,90)),str(random.randint(0,9))])
	    codes += char1
	    #每循环一次重新生成随机颜色
	    color1=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
	    
	    #把生成的字母或数字添加到图片上
	    #图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
	    draw1.text([i*20,5],char1,color1,font=font1)
	session['code'] = codes
	#把生成的图片保存为"pic.png"格式
	with open("code.png","wb") as f:
	    img1.save(f,format="png")

	with open('code.png','rb') as f:
		file = f.read().strip()
		# base64.b64encode
		# dzyy = json.load(file);
	return file

@app.route('/reg',methods=['POST'])
def reg():
	try:

		if request.method == 'POST':
			conn = sqlite3.connect('game.db')
			c = conn.cursor()

			accountR = request.form.get('accountR').strip()#账号
			if not accountR:
				return '用户名不能为空！'
			r1 = re.compile(r'^[a-zA-Z]\w{4,10}$')
			res1 = re.search(r1, accountR)
			if not res1:
				return '用户名错误！5~11个字符，包括字母、数字，以字母开头，字母或数字结尾'

			sql_ = "select * from info where accountr = '%s'"%accountR
			c.execute(sql_)
			data = c.fetchall()
			if data:
				return '该用户名已经被注册！'


			passwordR = request.form.get('passwordR').strip() #密码
			if not passwordR:
				return '密码不能为空！'
			if len(passwordR) < 6 or len(passwordR) > 12:
				return '密码错误！6~12个字符，包括字母、数字、特殊符号，区分大小写'

			renewpassword = request.form.get('renewpassword').strip() #确认密码
			if renewpassword != passwordR:
				return '两次密码不一致！'

			userName = request.form.get('userName') .strip()#真实姓名
			if not userName:
				return '真实姓名不能为空！'

			phone = request.form.get('phone').strip() #手机
			r2 = re.compile(r'^((166)|(13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$')
			res2 = re.search(r2, phone)
			if not res2:
				return '手机号格式错误！'

			verifyCodeR = request.form.get('verifyCodeR').strip() #验证码
			if not verifyCodeR:
				return '验证码不能为空！'
			if verifyCodeR.lower() != session['code'].lower():
				print(verifyCodeR,session['code'])
				return '验证码错误！'
			
			addtime = time.strftime('%Y-%m-%d %H:%M:%S')
			sql = "insert into info(accountr,passwordr,renewpassword,verifycoder,username,phone,time) values(?,?,?,?,?,?,?)"
			res = c.execute(sql,(accountR,passwordR,renewpassword,verifyCodeR,userName,phone,addtime))
			if res:
				conn.commit()
				session['userdata'] = accountR
				return 'ok'
			else:
				return '注册失败'

		else:
			return ''
	except Exception as e:
		print(e)

@app.route('/verifyusername',methods=['POST'])
def verifyusername():
	if request.method == 'POST':
		accountR = request.form.get('accountR').strip()#账号
		if accountR:
			conn = sqlite3.connect('game.db')
			c = conn.cursor()
			sql = "select * from info where accountr = '%s'"%accountR
			c.execute(sql)
			data = c.fetchall()
			if data:
				return '1'
			else:
				return '0'



if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8082)