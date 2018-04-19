

# s = '3333'

# print(s.isdigit())
# exit()



# f2 = open('333.txt','w')
# with open('222.txt','r') as f:
# 	for i in f:
# 		i = i.strip()
# 		if i.isdigit() and '0' not in i and '111'not in i and '222'not in i and '333'not in i and '444'not in i and '555'not in i and '666'not in i and '777'not in i and '999'not in i and len(i) == 6: 
# 			f2.write(i+'\n')
# 			print(i)

# import requests
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.23 Safari/537.36'}
# url = "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&fastloginfield=username&username=ntdgd573&password=a123456&quickforward=yes&handlekey=ls&inajax=1"
# url2 = "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1&handlekey=ls&quickforward=yes&password=a123456&username=ntdgd573"
# html = requests.get('http://www.shiliu2.cc'+url2,headers=headers,allow_redirects=False)
# print(html.text)


import base64
s = base64.b64encode('sssssssss'.encode().decode('utf8').encode())
print(s)
print(base64.b64decode('c3Nzc3Nzc3Nz'))
 
