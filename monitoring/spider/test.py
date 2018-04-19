

# print(int('button2'))
# load = MyImages.open(self.path+r'static/qrcode.png')
# pic = ImageTk.PhotoImage(load)
# label = tkinter.Label(self.root,image=pic)
# label.pack()  #place

# url = 'http://bbs.fuliking1.com'
# import redis
pool = redis.ConnectionPool(host='localhost', port=6379)
conn = redis.Redis(connection_pool=pool)
# conn.sadd('Waiting',url)



# class tests(object):
# 	__s = 1
# 	"""docstring for test"""
# 	def __init__(self, *arg):
# 		self.arg = arg
# 		print(self.arg)
# 		print(self.__s)


# import random
# # ss = tests(1,2,3,4)

# # s = '返回一个原字符串居中,并使用空格填充至长度 width 的新字符串'
# # ss = s.find('使用')
# # if ss:
# # 	print(ss)

# l = '0123456789ABCDEFGHIJKRMNOPQLSTUVWSYZabcdefghijklmnopqrstuvwxyz'
# print(int(random.uniform(666666,999999)))

import sqlite3

# conn = sqlite3.connect('./test.db')

# cursor = conn.cursor()

# sql = """
# select * from test where id = 100
# """

# # sql = "insert into test(id,name,username) values(1,'ssss','ssss')"

# res = cursor.execute(sql)
# print(cursor.fetchall())

# # conn.commit()
# cursor.close()

# import requests 

# conn = requests.Session()

# html = conn.get('http://localhost/index.html')
# encoding = requests.utils.get_encodings_from_content(html.text)[0]
# print(encoding)
# html.encoding = encoding
# print(html.text.encode().decode('utf8'))

# proxies = {
# 	"http":"http://14.29.47.90:3128"
# }
# headers={
# 'Cookie': 'mkSu_2132_smile=1D1; Hm_lvt_120f2599df7b2f55c4dd213c6a168c76=1520595342,1520902610; UM_distinctid=1621f50725f953-08618cf5510bcf-72113b4f-1fa400-1621f5072603db; QsYl_2132_smile=3D1; a7801_times=1; c693_2132_smile=1D1; Hm_lvt_6a60b923391636750bd84d6047523609=1520952134; 6U2l_2132_smile=1D1; Hm_lvt_bfd8626bac88fcdca6214c1fa8a5ea54=1520952217; bdshare_firstime=1520966836702; CNZZDATA1259328574=1027813708-1520940134-http%253A%252F%252Fwww.xkx7.cc%252F%7C1520996563; _ga=GA1.2.351202285.1520998508; IxKV_2132_smile=1D1; Hm_lvt_63b8f8f4895a04769ec9d88bfd02f566=1520949235,1521000099; CNZZDATA1269830048=1848790055-1520999552-http%253A%252F%252Fwww.xkx7.cc%252F%7C1520999552; UM82_2132_smile=1D1; a6887_times=1; yone_2132_smile=1D1; CNZZDATA1254974964=1950833054-1520996066-http%253A%252F%252Fwww.xkx7.cc%252F%7C1520996066; stbS_2132_smile=1D1; GJ6p_2132_smile=1D1; a7697_times=2; CNZZDATA1271388845=496354700-1520996150-http%253A%252F%252Fwww.xkx7.cc%252F%7C1521001565; CNZZDATA1261686664=444845189-1521006871-http%253A%252F%252Fwww.xkx7.cc%252F%7C1521006871; Hm_lvt_3422d8ed69debba8fec024354a744f47=1521013134; CNZZDATA1261963471=562199860-1520995749-null%7C1521011794; PHPSESSID=irpctqeot13modkhuneo142ga5; equipment=116.23.154.215_489902',
# 'Host': 'www.xkx7.cc',
# 'Referer': 'http://www.xkx7.cc/vip-index-index-type-3.jsp',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.23 Safari/537.36'
# }



# html = requests.get('http://www.xkx7.cc/vip-index-redirects-id-46.jsp',headers=headers)
# print(html.url)
# print(html.text)