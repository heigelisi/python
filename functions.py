

#邮件发送
# files = [];
# files.append({"file":"qrcode_for_gh_99ed93487fce_258.jpg","type":"image"})
# files.append({"file":"index.html","type":"html"})
# files.append({"file":"crm需求.txt","type":"plain"})
# sendEmail('vzhoufei@qq.com','测试发送','ffffffff',files)
def sendEmail(sendemail,title,body,files=[]):

	try:
		SERVER_ADDR = "869688800@qq.com";#发送方
		PASSWORD = "iuwxkkvurltxbbif";#必须是自动授权码,需要发送人的授权码
		SMTP_SERVER = 'smtp.qq.com'
		import os
		from email.mime.text import MIMEText#文本处理
		from email.header import Header#hader头处理
		from email.mime.multipart import MIMEMultipart
		from email.mime.image import MIMEImage#图片处理
		from email.utils import formatdate#时间
		message = MIMEMultipart()
		message['From'] = Header(SERVER_ADDR,'utf-8')#发件人
		message['To'] = Header(sendemail,'utf-8')#收件人
		message['Subject'] = Header(title,'utf-8')#标题
		if body:
			body = MIMEText(body,'plain','utf-8');#正文
			message.attach(body);

		#附件处理
		if files:
			for row in files:
				# print(row)
				if row.get('type') == 'image':
					with open(row.get('file'),'rb')as fp:
						picture = MIMEImage(fp.read())
					picture['Content-Type'] = 'application/octet-stream'
					picture['Content-Disposition'] = 'attachment;filename="%s"'%row.get('file')
					message.attach(picture);
				else:
					with open(row.get('file'),'r',encoding="utf8") as f:
						content = f.read()
					text = MIMEText(content,row.get('type'),'utf-8')
					#附件设置内容类型，方便起见，设置为二进制流
					text['Content-Type'] = 'application/octet-stream'
					#设置附件头，添加文件名
					basename = os.path.basename(row.get('file'))
					text['Content-Disposition'] = 'attachment;filename=%s'% basename
					#解决中文附件名乱码问题 
					if row.get('type') == 'plain':
						text.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', basename))
					message.attach(text)

			
		import smtplib
		# server = smtplib.SMTP(smtp_server,25)
		# 使用了ssl模式
		server = smtplib.SMTP_SSL(SMTP_SERVER,465)
		# 设置为调试模式
		server.set_debuglevel(1)
		# 登陆ssl服务器
		server.login(SERVER_ADDR,PASSWORD)
		# 发送邮件
		server.sendmail(SERVER_ADDR,[sendemail],message.as_string())
		# 退出
		server.quit()
	except Exception as e:
		print('发送失败');
		pass



# sendEmail('vzhoufei@qq.com','测试发送','哈哈哈哈哈哈啊哈哈哈哈哈');




def date(format_="%Y-%m-%d %H:%M:%S",timestamp=0):
	import time;
	if timestamp:
		timestamp = int(timestamp);
	else:
		timestamp = int(time.time());
	time_local = time.localtime(timestamp)
	#转换成新的时间格式(2016-05-05 20:28:54)
	return str(time.strftime(format_,time_local));


def md5(str):
	import hashlib
	return hashlib.md5(str.encode('utf-8')).hexdigest();


def printerr(e):
	"""打印异常"""
	print('发生错误的文件：', e.__traceback__.tb_frame.f_globals['__file__']);
	print('错误所在的行号：', e.__traceback__.tb_lineno);
	print('错误信息', e);


def setEnviron(path=None):
	"""设置环境变量"""
	import os;
	if not path:
		path = os.path.split(os.path.realpath(__file__))[0];#获取当前文件路径
	mydir = os.path.normpath(path);
	os.environ["PHANTOMJS"] = mydir;
	pathV = os.environ["PATH"];
	os.environ["PATH"]= mydir + ";" + os.environ["PATH"];





#加载ini配置文件
def loadCnf(path):
	config = {};
	with open(path,'r',encoding='utf8') as f:
		for r in f:
			row = r.strip();
			if not row:
				continue;
			if row[0] == "#":
				continue;
			if row[0] == '[' and row[-1] == ']':
				#配置标识
				cname = row[1:-1];
				config[cname] = {};
			key_val = row.split('=',1);
			if len(key_val) > 1:
				config[cname][key_val[0].strip()] = key_val[1].strip() or '';
	return config;