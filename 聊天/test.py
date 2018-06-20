


# import base64
# encode = base64.b64encode('中午') 
# print(ascii('aa'))
strs = b"\x81\x83\xaf\x05\xfa\x17\xceg\x99"
# str(strs, encoding='gbk')
print(strs.decode("gb18030"))


import json

data = {'name':"周菲",'age':'18'}

print(json.dumps(data))