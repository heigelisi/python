import imaplib
import email
import pymysql
import re
import time
import threading
import json
import os
import requests
from pyquery import PyQuery as pq
import sys,os
# import chardet
AccessToken = None
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
database = {'host':'localhost','user':'root','passwd':'8bee7008d7893cfc','db':'emaildata','charset':'utf8','port':3306}

class getEmail(object):

  def __init__(self):
    self.local = threading.local() 


  def login(self,emailname,emailpwd,followuserid):
    self.showMsg(emailname,'登陆...')
    self.local.followuserid = followuserid
    self.local.emailname = emailname
    try:
      #链接邮箱服务器
      conn = imaplib.IMAP4_SSL(r"imap.qq.com")
      #登录
      conn.login(emailname,emailpwd)
    except Exception as e:
      self.showMsg(emailname,'登陆失败！',e)
      exit()
    self.showMsg(emailname,'登陆成功')
    self.charge(conn)

  def charge(self,conn):
    """收取邮件"""
    while True:
      time.sleep(3)
      msgList = []
      try:
        #收邮件
        INBOX = conn.select("INBOX")
        #全部邮件
        types, data = conn.search(None, 'UNSEEN')#UNSEEN 未读邮件 ALL全部邮件
        #邮件列表
        msgList = data[0].split()
      except Exception as e:
        print(e)
        continue
      # print(msgList)
      self.showMsg(self.local.emailname,'收到',len(msgList),'条')
      iii = 0
      if msgList:
        #解析邮件
        for r in msgList:
          if iii > 30:
            continue
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
              mail = email.message_from_string((datas[0][1].decode('utf8')))
              subject = email.header.decode_header(mail['subject'])[0][0].decode('utf8')#标题
              #主体内容
              for part in mail.walk():
                # 如果ture的话内容是没用的
                if not part.is_multipart():       
                    # mycode=part.get_content_charset();
                    body = part.get_payload(decode=True).decode('utf8')
              # print('utf-8')
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
                      body = part.get_payload(decode=True).decode('gb18030')
                # print('gb18030')

              except Exception as e:
                pass
            if not subject:
              print(body)
              continue
              try:
                mail = email.message_from_string((datas[0][1].decode('gbk')))
                subject = email.header.decode_header(mail['subject'])[0][0].decode('gbk')#标题
                #主体内容
                for part in mail.walk():
                  # 如果ture的话内容是没用的
                  if not part.is_multipart():       
                      # mycode=part.get_content_charset();
                      body = part.get_payload(decode=True).decode('gbk')
                # print('gbk')

              except Exception as e:
                pass
            print(self.local.emailname,subject)
            if body:
              sender = mail['X-QQ-ORGSender']#发件人
              date = mail['Date']#发件时间
              # print(email.header.decode_header(mail['From'])[0][0].decode())#标题
              to = mail['To']#收件人
              
              #判断来源
              if '51job.com' in sender:
                self._51job_com(subject,sender,date,to,body)
                print('前程无忧')

              elif 'ganji.com' in sender:
                self.ganji_com(subject,sender,date,to,body)
                # print('赶集')

              elif 'zhaopinmail.com' in sender:
                

                self.zhaopinmail_com(subject,sender,date,to,body)
                print('智联招聘')


              elif '58.com' in sender:
                # with open('zhaopinmail_com.txt','w',encoding='utf8') as f:
                #   f.write(body)
                # body2 = ''
                # with open('zhaopinmail_com.txt','r',encoding='utf8') as f2:
                #   for line in f2:
                #     body2 += line
                self._58(subject,sender,date,to,body)
                print('58')

              else:
                print('未知来路')
                  
          except Exception as e:
            self.showMsg('收取邮件',e)
            pass
      else:
        continue


  def _51job_com(self,subject,sender,date,to,body):
    try:
      company = re.compile(r""".*?应聘职位.*?word-break:break-all">(.*?)</td>.*?font-weight:normal">(.*?)</strong>.*?([男女]).*?(\d+.*?岁\(\d{4}/\d{1,2}/\d{1,2}\)).*?word-break:break-all">(\d{11})</td>.*?word-break:break-all"><a href="mailto:(.*?)">.*?居住地：.*?break-all">(.*?)</td>.*?""",re.S)
      basic = re.search(company,body)
      position = basic.group(1)
      username = basic.group(2)
      sex = basic.group(3)
      age = basic.group(4)
      mobile = str(basic.group(5))
      email = basic.group(6)
      address = basic.group(7)
      company = re.compile(r'.*?>(.*?)<.*?',re.S)
      text = re.findall(company,body)
     
      html = pq(body)
      texts = html('body').text()

      self.setData([username.strip(),age.strip(),sex.strip(),mobile.strip(),email.strip(),address.strip(),'前程无忧',texts.strip(),date,self.local.emailname,''])
      
    except Exception as e:
      self.showMsg('前程无忧',e)
      pass


  def ganji_com(self,subject,sender,date,to,body):
    print('赶集')
    try:
      company = re.compile(r"(\\u[a-z0-9]{4})",re.S)
      text = re.findall(company,body)
      for i in text:
        a = i.encode('gbk').decode('unicode_escape')
        body =  body.replace(i,a)
     
      company = re.compile(r""".*?font-weight:bold">(.*?)</span>.*?投递职位：.*?>(.*?)</span>.*?font-size:16px">(\1（.*?）)</p>.*?工作地点：(.*?)</span>.*?电话：.*?(\d{11}).*?邮箱：(.*?)</.*?""",re.S)
      basic = re.search(company,body)
      # print(basic)
      if basic:
        position = basic.group(2)
        username = basic.group(1)
        age_sex = basic.group(3).split('（')[1].split(' ')
        sex = age_sex[0]
        age = age_sex[1].rstrip('）')
        address = basic.group(4)
        mobile = str(basic.group(5))
        email = basic.group(6)
      else:
        return False


      html = pq(body)
      texts = html('body').text()
      self.setData([username.strip(),age.strip(),sex.strip(),mobile.strip(),email.strip(),address.strip(),'赶集',texts.strip(),date,self.local.emailname,''])

    except Exception as e:
      self.showMsg('赶集',e)
      pass

  def zhaopinmail_com(self,subject,sender,date,to,body):
    try:
      self.showMsg('智联招聘')
      # print(body)
      #基本资料
      company = re.compile(r'.*?<td>.*?line-height:50px">(.*?)</td>.*?style="font-weight:bold">([男|女])</font>.*?weight:bold">([0-9]+年[0-9]+月)</font><br />(.*?)<small.*?href="(https://ihr\.zhaopin\.com.*?)".*?',re.S)
      basic = re.search(company,body)
      if basic:
        username = basic.group(1)
        sex = basic.group(2)
        age = basic.group(3)
        address = basic.group(4)
        url = basic.group(5)
      else:
        return False
      #联系方式
      try:
        import urllib
        from urllib.parse import parse_qs
        query = urllib.parse.urlparse(url).query
        param = parse_qs(query)['param'][0]
        url = "https://ihr.zhaopin.com/resumemanage/emailim.do?s="+param
        contact = requests.get(url,headers=headers).text
        contact = json.loads(contact)
        if contact['code'] == 200:
          username = contact['data']['username']
          mobile = str(contact['data']['phone'])
          email = contact['data']['email']
        else:
          return False
      except Exception as e:
        self.showMsg('智联招聘1',e)
        return False

      html = pq(body)
      texts = html('table').text() 


      self.setData([username.strip(),age.strip(),sex.strip(),mobile.strip(),email.strip(),address.strip(),'智联招聘',texts.strip(),date,self.local.emailname,''])

    except Exception as e:
      self.showMsg('智联招聘',e)


  def _58(self,subject,sender,date,to,body):
    try:
      # body = str(body)
      # body = body.encode('utf8')
      # body = body.decode('utf8')
      company = re.compile(r"(\\u[a-z0-9]{4})",re.S)
      text = re.findall(company,body)
      for i in text:
        a = i.encode('gbk').decode('unicode_escape')
        body =  body.replace(i,a)
       
      company = re.compile(r'.*?应聘职位.*?href="(.*?)".*?target="_blank">(.*?)<.*?weight:normal;">(.*?)<span.*?>（(.*?)）<.*?white-space:nowrap;">现居住(.*?)</li>.*?手机号码：.*?>(\d{11}?)<.*?电子邮箱.*?>(.*?)<.*?',re.S)
      basic = re.search(company,body)
      if basic:
        class_url = basic.group(1)
        zhiwei = basic.group(2)
        username = basic.group(3)
        sex_age = basic.group(4).split('，')
        sex = sex_age[0]
        age = sex_age[1]
        address = basic.group(5)
        mobile = str(basic.group(6))
        email = basic.group(7)
        # print(class_url,zhiwei,username,sex,age,address,mobile,email)

      html = pq(body)
      texts = "应聘职位："+zhiwei+html('body').text()
      self.setData([username.strip(),age.strip(),sex.strip(),mobile.strip(),email.strip(),address.strip(),'58',texts.strip(),date,self.local.emailname,class_url])



    except Exception as e:
      self.showMsg('58同城',e)
      pass


  def setData(self,data,ii=1):
    print(data)
    if ii > 4:
      return False
    ii += 1
    data2 = data
    try:
      # data[1] = re.findall(r'\d+',data[1])[0]
      connect = pymysql.connect(host=database['host'],user=database['user'],passwd=database['passwd'],db=database['db'],charset=database['charset'],port=int(database['port']));#链接数据库
      cursor = connect.cursor();#创建一个游标
      #生成用户唯一表示
      import hashlib
      validation = data[0]+data[1]+data[2]+data[3]+data[4]
      validation2 = hashlib.md5(validation.encode('utf-8')).hexdigest()
      data.append(validation2)
      #查询是否已经存在
      sql = "select id from info where validation = '%s' limit 1"%validation2
      res1 = cursor.execute(sql)
      if res1:
        self.showMsg(self.local.emailname,data[0],'已经存在')
        connect.close()
        return False
      #转换成localtime
      timestamp = int(time.time())
      time_local = time.localtime(timestamp)
      #转换成新的时间格式(2016-05-05 20:28:54)
      dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
      data.append(str(dt))
      self.showMsg(self.local.emailname,data)
      
      # data.append(self.local.username)
      insert = "insert into info(username,age,sex,phone,email,address,source,texts,deliverytime,froms,class_url,validation,addtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      res = cursor.execute(insert,(data))
      if res:
        connect.commit()
      connect.close()
    except Exception as e:
      self.showMsg('setData',e)
      try:
        connect.close()
      except Exception as e:
        pass
      time.sleep(3)
      self.setData(data2,ii)

  def setDataEC(self):
    """"""
    while True:
      try:
        file = 'static/id.txt'
        id_ = 0
        if os.path.exists(file):
          with open(file,'r',encoding='utf8') as f:
            id_f = f.read()
            if id_f:
              id_ = id_f.strip()


        sql = 'select username,age,sex,phone,email,address,source,texts,id,froms,deliverytime,class_url from info where id > %s limit 100'%(str(id_))
        connect = pymysql.connect(host=database['host'],user=database['user'],passwd=database['passwd'],db=database['db'],charset=database['charset'],port=int(database['port']));#链接数据库
        cursor = connect.cursor();#创建一个游标
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
          time.sleep(3)
          continue
        
        if AccessToken:
          for r in data:
            id_ = r[8]
            birthday = None
            # birthday = '2018/5/31'
            sex = r[2].strip() or '0'
            phone = r[3].strip()
            email = r[4].strip()
            address = r[5].strip() or '无'
            source = r[6].strip() or '无'
            if r[7]:
              text =re.split(r'\s+',r[7])  
              strs = '|'.join(text)
              strs = strs.replace('：|','：')
              f_memo = strs[0:490]
              f_memo2 = strs[490:1480]
              f_memo3 = strs[1480:2470]
              f_memo4 = strs[2470:3460]
            else:
              f_memo = ''
              f_memo2 = ''
              f_memo3 = ''
              f_memo4 = ''

            

            #处理生日
            age = None
            #获取当前的年份
            #转换成localtime
            timestamp = int(time.time())
            time_local = time.localtime(timestamp)
            #转换成新的时间格式(2016-05-05 20:28:54)
            y_ = int(time.strftime("%Y",time_local))
            pattern = re.compile(r'.*?(\d+)\s?年(\d+)\s?月.*?',re.S)
            age = re.search(pattern,r[1])
            if age:
              birthday = age.group(1)+'/'+age.group(2)+'/30'
              age_ = int(y_) - int(age.group(1))

            if not birthday:
              pattern = re.compile(r'.*?(\d+/\d+/\d{0,2}).*?',re.S)
              age = re.search(pattern,r[1])
              if age:
                birthday = age.group(1)
                #提取年份
                pattern = re.compile(r'.*?(\d+)/(\d+)/\d{0,2}.*?',re.S)
                y_1 = re.search(pattern,birthday)
                age_ = int(y_) - int(y_1.group(1))

            if not birthday:
              pattern = re.compile(r'.*?(\d+\s?)岁.*?',re.S)
              age2 = re.search(pattern,r[1])
              if age2:
                age3 = int(age2.group(1))
                
                y = y_ - age3
                birthday = str(y)+'/12/30'
                age_ = age3

            # 过滤年龄 男：18-35 女：18:30
            if sex == '男':
              if age_ < 18 or age_ > 35:
                continue
            if sex == '女':
              if age_ < 18 or age_ > 30:
                continue

            if not birthday:
              birthday = '2018/5/31'
            # 5698609
            followUserId = '7508618'
            # for c in config.emails:
            #   if c[0] == r[9]:
            #     followUserId = c[3]

            data_ = {
                    "optUserId":7508618,
                    # "groupId":5698611,
                    "followUserId":followUserId,
                    "f_name": r[0],
                    "f_birthday": birthday,
                    "f_title": r[9].replace('@qq.com',''),
                    "f_company":r[10],
                    # "f_mobile": phone,
                    "f_company_addr": address,
                    "f_memo": f_memo,
                    "f_gender": sex,
                    "f_channel": source,
                    "81116447":f_memo2,
                    "81127941":f_memo3,
                    "81127942":f_memo4,
                    "81127942":r[11],
                    "customFieldMapping": {
                      "81116447": {
                          "option_id": "",
                          "type": "1"
                      },
                      "81127941":{
                          "option_id": "",
                          "type": "1"
                      },
                      "81127942": {
                          "option_id": "",
                          "type": "1"
                      },
                      "81163784": {
                          "option_id": "",
                          "type": "1"
                      }
                    }
                }
            if email:
              data_['f_email'] = email
            if phone:
              data_['f_mobile'] = phone
            data_ = json.dumps(data_)
            url = 'https://open.workec.com/customer/addCustomer'
            headers = {'authorization':AccessToken,'corp_id':'5698610','cache-control':'no-http://xiaorui.cc/page/2/','content-type':'application/json'}
            res = requests.post(url,headers=headers,data=data_).text
            resjson = json.loads(res)
            if resjson['errCode'] == 200:
              #写入EC成功 记录
              #转换成localtime
              timestamp = int(time.time())
              time_local = time.localtime(timestamp)
              #转换成新的时间格式(2016-05-05 20:28:54)
              dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
              self.statistical(id_,dt)

            resmsg = res+'录入客户：'+r[0]+phone
            self.showMsg(resmsg)
            with open('static/log.log','a',encoding='utf8') as f2:
              f2.write(resmsg+'\r\n')

        else:
          continue

      except Exception as e:
        self.showMsg('setDataEC',e)
        pass
      try:
        connect.close()
      except Exception as e:
        pass
      with open(file,'w',encoding='utf8') as f3:
        f3.write(str(id_))
      time.sleep(60)

  def cacheaccesstoken(self):
    while True:
      try:
        headers = {'cache-control':'no-cache','content-type':'application/json'}
        data_ = json.dumps({'appId':342620696708382720,'appSecret':'OhPE5SGH9ygLUwIlglA'})
        url = 'https://open.workec.com/auth/accesstoken'
        accessToken = json.loads(requests.post(url,headers=headers,data=data_).text)
        if accessToken['errCode'] == 200:
          global AccessToken
          AccessToken = accessToken['data']['accessToken']
          print(AccessToken)
        time.sleep(7000)
      except Exception as e:
        time.sleep(3)
        self.showMsg('cacheaccesstoken',e)


  def statistical(self,infoid,datatime):
    """统计入库EC数据"""
    while True:
      try:
        connect = pymysql.connect(host=database['host'],user=database['user'],passwd=database['passwd'],db=database['db'],charset=database['charset'],port=int(database['port']));#链接数据库
        cursor = connect.cursor();#创建一个游标
        sql = "insert into statistical(info_id,addtime) values(%s,%s)"
        res = cursor.execute(sql,([str(infoid),datatime]))
        if res:
          connect.commit()
        connect.close()
        break
      except Exception as e:
        print(e)
        try:
          connect.close()
        except Exception as e:
          pass
        time.sleep(3)
        self.statistical(infoid,datatime)

  def showMsg(self,*msg):
    try:
      msg = ','.join(msg)
      sys.stdout.write(msg+'\r\n')
      sys.stdout.flush()
    except Exception as e:
      pass

  def main(self):
    try:
      w2 = threading.Thread(target=self.cacheaccesstoken)
      w2.start()
      w = threading.Thread(target=self.setDataEC)
      w.start()

      try:
        connect = pymysql.connect(host=database['host'],user=database['user'],passwd=database['passwd'],db=database['db'],charset=database['charset'],port=int(database['port']));#链接数据库
        cursor = connect.cursor();#创建一个游标
        sql = "select emailname,emailpwd,followuserid from config"
        cursor.execute(sql)
        data = cursor.fetchall()
        connect.close()
      except Exception as e:
       
        self.showMsg('数据库连接失败',e)
        exit()

      

      for row in data:
        print(row)
        w = threading.Thread(target=self.login,args=(row[0],row[1],row[2],))
        w.start()
    except Exception as e:
      print(e)
      exit()

if __name__ == '__main__':
  getEmail().main()
