import imaplib


email_='869688800@qq.com'
password='choqdwkaphjobcih'

# #链接邮箱服务器
conn = imaplib.IMAP4_SSL("imap.qq.com")
#登录
conn.login(email_,password)
#收邮件
INBOX = conn.select("INBOX")
#全部邮件
types, data = conn.search(None, 'ALL')
#邮件列表
msgList = data[0].split()
#最后一封
last = msgList[len(msgList) - 2]
# print(last)
#取最后一封
types, datas = conn.fetch(last, '(RFC822)')
#把取回来的邮件写入txt文档
# print(type(datas[0][1].decode()))
# print(datas[0][1].decode())
import email
mail = email.message_from_string((datas[0][1].decode()))
# print(email.header.decode_header(mail['subject']).decode() )
# print(mail['subject'])
print(email.header.decode_header(mail['subject'])[0][0].decode())


for row in mail.keys():
  try:
    print(email.header.decode_header(mail[row])[0][0].decode()) 
  except Exception as e:
    pass
# print(mail[row])
# print(row)



# print(datas[0][1].decode().split("\r\n"))
# print(mail.keys() ,mail.items())

def showmessage(mail):


  if mail.is_multipart():


    for part in mail.get_payload():


      showmessage(part)


  else:


    type=mail.get_content_charset()


    if type==None:


      print (mail.get_payload())


    else:


      try:


        print(mail.get_payload('base64'))


      except UnicodeDecodeError:


         print (mail)