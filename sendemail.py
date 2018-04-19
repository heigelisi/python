# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
# 第一个为文本内容,第二个设置文本格式,第三个编码格式
msg = MIMEText('Python邮件发送测试','plain','utf-8')
# 显示于发件人
msg['From'] = Header('我是发送方','utf-8')
# 显示与收件人
msg['To'] = Header('你自己','utf-8')
# 就是标题,最醒目的
subject = 'Python SMTP发送邮件测试_9.20'
msg['Subject'] = Header(subject,'utf-8')
# 
# 发送方
from_addr = '869688800@qq.com'
# 必须是自动授权码,需要发送人的授权码
password = 'iuwxkkvurltxbbif'

# qq的smtp服务器
smtp_server = 'smtp.qq.com'
# 接收方
to_addr = '1666549728@qq.com'
import smtplib
# server = smtplib.SMTP(smtp_server,25)
# 使用了ssl模式
server = smtplib.SMTP_SSL(smtp_server,465)
# 设置为调试模式
server.set_debuglevel(1)

# 登陆ssl服务器
server.login(from_addr,password)
# 发送邮件
server.sendmail(from_addr,[to_addr],msg.as_string())
# 退出
server.quit()

