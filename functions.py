

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



# %y 两位数的年份表示（00-99）
# %Y 四位数的年份表示（000-9999）
# %m 月份（01-12）
# %d 月内中的一天（0-31）
# %H 24小时制小时数（0-23）
# %I 12小时制小时数（01-12）
# %M 分钟数（00=59）
# %S 秒（00-59）
# %a 本地简化星期名称
# %A 本地完整星期名称
# %b 本地简化的月份名称
# %B 本地完整的月份名称
# %c 本地相应的日期表示和时间表示
# %j 年内的一天（001-366）
# %p 本地A.M.或P.M.的等价符
# %U 一年中的星期数（00-53）星期天为星期的开始
# %w 星期（0-6），星期天为星期的开始
# %W 一年中的星期数（00-53）星期一为星期的开始
# %x 本地相应的日期表示
# %X 本地相应的时间表示
# %Z 当前时区的名称
# %% %号本身
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


from PIL import Image,ImageDraw

def zoom(filepath,width,height):
	#图片缩放
	from PIL import Image
	newImg = Image.new('RGBA',(width,height),(255,255,255))#创建一个新图片
	img = Image.open(filepath)#要缩放的图片
	w,h = img.size#获取原大小
	#w/h谁大按照谁缩放，目标大小width/height除以要缩放的图片w/h得出要缩放的比率
	if w > h:
		x = width / w
	else:
		x = height / h
	#按照x比率计算缩放大小
	ww = int(w*x)
	hh = int(h*x)
	img2 = img.resize((ww,hh),Image.ANTIALIAS)#缩放
	left = int((width - ww) / 2)#得出粘贴位置的left
	top = int((height - hh) / 2)#得出粘贴位置的top
	newImg.paste(img2,(left,top))#合并图片
	newImg.save('4.png','png')#保存图片

# zoom('1.jpg',800,800)

def circular(filepath):
	"""图片转换层圆形"""
	ima = Image.open(filepath).convert("RGBA")#打开要处理的图片
	# 获取最小半径
	size = ima.size
	r2 = min(size[0], size[1])
	#如果不是正方向 转换成正方形
	if size[0] != size[1]:
		ima = ima.resize((r2, r2), Image.ANTIALIAS)

	#创建透明图
	circle = Image.new('L', (r2, r2), 0)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, r2, r2), fill=255)
	alpha = Image.new('L', (r2, r2), 255)
	alpha.paste(circle, (0, 0))
	ima.putalpha(alpha)#给图片添加透明度
	ima.save('test_circle.png')