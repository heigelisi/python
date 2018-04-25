
str_ = ''
with open('mg.txt','r',encoding='utf8') as f:
	for i in f:
		name = i.strip()
		if name:
			str_ += "['%s','ffff'],"%name



print(str_)