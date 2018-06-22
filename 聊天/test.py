import json


stss =  b'\xe6\xb0\x93\xe8\x81\xad\xe7\xaf\x93\xe8\x8c\x85\xe6\x8b\xa2\xe8\x81\xbb'
for i in stss:
	print(i)



exit()
# print(ord('中'))
# # print(chr('0x30'))
# print('('.encode())
# print(ascii('aa'))

# msg = b"\x05B微信\x05D".decode()
# print(msg)
# exit()
# # print(chr(msg))
# message = {'code':200,'msg':msg}
# m = json.dumps(message)
# print(m)
# s = json.loads(m)
# print(s)
# exit()





# import base64
# encode = base64.b64encode('中午') 
# print(ascii('aa'))

# print(chr(21608),chr(45),chr(37),chr(30),chr(89))
print(chr(97),'sss')
print(ord('飞'))
# 160
# 30 
# 45 
# 37 
# 248
# 30 
# 89 
# 101
# 251
exit()
strs = b"\x81\x89^\xc7,\xed\xb8O\xbd\x08\xe0O\xc9H\xe3"



def parseData(msg): 
	g_code_length = msg[1] & 127 
	if g_code_length == 126: 
		g_code_length = struct.unpack('!H', msg[2:4])[0] 
		masks = msg[4:8] 
		data = msg[8:] 
	elif g_code_length == 127: 
		g_code_length = struct.unpack('!Q', msg[2:10])[0] 
		masks = msg[10:14] 
		data = msg[14:] 
	else: 
		masks = msg[2:6] 
		data = msg[6:] 
		i = 0 
		raw_by = bytearray() 
	for d in data: 
		raw_by.append( int(d) ^ int(masks[i % 4]) ) 
		i += 1 
	print(u"总长度是:%d" % int(g_code_length)) 
	raw_str = raw_by.decode() 
	return raw_str 

print(parseData(strs),'ssss')
# def hex_to_str(b):
#     s = ''
#     for i in b:
#         s += '{0:0>2}'.format(str(hex(i))[2:])
#     return(s)

# print(hex_to_str(strs))
# print(strs.decode('utf8'))
# # str(strs, encoding='gbk')
# print(strs.decode("gb18030"))


import json

data = {'name':"周菲",'age':'18'}

print(json.dumps(data))
# 8189c9e1e60c2f6977e9776903a974
  # 81895ec72cedb84fbd08e04fc948e3