import imaplib
import email
# import chardet

email_='869688800@qq.com'
password='choqdwkaphjobcih'
def getEmail(username,password):

  #链接邮箱服务器
  conn = imaplib.IMAP4_SSL(r"imap.qq.com")
  #登录
  conn.login(email_,password)
  #收邮件
  INBOX = conn.select("INBOX")
  #全部邮件
  types, data = conn.search(None, 'UNSEEN')#UNSEEN 未读邮件 ALL全部邮件
  #邮件列表
  msgList = data[0].split()
  

  #读取邮件
  for r in msgList:
    try:
      subject=sender=date=to=body = ''
      types, datas = conn.fetch(r, '(RFC822)')
      #获取编码类型
      # fencoding=chardet.detect(datas[0][1])
      # if fencoding['encoding'] == 'ascii' or fencoding['encoding'] == 'utf-8':
      #   encoding = 'utf8'
      # else:
      encoding = None
      subject = None
      try:
        mail = email.message_from_string((datas[0][1].decode()))
        subject = email.header.decode_header(mail['subject'])[0][0].decode()#标题
        #主体内容
        for part in mail.walk():
          # 如果ture的话内容是没用的
          if not part.is_multipart():       
              # mycode=part.get_content_charset();
              body = part.get_payload(decode=True).decode('utf-8')

      except Exception as e:
        pass
      if not subject:
        try:
          mail = email.message_from_string((datas[0][1].decode('gb18030')))
          subject = email.header.decode_header(mail['subject'])[0][0].decode('gb18030')#标题
          #主体内容
          for part in mail.walk():
            # 如果ture的话内容是没用的
            if not part.is_multipart():       
                # mycode=part.get_content_charset();
                body = part.get_payload(decode=True).decode('utf-8')

        except Exception as e:
          pass
      if not subject:
        try:
          mail = email.message_from_string((datas[0][1].decode('gbk')))
          subject = email.header.decode_header(mail['subject'])[0][0].decode('gbk')#标题
          #主体内容
          for part in mail.walk():
            # 如果ture的话内容是没用的
            if not part.is_multipart():       
                # mycode=part.get_content_charset();
                body = part.get_payload(decode=True).decode('utf-8')

        except Exception as e:
          pass
      print(subject)
      if body:
        sender = mail['X-QQ-ORGSender']#发件人
        date = mail['Date']#发件时间
        # print(email.header.decode_header(mail['From'])[0][0].decode())#标题
        to = mail['To']#收件人
            
    except Exception as e:
      pass

getEmail(email_,password)



# for row in mail.keys():
#   print(row)
#   try:
#     print(email.header.decode_header(mail[row])[0][0]) 
#   except Exception as e:
#     print(e)
#     pass

# print(datas[0][1].decode().split("\r\n"))
# print(mail.keys() ,mail.items())

# def showmessage(mail):


#   if mail.is_multipart():


#     for part in mail.get_payload():


#       showmessage(part)


#   else:


#     type=mail.get_content_charset()


#     if type==None:


#       print (mail.get_payload())


#     else:


#       try:


#         print(mail.get_payload('base64'))


#       except UnicodeDecodeError:


#          print (mail)